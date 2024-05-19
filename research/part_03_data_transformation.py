import os 
import pandas as pd 
import numpy as np 
import joblib 
from pathlib import Path 
from dataclasses import dataclass

from src.ElectricityBill import logging
from src.ElectricityBill.utils.commons import save_object
from src.ElectricityBill.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.ElectricityBill.utils.commons import read_yaml, create_directories


from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline 
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


@dataclass 
class DataTransformationConfig:
    root_dir: Path
    data_path: Path 
    numerical_cols: list 
    categorical_cols: list 


# Class for the configuration manager 
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


# Create a class to handle the actual data transformation process 
class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config 


    def get_transformer_obj(self):
        try:
            # Separate the numeric and categorical columns 
            numerical_cols = self.config.numerical_cols
            categorical_cols = self.config.categorical_cols

            # Crete a pipeline for numeric columns 
            numeric_transformer = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )
            # Create a pipeline for categorical columns
            categorical_transformer = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent', fill_value='missing')),
                    ('onehot', OneHotEncoder(handle_unknown='ignore'))
                ]
            )
            # Combine the numeric and categorical pipelines
            preprocessor = ColumnTransformer(
                transformers=[
                    ('numerical', numeric_transformer, numerical_cols),
                    ('categorical', categorical_transformer, categorical_cols)
                ],
                remainder='passthrough'
            )

            # Return the preprocessor object 
            return preprocessor

        except Exception as e: 
            raise e 
        
    # Split the data into training and testing sets 
    def train_test_splitting(self):
        try:
            logging.info("Data Splitting process has started")

            df = pd.read_csv(self.config.data_path)
            X = df.drop(columns=["ElectricityBill"])
            y = df["ElectricityBill"]

            logging.info("Splitting data into training and testing sets")

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            logging.info("Saving the training and testing data in artifacts")
            
            # Save the target variable for both training and testing 
            y_train.to_csv(os.path.join(self.config.root_dir, "y_train.csv"), index=False)
            y_test.to_csv(os.path.join(self.config.root_dir, "y_test.csv"), index=False)
            
            # Save the training and testing data
            #X_train.to_csv(os.path.join(self.config.root_dir, "X_train.csv"), index=False)
            #X_test.to_csv(os.path.join(self.config.root_dir, "X_test.csv"), index=False)
            
            logging.info("Data Splitting process has completed")

            return X_train, X_test, y_train, y_test
        
        except Exception as e:
            raise e
        
    # Initiate data transformation 
    def initiate_data_transformation(self, X_train, X_test, y_train, y_test ):
        try:
            logging.info("Data Transformation process has started")
            
            # Get the preprocessor object
            preprocessor_obj = self.get_transformer_obj()

            # Transform the training and test data
            X_train_transformed = preprocessor_obj.fit_transform(X_train)
            X_test_transformed = preprocessor_obj.transform(X_test)

            # Save the preprocessing object 
            preprocessor_path = os.path.join(self.config.root_dir, "preprocessor_obj.joblib")
            save_object(obj=preprocessor_obj, file_path=preprocessor_path)

            # Save the transformed data as sparse matrix 
            X_train_transformed_path = os.path.join(self.config.root_dir, "X_train_transformed.joblib")
            X_test_transformed_path = os.path.join(self.config.root_dir, "X_test_transformed.joblib")
            joblib.dump(X_train_transformed, X_train_transformed_path)
            joblib.dump(X_test_transformed, X_test_transformed_path)


            logging.info("Data Transformation process has completed")


            # Return 
            return X_train_transformed, X_test_transformed, y_train, y_test, preprocessor_path 

        except Exception as e:
            raise e
        
# Pipeline 
if __name__=="__main__":
    try:
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(config = data_transformation_config)
        X_train, X_test, y_train, y_test = data_transformation.train_test_splitting()
        train_data_path, test_data_path, y_train_data_path, y_test_data_path, preprocessor_path= \
            data_transformation.initiate_data_transformation(X_train, X_test, y_train, y_test) 
        
    except Exception as e:
        logging.exception(e)
        raise e

    




        


