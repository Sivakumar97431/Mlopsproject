from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import numpy as np
import pandas as pd
import pymongo
import os
import sys
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()


MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_collection_as_dataframe(self):
        """
        Read the data from mongoDB
        """
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            
            if "_id" in df.columns.to_list():
                df=df.drop(columns=['_id'],axis=1)
                
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_dataframe_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_path=self.data_ingestion_config.feature_store_file_path
            path_dir=os.path.dirname(feature_store_path)
            os.makedirs(path_dir,exist_ok=True)
            dataframe.to_csv(feature_store_path,header=True,index=False)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            path_dir=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(path_dir,exist_ok=True)
            
            logging.info("Exporting train test file path")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,header=True,index=False
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,header=True,index=False
            )
            logging.info("Exported train test file paths")
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_dataframe_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
    