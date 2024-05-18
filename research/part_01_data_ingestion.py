from dataclasses import dataclass 
from pathlib import Path 

import os 
import urllib.request as request 
import zipfile 

# Import specific constants and utility functions 
from src.ElectricityBill.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.ElectricityBill.utils.commons import read_yaml, create_directories, get_size
from src.ElectricityBill import logging


# Entity
# Define the structure of data ingestion configuration 
@dataclass
class DataIngestionConfig:
    # Define the path to the data ingestion configuration file
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path 


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

        
# Defining the DataIngestion component class
class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config = config

    # Create a method to download a file from the specified URL 
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            # If the file does not exist locally download it 
            filename, headers = request.urlretrieve(
                    url = self.config.source_URL, 
                    filename = self.config.local_data_file
            )
            logging.info(f"Downloaded the file {filename} with the following information: \n{headers}")

        else:
            # If the file exists get the file size 
            #file_size = get_size(self.config.local_data_file)
            logging.info(f"The file exists and is of size: {get_size(Path(self.config.local_data_file))}")



        # Method to extract the zip file 
    def extract_file(self):
        # Create a directory if it does not exist 
        unzip_path = self.config.unzip_dir 
        os.makedirs(unzip_path, exist_ok=True)
        # Extract the zip file
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        logging.info(f"Extracted the file {self.config.local_data_file} to the directory {unzip_path}")

       
if __name__=="__main__":
    try:
        # Initialize configurationManager to get the configuration settings 
        config = ConfigurationManager()
        # Get the data ingestion configuration
        data_ingestion_config = config.get_data_ingestion_config()
        # Initialize the data ingestion component
        data_ingestion = DataIngestion(config = data_ingestion_config)
        # Download the file 
        data_ingestion.download_file()
        # Extract the file 
        data_ingestion.extract_file()

        logging.info("Data Ingestion Completed")

    except Exception as e:
        raise e
             
            











