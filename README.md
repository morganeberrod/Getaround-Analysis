# Getaround Analysis 🚗

The goal of this part is to understand the rental prices dataset, and to produce a model that can predict them. We use Mlflow as the framework to train our model, and use it to store versions and deploy it as well. This model is deployed on Heroku and accessible through a simple REST API.

## Project 🚧
For this case study, we suggest that you put yourselves in our shoes, and run an analysis we made back in 2017 🔮 🪄

When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.

Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time.

## Goals 🎯
In order to mitigate those issues we’ve decided to implement a minimum delay between two rentals. A car won’t be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental.

It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off.

Our Product Manager still needs to decide:

- threshold: how long should the minimum delay be?
- scope: should we enable the feature for all cars?, only Connect cars?

In order to help them make the right decision, they are asking you for some data insights. Here are the first analyses they could think of, to kickstart the discussion. Don’t hesitate to perform additional analysis that you find relevant.

- Which share of our owner’s revenue would potentially be affected by the feature?
- How many rentals would be affected by the feature depending on the threshold and scope we choose?
- How often are drivers late for the next check-in? How does it impact the next driver?
- How many problematic cases will it solve depending on the chosen threshold and scope?

## Analysis

The first part of the work is to analyse and understand the data we are working with. There are 3 notebooks in the corresponding folder. 

The first one is ml.ipynb, which is a short automl try to produce a baseline model.

The second one is a short analysis of pricing dataset, to understand the data, the target, and do some cleanup before actually producing a model.

The third one is the analysis of the delay.

## Model and training

As said, the model is trained through Mlflow. Mlflow is run locally, and all storage will be done in ./mlruns.

To train a model, you should first create two experiments, fast_training and production training:

``` mlflow experiments create -n fast_training ```

``` mlflow experiments create -n production_training ``` 

Then, you can make use of the two endpoints and launch them in their corresponding experiment:

``` mlflow run -e production_training . --env-manager=local --experiment-id=980197819695436151 ```

``` mlflow run -e fast_training . --env-manager=local --experiment-id=351747242691598775 -P n_estimators=100 -P learning_rate=0.1 -P max_depth=4 ```

Fast training will be used for prototyping, with a small learning rate, and production training will be with the best parameters found. Production training will also register the model, so a version of it is available for serving, and will also save it in the assets folder of the API (which would not be done if the mlflow server was hosted online.)


The model itself it an XGBoost regressor, as it gives good performances on this dataset, and makes good use of the categories present here.


## Serving

We use FastAPI as our serving tool. It has only one route /prediction, that calls the model that is loaded through MLflow.

It can either be run with uvicorn, with the command ``` getaround uvicorn main:app --reload ```, or be ran as a container with the Dockerfile present inside the api folder.

## Links 

API : https://mbd-getaround-rental-prices-c2066c4e09b8.herokuapp.com/docs

Web application : https://mbd-getaround-webapp.herokuapp.com/

## Details for certification purpose
email adress: morgane.berrod@gmail.com

video link: https://share.vidyard.com/watch/qR7L5ozHa6U7y8E2NcmP9y?

## Authors
**Morgane BERROD** - [MorganeBD](https://github.com/morganeberrod)

## Acknowledgements
A big thank you to [Mathieu](https://github.com/M-Garrigues) for his help on this project, especially on the ML part.
