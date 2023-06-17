"""This module should be used through the mlflow CLI. It will fit a model given certain parameters.

Make sure to launch them in specific experiments, through the MLproject endpoints.

For example:

mlflow experiments create -n fast_training

mlflow run -e fast_training . --env-manager=local --experiment-id=351747242691598775 -P n_estimators=100 -P learning_rate=0.1 -P max_depth=4
"""

import logging
import warnings
from typing import Tuple

import click
import mlflow
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual: np.array, pred: np.array) -> Tuple[float, float, float]:
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


@click.command(
    help="Trains an XGBoost Regressor model." "The model and its metrics are logged with mlflow."
)
@click.option("--learning_rate", type=click.FLOAT, default=1e-2, help="Learning rate.")
@click.option("--n_estimators", type=click.INT, default=50, help="Number of estimators.")
@click.option("--max_depth", type=click.INT, default=3, help="Max tree depth.")
@click.option("--seed", type=click.INT, default=1, help="Seed for the random generator.")
@click.option(
    "--register",
    type=click.BOOL,
    default=False,
    help="Wether to register the model at the end of training.",
)
@click.option(
    "--experiment-id",
    type=click.STRING,
    default="default",
    help="Which experiment to start the run in.",
)
@click.argument("training_data")
def run(training_data, learning_rate, n_estimators, max_depth, seed, register, experiment_id):
    np.random.seed(seed)

    if register:
        # If the model should be registered, we give it a name so it can be registered.
        mlflow.xgboost.autolog(
            model_format="json", log_input_examples=True, registered_model_name="getaround-model"
        )
    else:
        # If not, no name is provided.
        mlflow.xgboost.autolog(model_format="json", log_input_examples=True)

    try:
        data = pd.read_csv(training_data)
    except Exception as e:
        raise Exception("Unable to open training csv. Error: %s", e) from e

    target = data["rental_price_per_day"]
    data = data.drop(columns=["rental_price_per_day"])

    category_columns = ["model_key", "fuel", "paint_color", "car_type"]

    # We set categorical columns as such, so that the XGB model can use them effectively.
    for col in category_columns:
        data[col] = data[col].astype("category")

    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.15)

    model = XGBRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        objective="reg:squarederror",
        random_state=seed,
        enable_categorical=True,
        tree_method="hist",  # Mandatory since we want to use categorical data.
    )

    with mlflow.start_run(experiment_id=experiment_id, tags={"production": register}):
        model.fit(X_train, y_train)

        predicted = model.predict(X_test)
        (rmse, mae, r2) = eval_metrics(y_test, predicted)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        if register:
            # This part is not really necessary in a normal workflow.
            # But as we use mlflow in a local setting and not with a remote server, we actually
            # need to save models locally as well so the API is able to use them.
            name = "getaround-model"
            client = mlflow.MlflowClient()
            try:
                latest = client.get_latest_versions(name, stages=["None"])[
                    0
                ].version  # index 0 because the list should contain only 1 element.
            except BaseException:
                latest = 1

            mlflow.xgboost.save_model(
                model, "./api/assets/getaround-model/" + str(latest), model_format="json"
            )


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    run()
