import os 
import urllib.request as request 
import zipfile 
from src.ElectricityBill import logging
from src.ElectricityBill.utils.commons import get_size
from src.ElectricityBill.entity.configuration_entity import DataIngestionConfig
from pathlib import Path



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
