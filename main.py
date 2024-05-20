from src.ElectricityBill import logging
from src.ElectricityBill.pipelines.pip_01_data_ingestion import DataIngestionPipeline
from src.ElectricityBill.pipelines.pip_02_data_validation import DataValidationPipeline
from src.ElectricityBill.pipelines.pip_03_data_transformation import DataTransformationPipeline
from src.ElectricityBill.pipelines.pip_04_model_trainer import ModelTrainerPipeline



COMPONENT_NAME = "Data Ingestion Component"
try:
    logging.info(f"# ============= {COMPONENT_NAME} Started ====================#")
    pipeline = DataIngestionPipeline()
    pipeline.main()
    logging.info(f"# ============= {COMPONENT_NAME} Terminated Successfully ! ======================\n\nx*****************************x")
except Exception as e:
    logging.exception(e)
    raise e


COMPONENT_NAME = "Data Validation Component"
try:
    logging.info(f"# =============== {COMPONENT_NAME} Started ===================#")
    pipeline = DataValidationPipeline()
    pipeline.main()
    logging.info(f"# ============= {COMPONENT_NAME} Terminated Successfully ! ========================#\n\nx***************************x")
except Exception as e:
    logging.exception(e)
    raise e


COMPONENT_NAME = "Data Transformation Component"
try:
    logging.info(f"# ================ {COMPONENT_NAME} Started ===================#")
    pipeline = DataTransformationPipeline()
    pipeline.main()
    logging.info(f"# ============= {COMPONENT_NAME} Terminated Successfully ! =======================#\n\nx****************************x")
except Exception as e:
    logging.exception(e)
    raise e


COMPONENT_NAME = "Model trainer Component"
try:
    logging.info(f"# ================ {COMPONENT_NAME} Started ===================#")
    pipeline = ModelTrainerPipeline()
    pipeline.main()
    logging.info(f"# ============= {COMPONENT_NAME} Terminated Successfully ! =======================#\n\nx****************************x")
except Exception as e:
    logging.exception(e)
    raise e


