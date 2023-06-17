"""Model class for the prediction input."""

from numpy import dtype
from pandas import CategoricalDtype, DataFrame
from pydantic import BaseModel


class RentalPriceInput(BaseModel):
    input: list[list]

    def cast_to_dataframe(self) -> DataFrame:
        """Transforms the input into a Categorical friendly representation.

        Returns:
            DataFrame: Dataframe with the right columns and dtype.
        """
        df = DataFrame(
            self.input,
            columns=[
                "model_key",
                "mileage",
                "engine_power",
                "fuel",
                "paint_color",
                "car_type",
                "private_parking_available",
                "has_gps",
                "has_air_conditioning",
                "automatic_car",
                "has_getaround_connect",
                "has_speed_regulator",
                "winter_tires",
            ],
        )

        dtypes = {
            "model_key": CategoricalDtype(
                categories=[
                    "Alfa Romeo",
                    "Audi",
                    "BMW",
                    "Citroën",
                    "Ferrari",
                    "Fiat",
                    "Ford",
                    "Honda",
                    "KIA Motors",
                    "Lamborghini",
                    "Lexus",
                    "Maserati",
                    "Mazda",
                    "Mercedes",
                    "Mini",
                    "Mitsubishi",
                    "Nissan",
                    "Opel",
                    "PGO",
                    "Peugeot",
                    "Porsche",
                    "Renault",
                    "SEAT",
                    "Subaru",
                    "Suzuki",
                    "Toyota",
                    "Volkswagen",
                    "Yamaha",
                ],
                ordered=False,
            ),
            "mileage": dtype("int64"),
            "engine_power": dtype("int64"),
            "fuel": CategoricalDtype(
                categories=["diesel", "electro", "hybrid_petrol", "petrol"], ordered=False
            ),
            "paint_color": CategoricalDtype(
                categories=[
                    "beige",
                    "black",
                    "blue",
                    "brown",
                    "green",
                    "grey",
                    "orange",
                    "red",
                    "silver",
                    "white",
                ],
                ordered=False,
            ),
            "car_type": CategoricalDtype(
                categories=[
                    "convertible",
                    "coupe",
                    "estate",
                    "hatchback",
                    "sedan",
                    "subcompact",
                    "suv",
                    "van",
                ],
                ordered=False,
            ),
            "private_parking_available": dtype("bool"),
            "has_gps": dtype("bool"),
            "has_air_conditioning": dtype("bool"),
            "automatic_car": dtype("bool"),
            "has_getaround_connect": dtype("bool"),
            "has_speed_regulator": dtype("bool"),
            "winter_tires": dtype("bool"),
        }

        for k, v in dtypes.items():
            df[k] = df[k].astype(v)

        return df
