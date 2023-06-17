"""Module defining where predictions are made."""

from pandas import DataFrame
from prediction.model import XGBoost_model


def prediction(input: DataFrame) -> list[float]:
    """Make a prediction for the given dataframe of inputs.

    Args:
        input (DataFrame): A list of numerical and text values corresponding to multiple vehicles.

    Returns:
        list[float]: The estimated rental prices for the given vehicles.
    """
    return XGBoost_model.predict(input).tolist()
