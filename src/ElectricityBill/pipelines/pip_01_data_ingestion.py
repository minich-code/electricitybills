from src.ElectricityBill.config.configuration import ConfigurationManager
from src.ElectricityBill.components.c_01_data_ingestion import DataIngestion
from src.ElectricityBill import logging 


PIPELINE_NAME = "DATA INGESTION PIPELINE"

class DataIngestionPipeline:
    def __init__(self):
        pass 

    def main(self):
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

if __name__=="__main__":
    try:
        logging.info(f"# ========= {PIPELINE_NAME} Started ================")
        pipeline = DataIngestionPipeline()
        pipeline.main()
        logging.info(f"# ============= {PIPELINE_NAME} Terminated Successfully ! ==============\n\nx**************x")
    except Exception as e:
        raise e
