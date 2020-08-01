from collections import defaultdict
from typing import Dict, Set

import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver


class Stats:
    def __init__(self):
        self.driver = self._get_driver()
        self.start_year, self.end_year = (2011, 2019)
        self.stat_codes = {
            233: ["Won", "Lost"],
            228: ["Goals"],
            229: ["Goals Allowed"],
        }
        self.playoffs = None

    def get_season_stats(self) -> pd.DataFrame:
        stats = []
        for code, cols in self.stat_codes.items():
            df = self._get_stat_table(code)
            stats.append(df[cols])
        merged = pd.concat(stats, axis=1)
        self.playoffs = self.get_playoff_teams()
        return self._clean_df(merged)

    def get_playoff_teams(self) -> Dict[int, Set[str]]:
        playoff_teams_dict = defaultdict(list)
        for year in range(self.start_year, self.end_year + 1):
            playoff_teams_dict[year] = self._get_playoff_teams(year)
        return playoff_teams_dict

    def _get_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        options.add_argument("--headless")
        return webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)

    def _get_query(self, stat_code: int) -> str:
        url = "http://stats.ncaa.org/rankings/national_ranking"
        base_qry = "?division=1.0&ranking_period=15.0&sport_code=MLA"
        custom_qry = f"&academic_year={self.start_year}.0&stat_seq={stat_code}.0"
        return f"{url}{base_qry}{custom_qry}"

    def _get_stat_table(self, stat_code: int) -> pd.DataFrame:
        query = self._get_query(stat_code)
        self.driver.get(query)

        tbls = []
        for year in range(self.start_year, self.end_year + 1):
            self._click_year(year)
            self._click_show_entries()
            tbl = self.driver.find_element_by_id("rankings_table")
            df = pd.read_html(tbl.get_attribute("outerHTML"))[0]
            df.loc[:, "Year"] = year
            df.set_index(["Team", "Year"], inplace=True)
            logger.info(f"{year} - {stat_code} - shape: {df.shape}")
            tbls.append(df)
        return pd.concat(tbls)

    def _click_show_entries(self) -> None:
        css = "#rankings_table_length > label:nth-child(1) > select:nth-child(1)"
        drp_length = self.driver.find_element_by_css_selector(css)
        for option in drp_length.find_elements_by_tag_name("option"):
            if option.get_attribute("value") == "-1":
                option.click()
                break

    def _click_year(self, year: int) -> None:
        drp_acadyr = self.driver.find_element_by_id("acadyr")
        for option in drp_acadyr.find_elements_by_tag_name("option"):
            if option.get_attribute("value") == f"{year}.0":
                option.click()
                break

    def _click_playoffs(self) -> None:
        drp_ranking = self.driver.find_element_by_id("rp")
        for option in drp_ranking.find_elements_by_tag_name("option"):
            if "DI" in option.text:
                option.click()
                break

    def _get_playoff_teams(self, year: int) -> Set[str]:
        if year < 2017:
            return self._get_playoff_teams_old(year)
        return self._get_playoff_teams_new(year)

    def _get_playoff_teams_old(self, year: int) -> Set[str]:
        bad_data = {
            "Albany (NY)": "Albany",
            "Detroit": "Detroit Mercy",
            "NAVY": "Navy",
            "OSU": "Ohio St.",
            "UAlbany": "Albany",
            "Yale Bulldogs": "Yale",
            "YALE": "Yale",
        }
        url = f"http://fs.ncaa.org/Docs/stats/m_lacrosse_champs_records/{year}/d1/html/confstat.htm"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        teams = [link.get_text() for link in soup.find_all("a")]
        return {
            team if team not in bad_data else bad_data[team]
            for team in teams[4:]
            if team != "Box score"
        }

    def _get_playoff_teams_new(self, year: int) -> Set[str]:
        self._click_year(year)
        self._click_playoffs()
        tbl = self.driver.find_element_by_id("rankings_table")
        df = pd.read_html(tbl.get_attribute("outerHTML"))[0]
        return {tc.split("(")[0].strip() for tc in df.Team}

    def _check_playoffs(self, team, year):
        return "yes" if team in self.playoffs[year] else "no"

    def _clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[~df.index.isin(["Reclassifying"], level=0)].copy()
        df.dropna(inplace=True)
        years = [idx[-1] for idx in df.index]
        team_conf = [idx[0] for idx in df.index]
        teams = [team.split("(")[0].strip() for team in team_conf]
        confs = [team.split("(")[-1].strip(")") for team in team_conf]
        df.reset_index(inplace=True, drop=True)

        df.loc[:, "Team"] = teams
        df.loc[:, "Conference"] = confs
        df.loc[:, "Year"] = years
        df.loc[:, "Games"] = df.Won.astype(int) + df.Lost.astype(int)
        df.loc[:, "GPG"] = df["Goals"].astype(int) / df.Games.astype(int)
        df.loc[:, "GAPG"] = df["Goals Allowed"].astype(int) / df.Games.astype(int)
        df.loc[:, "Playoffs"] = [
            self._check_playoffs(tm, yr) for tm, yr in zip(df.Team, df.Year)
        ]
        cols = [
            "Team",
            "Conference",
            "Year",
            "Games",
            "Won",
            "Lost",
            "Goals",
            "GPG",
            "Goals Allowed",
            "GAPG",
            "Playoffs",
        ]
        return df[cols]
