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
