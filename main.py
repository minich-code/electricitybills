from src.ElectricityBill import logging
from src.ElectricityBill.pipelines.pip_01_data_ingestion import DataIngestionPipeline



COMPONENT_NAME = "Data Ingestion Component"
try:
    logging.info(f"# ========= {COMPONENT_NAME} Started ================")
    pipeline = DataIngestionPipeline()
    pipeline.main()
    logging.info(f"# ============= {COMPONENT_NAME} Terminated Successfully ! ==============\n\nx**************x")
except Exception as e:
    logging.exception(e)
    raise e