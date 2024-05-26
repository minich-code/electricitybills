# electricitybills



### dagshub 

MLFLOW_TRACKING_URI = https://dagshub.com/minich-code/electricitybills.mlflow

import dagshub
dagshub.init(repo_owner='minich-code', repo_name='electricitybills', mlflow=True)

import mlflow
with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)