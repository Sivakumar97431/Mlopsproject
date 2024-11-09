import os
import sys

from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.entity.artifact_entity import ModelTrainerArtifact

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact
from networksecurity.entity.config_entity import ModelTrainingConfig

from networksecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models,load_object,save_object
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score


class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
                 model_training_config:ModelTrainingConfig
                 ):
        try:
            self.data_transformation_artifact=data_transformation_artifact
            self.model_training_config=model_training_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def train_model(self,X_train,y_train,X_test,y_test):
        try:
            models = {
                    "Random Forest": RandomForestClassifier(verbose=1),
                    "Decision Tree": DecisionTreeClassifier(),
                    "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                    "Logistic Regression": LogisticRegression(verbose=1),
                    "AdaBoost": AdaBoostClassifier(),
                }
            params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            model_report: dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,param=params)
            
            best_model_score=max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            
            y_train_pred=best_model.predict(X_train)
            classification_train_metric=get_classification_score(y_train,y_train_pred)
            
            y_test_pred=best_model.predict(X_test)
            classification_test_metric=get_classification_score(y_test,y_test_pred)
            
            
            preprocessor=load_object(filepath=self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir_path=os.path.dirname(self.model_training_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            Network_model=NetworkModel(preprocess=preprocessor,model=best_model)
            
            save_object(filepath=self.model_training_config.trained_model_file_path,object=Network_model)
            
            model_trainer_artifact=ModelTrainerArtifact(
                trained_model_file_path=self.model_training_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            logging.info(f"model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path
            
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)
            
            X_train,y_train,X_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            
            model_trainer_artifact=self.train_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
            
        