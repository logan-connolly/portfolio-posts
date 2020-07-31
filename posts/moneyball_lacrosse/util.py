import plotly.express as px


def calculate_win_predictor(df):
    wp = (0.5 + 0.08 * (df.GPG - df.GAPG)) * df.Games
    return [0 if n < 0 else round(n, 1) for n in wp]


def split_data(df, year=2017):
    mask = df.Year >= year
    return df[~mask], df[mask]


def plot_wins(df):
    return px.scatter(
        df,
        x="Win_Predictor",
        y="Won",
        color="Made_Playoffs",
        hover_name="Team",
        hover_data=["Lost", "Year"],
        title="Actual Wins vs. Projected Wins [2014-2016]",
        labels={
            "Win_Predictor": "Projected Wins",
            "Won": "Actual Wins",
            "Made_Playoffs": "Playoffs"
        },
        template="plotly_dark"
    )
