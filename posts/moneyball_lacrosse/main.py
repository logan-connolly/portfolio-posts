from pathlib import Path

import pandas as pd
import plotly.io as pio
import statsmodels.api as sm

from util import calculate_win_predictor, plot_wins, split_data
from scrape import Stats


def main():
    if not (fname := Path("data/teams.csv")).is_file():
        df = Stats().get_season_stats()
        df.to_csv(fname, index=False)

    df = pd.read_csv("data/teams.csv")
    df["Win_Predictor"] = calculate_win_predictor(df)
    train, test = split_data(df)

    X, y = train.Win_Predictor, train.Won
    model = sm.OLS(y, X).fit()
    preds = model.predict(test.Win_Predictor)

    fig1 = plot_wins(train)
    pio.write_html(fig1, file="plots/plot_1.html")

    print(pd.DataFrame(dict(team=test.Team, won=test.Won, pred=preds)))


if __name__ == "__main__":
    main()
