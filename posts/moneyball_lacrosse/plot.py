import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
from loguru import logger
from sklearn.metrics import r2_score

from util import fit_model, make_predictions


def generate_model_plot(df, x, y, preds, out_file=None, title=None):
    plt = px.scatter(
        df,
        x=x,
        y=y,
        color="Playoffs",
        hover_name="Team",
        hover_data=["Year"],
        title=title,
        labels={
            "Made_Playoffs": "Playoffs",
        },
        template="plotly_dark",
    )
    plt_ols = plt.add_traces(
        go.Scatter(x=df[x], y=preds, mode="lines", name="OLS")
    )
    pio.write_json(plt_ols, file=out_file)


def generate_model_plots(train, test):
    # Train WinPredictor model
    model = fit_model(train.WinPredictor, train.Won)
    generate_model_plot(
        train,
        "WinPredictor",
        "Won",
        model.fittedvalues,
        out_file="plots/model_plot_train.json",
        title="Actual Wins vs. Projected Wins [2011-2018]",
    )
    logger.info(f"\n{model.summary()}")

    # Calculate and visualize predictions
    preds = make_predictions(model, test.WinPredictor)
    generate_model_plot(
        test,
        "WinPredictor",
        "Won",
        preds,
        out_file="plots/model_plot_test.json",
        title="Actual Wins vs. Projected Wins 2019",
    )
    pred_df = pd.DataFrame(
        dict(year=test.Year, team=test.Team, won=test.Won, pred=preds)
    ).reset_index(drop=True)
    logger.info(f"R2 Score: {r2_score(test.Won, preds)}")
    logger.info(f"\n{pred_df}")

    # Train GPG model
    gpg_model = fit_model(train.GPG, train.WinPct)
    generate_model_plot(
        train,
        "GPG",
        "WinPct",
        gpg_model.fittedvalues,
        out_file="plots/model_plot_gpg_train.json",
        title="Goals Per Game vs. Win Percentage [2011-2018]",
    )
    logger.info(f"\n{gpg_model.summary()}")

    # Train GAPG model
    gapg_model = fit_model(train.GAPG, train.WinPct)
    generate_model_plot(
        train,
        "GAPG",
        "WinPct",
        gapg_model.fittedvalues,
        out_file="plots/model_plot_gapg_train.json",
        title="Goals Against Per Game vs. Win Percentage [2011-2018]",
    )
    logger.info(f"\n{gapg_model.summary()}")
