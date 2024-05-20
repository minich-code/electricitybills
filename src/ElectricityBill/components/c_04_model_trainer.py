import pandas as pd 
import os 
from src.ElectricityBill import logging
from sklearn.tree import DecisionTreeRegressor
import joblib 
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from src.ElectricityBill.entity.configuration_entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config


    def initiate_model_trainer(self, X_train_transformed, X_test_transformed, y_train, y_test):

        dt_model = DecisionTreeRegressor(
            criterion = self.config.criterion,
            splitter = self.config.splitter,
            min_samples_split = self.config.min_sample_split,
            min_samples_leaf = self.config.min_samples_leaf,
            min_impurity_decrease = self.config.min_impurity_decrease,
            ccp_alpha = self.config.ccp_alpha
        )

        dt_model.fit(X_train_transformed, y_train)

        joblib.dump(dt_model, os.path.join(self.config.root_dir, self.config.model_name))
        # Logging info 
        logging.info(f"Model Trainer completed: Saved to {os.path.join(self.config.root_dir, self.config.model_name)}")