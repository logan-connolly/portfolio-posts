from pathlib import Path

import pandas as pd

from plot import generate_model_plots
from scrape import Stats
from util import calculate_pythagorean_expectation, split_data


def main():
    if not (fname := Path("data/teams.csv")).is_file():
        df = Stats().get_season_stats()
        df.to_csv(fname, index=False)

    df = pd.read_csv("data/teams.csv")
    df.loc[:, "WinPct"] = round(df.Won / df.Games, 4)
    df.loc[:, "ExpectPct"] = calculate_pythagorean_expectation(df, exp=1.23)
    df.loc[:, "WinPredictor"] = df["Games"] * df["ExpectPct"]
    train, test = split_data(df)
    generate_model_plots(train, test)


if __name__ == "__main__":
    main()
