import os
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import joblib

from src.ElectricityBill.utils.commons import read_yaml, create_directories, save_json
from src.ElectricityBill.entity.configuration_entity import ModelEvaluationConfig
from pathlib import Path


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config


    def predictions(self, model, X_test_transformed):
        
        y_pred = model.predict(X_test_transformed)
        
        return y_pred


    def model_evaluation(self, y_test, y_pred):
               
        # Evaluation metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

        
        # return
        return y_pred, mae, mse, r2, rmse, mape
        

    def save_results(self, y_test, y_pred):
        returned_values = self.model_evaluation(y_test, y_pred)
        mae, mse, r2, rmse, mape = returned_values[1:]  

        # Saving metrics as local
        scores = {"MAE": mae, "MSE":mse, "R2": r2, "RMSE": rmse, "MAPE": mape}
        save_json(path=Path(self.config.metric_file_name), data=scores)
