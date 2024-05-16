from src.ElectricityBill.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.ElectricityBill.utils.commons import read_yaml, create_directories, get_size
from src.ElectricityBill.entity.configuration_entity import DataIngestionConfig


# Create a configuration manager class to manage the configurations 
class ConfigurationManager:
    def __init__(
            self,
            config_filepath = CONFIG_FILE_PATH,
            params_filepath = PARAMS_FILE_PATH,
            schema_filepath = SCHEMA_FILE_PATH
            ):
        
        # Initialize the configuration manager 
        # Read YAML configurations files to initialize configuration parameters 
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        # Create necessary directories specified in the configuration
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) ->DataIngestionConfig:
            # Get the data ingestion configuration 
            config = self.config.data_ingestion

            # Create the data ingestion configuration object 
            create_directories([config.root_dir])

            # Create and return the Data Ingestion Config object 
            data_ingestion_config = DataIngestionConfig(
                root_dir = config.root_dir,
                source_URL = config.source_URL,
                local_data_file = config.local_data_file,
                unzip_dir = config.unzip_dir
            )

            return data_ingestion_config