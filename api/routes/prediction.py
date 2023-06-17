"""Module defining the 'prediction' router."""

from fastapi import APIRouter
from models.rental_price_prediction.input import RentalPriceInput
from prediction import rental_price_prediction

router = APIRouter(
    prefix="/predict",
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=list[float])
async def make_prediction(input_json: RentalPriceInput) -> list[float]:
    """Car rental price prediction endpoint.

    Args:
        input_json (RentalPriceInput): A json containing a list of car caracteristics.

    Returns:
        list[float]: The corresponding list of rental prices estimations.
    """
    return rental_price_prediction.prediction(input_json.cast_to_dataframe())
