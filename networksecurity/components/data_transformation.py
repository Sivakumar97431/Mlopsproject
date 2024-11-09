import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import (
    DataValidationArtifact,
    DataTransformationArtifact
)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(filepath:str)->pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def get_data_transformer_object(cls)->Pipeline:
        try:
            logging.info("Entered Datatranformation class to transform the data")
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"initiated the KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS} args")
            processor:Pipeline=Pipeline([('imputer',imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered into the the initiate data transformation method in DataTransformaion class")
        try:
            logging.info("starting data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ## training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            
            ## testing dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            
            preprocesser=self.get_data_transformer_object()
            preprocessor_object=preprocesser.fit(input_feature_train_df)
            transformed_input_train_feature=preprocesser.transform(input_feature_train_df)
            transformed_input_test_feature=preprocesser.transform(input_feature_test_df)
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_arr = np.c_[ transformed_input_test_feature, np.array(target_feature_test_df) ]
            
            #save numpy array data
            save_numpy_array_data(self.data_transformation_config.data_transformed_train_file_path,
                                  train_arr
                                  )
            save_numpy_array_data(self.data_transformation_config.data_transformed_test_file_path,
                                  test_arr
                                  )
            save_object(self.data_transformation_config.data_transformed_object_file_path,
                        preprocessor_object
                        )
            data_transform_artifact=DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.data_transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.data_transformed_object_file_path
            )
            return data_transform_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
            
            
        
    
