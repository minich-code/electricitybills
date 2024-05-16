from dataclasses import dataclass 
from pathlib import Path 

# Data ingestion entity
@dataclass
class DataIngestionConfig:
    # Define the path to the data ingestion configuration file
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path 