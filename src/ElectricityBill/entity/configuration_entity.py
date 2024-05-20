from dataclasses import dataclass 
from pathlib import Path 

# Data ingestion entity
@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path 

# Data validation entity 
@dataclass
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path 
    all_schema: dict

# Data Transformation Entity 

@dataclass 
class DataTransformationConfig:
    root_dir: Path
    data_path: Path 
    numerical_cols: list 
    categorical_cols: list 

# Model Trainer Entity 
@dataclass
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    # DecisionTreeRegressor Parameter 
    criterion: str
    splitter: str 
    min_sample_split: int
    min_samples_leaf: int
    min_impurity_decrease: float
    ccp_alpha: float