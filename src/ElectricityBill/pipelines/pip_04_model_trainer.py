from src.ElectricityBill.config.configuration import ConfigurationManager
from src.ElectricityBill.components.c_03_data_transformation import DataTransformation
from src.ElectricityBill.components.c_04_model_trainer import ModelTrainer
from src.ElectricityBill import logging 


PIPELINE_NAME = "MODEL TRAINER PIPELINE"

class ModelTrainerPipeline:
    def __init__(self):
        pass


    def main(self):
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


if __name__=="__main__":
    try:
        logging.info(f"# ========= {PIPELINE_NAME} Started ================#")
        pipeline = ModelTrainerPipeline()
        pipeline.main()
        logging.info(f"# ============= {PIPELINE_NAME} Terminated Successfully ! ===========\n\nx******************x") 
    except Exception as e:
        logging.exception(e)
        raise e