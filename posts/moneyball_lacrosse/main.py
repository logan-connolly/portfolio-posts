import pandas as pd
import plotly.io as pio
import plotly.graph_objs as go
import statsmodels.api as sm

from util import calculate_win_predictor, plot_wins, split_data


def main():
    df = pd.read_csv("data/teams.csv")
    df["Win_Predictor"] = calculate_win_predictor(df)
    df["Made_Playoffs"] = ["Yes" if p == 1 else "No" for p in df.Playoffs]
    train, test = split_data(df)

    fig1 = plot_wins(train)
    pio.write_html(fig1, file="plots/plot_1.html")

    X, y = train.Win_Predictor, train.Won
    model = sm.OLS(y, X).fit()
    preds = model.predict(test.Win_Predictor)
    print(pd.DataFrame(dict(team=test.Team, won=test.Won, pred=preds)))

    fig2 = fig1.add_traces(
        go.Scatter(x=X, y=model.fittedvalues, mode="lines", name="OLS")
    )
    pio.write_html(fig2, file="plots/plot_2.html")


if __name__ == "__main__":
    main()
