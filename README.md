# Getaround rental prices estimation

The goal of this part is to understand the rental prices dataset, and to produce a model that can predict them. We use Mlflow as the framework to train our model, and use it to store versions and deploy it as well. This model is deployed on Heroku and accessible through a simple REST API.

### Analysis

The first part of the work is to analyse and understand the data we are working with. There are two notebooks in the corresponding folder. 

The first one is ml.ipynb, which is a short automl try to produce a baseline model.

The second one is a short analysis, to understand the data, the target, and do some cleanup before actually producing a model.

### Model and training

As said, the model is trained through Mlflow. Mlflow is run locally, and all storage will be done in ./mlruns.

To train a model, you should first create two experiments, fast_training and production training:

mlflow experiments create -n fast_training

mlflow experiments create -n production_training

Then, you can make use of the two endpoints and launch them in their corresponding experiment:

mlflow run -e production_training . --env-manager=local --experiment-id=980197819695436151

mlflow run -e fast_training . --env-manager=local --experiment-id=351747242691598775 -P n_estimators=100 -P learning_rate=0.1 -P max_depth=4

Fast training will be used for prototyping, with a small learning rate, and production training will be with the best parameters found. Production training will also register the model, so a version of it is available for serving, and will also save it in the assets folder of the API (which would not be done if the mlflow server was hosted online.)


The model itself it an XGBoost regressor, as it gives good performances on this dataset, and makes good use of the categories present here.


### Serving

We use FastAPI as our serving tool. It has only one route /prediction, that calls the model that is loaded through MLflow.

It can either be run with uvicorn, with the command getaround uvicorn main:app --reload, or be ran as a container with the Dockerfile present inside the api folder.
