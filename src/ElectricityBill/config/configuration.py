from src.ElectricityBill.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.ElectricityBill.utils.commons import read_yaml, create_directories, get_size
from pathlib import Path 
from src.ElectricityBill.entity.configuration_entity import (DataIngestionConfig, DataValidationConfig,
                                                             DataTransformationConfig, ModelTrainerConfig,
                                                             ModelEvaluationConfig) 


# Create a configuration manager class to manage the configurations 
class ConfigurationManager:
    def __init__(
            self,
            config_filepath = CONFIG_FILE_PATH,
            params_filepath = PARAMS_FILE_PATH,
            schema_filepath = SCHEMA_FILE_PATH
            ):
        
        # Initialize the configuration manager 
        # Read YAML configurations files to initialize configuration parameters 
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        # Create necessary directories specified in the configuration
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) ->DataIngestionConfig:
            # Get the data ingestion configuration 
            config = self.config.data_ingestion

            # Create the data ingestion configuration object 
            create_directories([config.root_dir])

            # Create and return the Data Ingestion Config object 
            data_ingestion_config = DataIngestionConfig(
                root_dir = config.root_dir,
                source_URL = config.source_URL,
                local_data_file = config.local_data_file,
                unzip_dir = config.unzip_dir
            )

            return data_ingestion_config
# Data Validation Config   
    def get_data_validation_config(self) ->DataValidationConfig:
        # Get the data validation configuration 
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])
        # Create and return the Data Validation Config object
        data_validation_config = DataValidationConfig(
            root_dir = config.root_dir,
            STATUS_FILE = config.STATUS_FILE,
            unzip_data_dir = config.unzip_data_dir,
            all_schema = schema
        )
        return data_validation_config

 # Data Transformation Config   

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
    
# Model Trainer config
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
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        params = self.params.DecisionTreeRegressor
        schema = self.schema.TARGET_COLUMN

        create_directories([config.root_dir])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            test_data_path=config.test_data_path,
            test_target_variable= config.test_target_variable,
            model_path = config.model_path,
            all_params=params,
            metric_file_name = config.metric_file_name,
            target_column = schema.name
           
        )

        return model_evaluation_config
