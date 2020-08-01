import plotly.express as px
import plotly.graph_objs as go


def calculate_win_predictor(df):
    wp = (0.5 + 0.08 * (df["GPG"] - df["GAPG"])) * df["Games"]
    return [0 if n < 0 else round(n, 1) for n in wp]


def split_data(df, year=2019):
    mask = df.Year >= year
    return df[~mask], df[mask]


def plot_wins(df):
    plt = px.scatter(
        df,
        x="Win_Predictor",
        y="Won",
        color="Playoffs",
        hover_name="Team",
        hover_data=["Lost", "Year"],
        title="Actual Wins vs. Projected Wins [2011-2018]",
        labels={
            "Win_Predictor": "Projected Wins",
            "Won": "Actual Wins",
            "Made_Playoffs": "Playoffs"
        },
        template="plotly_dark"
    )
    return plt.add_traces(
        go.Scatter(x=X, y=model.fittedvalues, mode="lines", name="OLS")
    )

