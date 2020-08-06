import statsmodels.api as sm


def calculate_win_predictor(df):
    wp = (0.5 + 0.08 * (df["GPG"] - df["GAPG"])) * df["Games"]
    return [0 if n < 0 else round(n, 1) for n in wp]


def calculate_pythagorean_expectation(df, exp=2):
    return 1 / 1 + (df["Goals"] / df["Goals Allowed"])**exp


def split_data(df, year=2019):
    mask = df.Year >= year
    return df[~mask], df[mask]


def fit_model(X, y):
    X = sm.add_constant(X)
    return sm.OLS(y, X).fit()


def make_predictions(model, X):
    X = sm.add_constant(X)
    return model.predict(X)
