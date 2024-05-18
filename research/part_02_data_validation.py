from dataclasses import dataclass
from pathlib import Path

from src.ElectricityBill.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.ElectricityBill.utils.commons import read_yaml, create_directories, get_size
from src.ElectricityBill import logging

import os 
import pandas as pd 


# Defining the structure of data validation configuration using a data class
@dataclass
class DataValidationConfig:
    # Define the path to the data validation configuration file
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path 
    all_schema: dict

# Create a configuration manager class to manage the configuration 
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
    

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config 
    
    # Method to validate all columns of the dataset against the specified schema 
    def validate_columns(self) -> bool:
        try:
            validation_status = None
            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)

            all_schema = self.config.all_schema.keys()

            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    logging.error(f"Column {col} is not present in the schema")

                    # Write validation status to the status file 
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(str(validation_status))
                    return validation_status
                
                else:
                    validation_status = True
                    logging.info(f"Column {col} is present in the schema")
                    
                    # Write validation status to the status file
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(str(validation_status))
                    return validation_status

            return validation_status
        
        except Exception as e:
            raise e
        
    # Method to validate the data types of all columns 
    def validate_data_types(self) -> bool:
        try:
            validation_status = None
            # Read the csv file 
            data = pd.read_csv(self.config.unzip_data_dir)
            # Get all column names and their corresponding data types from the schema
            all_cols = list(data.columns)

                # Check if the data types of columns in the dataset match those specified in the schema
            for col in all_cols:
                if data[col].dtype!= self.config.all_schema[col]:
                    validation_status = False
                    logging.error(f"Data type of column {col} does not match the schema")
                    
                    # Write validation status to the status file
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(str(validation_status))
                    return validation_status
                
                else:
                    validation_status = True
                    logging.info(f"Data type of column {col} matches the schema")

                    # Write validation status to the status file
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(str(validation_status))
            return validation_status
        
        except Exception as e:
            raise e

# Pipeline 
if __name__ =="__main__":
    try:
        # Initialize configuration manager 
        config = ConfigurationManager()
        # Get the data validation configuration 
        data_validation_config = config.get_data_validation_config()
        # Initialize the data validation component
        data_validation = DataValidation(config = data_validation_config)
        # Validate all columns of the dataset against the specified schema 
        data_validation.validate_columns()
        # Validate the data types of all columns 
        data_validation.validate_data_types()
        logging.info("Data Validation Completed") 
    except Exception as e:
        raise e




    