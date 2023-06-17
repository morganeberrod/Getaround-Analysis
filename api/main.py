"""Main module for the API."""

from fastapi import FastAPI
from routes import prediction

app = FastAPI(
    title="Getaround rental price",
    description="Basic API loading an MLflow model to predict rental prices.",
    version="1.0",
)


app.include_router(prediction.router)
