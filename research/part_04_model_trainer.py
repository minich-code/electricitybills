from dataclasses import dataclass
from pathlib import Path

from src.ElectricityBill.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.ElectricityBill.utils.commons import read_yaml, create_directories, save_json
from research.part_03_data_transformation import DataTransformationConfig


# Entity 
@dataclass
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    # DecisionTreeRegressor Parameter 
    criterion: str
    splitter: str 
    min_sample_split: int
    min_samples_leaf: int
    min_impurity_decrease: float
    ccp_alpha: float

# Class for the configuration manager 
class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH):
        
        # Initialize the configuration manager 
        # Read YAML configurations files to initialize configuration parameters
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        # Create necessary directories specified in the configuration
        create_directories([self.config.artifacts_root])

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation 
        
        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            numerical_cols= list(config.numerical_cols),
            categorical_cols= list(config.categorical_cols)
        )
        return data_transformation_config


    def get_model_trainer_config(self) ->ModelTrainerConfig:
        # Get the model trainer configuration 
        config = self.config.model_trainer
        params = self.params.DecisionTreeRegressor
        #schema = self.schema.TARGET_COLUMN

        create_directories([config.root_dir])
        
        # Create and return the Model Trainer Config object
        model_trainer_config = ModelTrainerConfig(
            root_dir = config.root_dir,
            train_data_path = config.train_data_path,
            test_data_path = config.test_data_path,
            model_name = config.model_name,
            criterion = params.criterion,
            splitter = params.splitter,
            min_sample_split = params.min_sample_split,
            min_samples_leaf = params.min_samples_leaf,
            min_impurity_decrease = params.min_impurity_decrease,
            ccp_alpha = params.ccp_alpha,
        )

        return model_trainer_config
    

import pandas as pd 
import os 
from src.ElectricityBill import logging
from sklearn.tree import DecisionTreeRegressor
import joblib 
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from research.part_03_data_transformation import DataTransformation

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


# Pipeline 

if __name__ == "__main__":
    try:
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        data_transformation_config = config.get_data_transformation_config()

        data_transformation = DataTransformation(config=data_transformation_config)
        X_train, X_test, y_train, y_test = data_transformation.train_test_splitting()

        X_train_transformed, X_test_transformed, _, _, _ = data_transformation.initiate_data_transformation(
                X_train, X_test, y_train, y_test
            )
        
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.initiate_model_trainer(X_train_transformed, X_test_transformed, y_train, y_test)
    
    except Exception as e:
        raise e






        

    

