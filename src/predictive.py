"""Hold-out evaluation of synthetic laboratory assay regression."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

FEATURES = ["product", "temperature_c", "ph", "target"]

def evaluate_assay_model(df, seed=42):
    """Evaluate without leakage: deviation and out_of_spec are excluded."""
    data = df.dropna(subset=FEATURES + ["assay_pct"])
    if len(data) < 30:
        raise ValueError("Se necesitan al menos 30 muestras completas.")
    X_train, X_test, y_train, y_test, ids_train, ids_test = train_test_split(
        data[FEATURES], data["assay_pct"], data["sample_id"],
        test_size=0.25, random_state=seed)
    preprocessor = ColumnTransformer([
        ("product", OneHotEncoder(handle_unknown="ignore"), ["product"]),
        ("numeric", "passthrough", ["temperature_c", "ph", "target"])])
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(n_estimators=80, min_samples_leaf=3,
                                         random_state=seed, n_jobs=-1))])
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    baseline = DummyRegressor(strategy="mean").fit(X_train, y_train).predict(X_test)
    rows = []
    for name, values in [("Random Forest", prediction), ("Referencia (media)", baseline)]:
        rows.append({"Modelo": name, "MAE": mean_absolute_error(y_test, values),
                     "RMSE": np.sqrt(mean_squared_error(y_test, values)),
                     "R²": r2_score(y_test, values)})
    results = pd.DataFrame({"Muestra": ids_test.to_numpy(),
                            "Real (%)": y_test.to_numpy(),
                            "Predicción (%)": prediction,
                            "Error absoluto": np.abs(y_test.to_numpy() - prediction)})
    return pd.DataFrame(rows), results
