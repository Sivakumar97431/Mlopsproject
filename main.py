from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataValidationConfig, ModelTrainingConfig, TrainingPipelineConfig
from networksecurity.entity.config_entity import DataIngestionConfig, DataTransformationConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_transformation import DataTransformation
import sys
import warnings
warnings.filterwarnings('ignore')

if __name__=="__main__":
    try:
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config)
        logging.info("Initiated data ingestion process")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        logging.info("Completed Data ingestion Process")
        print(data_ingestion_artifact)
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data validation Completed")
        print(data_validation_artifact)
        logging.info("initiate data transformation")
        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,
                                               data_transformation_config=data_transformation_config
                                               )
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_ingestion_artifact)
        logging.info("completed data transformation")
        logging.info("Model Training stared")
        model_trainer_config=ModelTrainingConfig(training_pipeline_config)
        model_trainer=ModelTrainer(model_training_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")
    except Exception as e:
        raise NetworkSecurityException(e,sys)