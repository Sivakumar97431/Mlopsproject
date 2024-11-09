from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,recall_score,precision_score
import sys
import os
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact

def get_classification_score(y_test,y_pred)->ClassificationMetricArtifact:
    try:
        model_f1_score=f1_score(y_test,y_pred)
        model_recall_score=recall_score(y_test,y_pred)
        model_precision_score=precision_score(y_test,y_pred)
        classification_metric=ClassificationMetricArtifact(
            f1_score=model_f1_score,
            recall_score=model_recall_score,
            precision_score=model_precision_score
        )
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)