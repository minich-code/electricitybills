from src.ElectricityBill.config.configuration import ConfigurationManager
from src.ElectricityBill.components.c_02_data_validation import DataValidation
from src.ElectricityBill import logging 


PIPELINE_NAME = "DATA VALIDATION PIPELINE"

class DataValidationPipeline:
    def __init__(self):
        pass 

    def main(self):
  
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config = data_validation_config)
        data_validation.validate_columns()
        data_validation.validate_data_types()

if __name__=="__main__":
    try:
        logging.info(f"# ========= {PIPELINE_NAME} Started ================#")
        pipeline = DataValidationPipeline()
        pipeline.main()
        logging.info(f"# ============= {PIPELINE_NAME} Terminated Successfully ! ==============\n\nx****************************x")
    
    except Exception as e:
        raise e

