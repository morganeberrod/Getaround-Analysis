"""Module containing the instanciation of the model(s)"""

import mlflow

name = "getaround-model"
client = mlflow.MlflowClient()

try:
    latest = client.get_latest_versions(name, stages=["None"])[
        0
    ].version  # index 0 because the list should contain only 1 element.
except BaseException:
    latest = 8

XGBoost_model = mlflow.pyfunc.load_model("./assets/getaround-model/" + str(latest))
