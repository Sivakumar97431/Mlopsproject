import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import os,sys
import numpy as np
import pickle

def read_yaml_file(file_path: str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path: str, content: object, replace: bool =False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array_data(filepath:str,array: np.array):
    try:
        dirname=os.path.dirname(filepath)
        os.makedirs(dirname,exist_ok=True)
        with open(filepath,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
def save_object(filepath:str,object: object):
    try:
        logging.info("Entered the save_object method of MainUtils class")
        dirname=os.path.dirname(filepath)
        os.makedirs(dirname,exist_ok=True)
        with open(filepath,'wb') as obj_file:
            pickle.dump(obj=object,file=obj_file)
        logging.info("object saved successfully in mainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
def load_numpy_array_data(filepath:str):
    try:
        with open(filepath,'rb') as file:
            return np.load(filepath)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
def load_object(filepath:str):
    try:
        if not os.path.exists(filepath):
            raise Exception(f"file: {filepath} is not exists")
        with open(filepath,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
        