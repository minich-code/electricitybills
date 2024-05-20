from src.ElectricityBill.config.configuration import ConfigurationManager
from src.ElectricityBill.components.c_05_model_evaluation import ModelEvaluation
from src.ElectricityBill import logging 
import joblib 
import pandas as pd


PIPELINE_NAME = "MODEL EVALUATION PIPELINE"

class ModelEvaluationPipeline:
    def __init__(self):
        pass


    def main(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()

        # Load the trained model, transformed test data, and y_test data
        model = joblib.load(model_evaluation_config.model_path)
        X_test_transformed = joblib.load(model_evaluation_config.test_data_path)

        y_test_df = pd.read_csv(model_evaluation_config.test_target_variable)
        y_test = y_test_df[model_evaluation_config.target_column]

        # Create ModelEvaluation object
        model_evaluation = ModelEvaluation(config=model_evaluation_config)

        # Get predictions
        y_pred = model_evaluation.predictions(model, X_test_transformed)

        # Save evaluation results
        evaluation_results = model_evaluation.save_results(y_test, y_pred)
        return evaluation_results


if __name__=="__main__":
    try:
        logging.info(f"# ========= {PIPELINE_NAME} Started ================#")
        pipeline = ModelEvaluationPipeline()
        pipeline.main()
        logging.info(f"# ============= {PIPELINE_NAME} Terminated Successfully ! ===========\n\nx******************x") 
    except Exception as e:
        logging.exception(e)
        raise e
