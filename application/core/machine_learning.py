# 
# core/machine_learning.py
#
# Author: Mihai Ionut Deaconu
#

import pandas as pd
import numpy as np
import operator
import joblib
from sklearn.feature_selection import SelectFromModel
from django.conf import settings

def select_genes_svm(classifier, data):
  # Load the model and data files
  clf = joblib.load(settings.MEDIA_ROOT + str(classifier))
  data = pd.read_csv(settings.MEDIA_ROOT + str(data))
  data.set_index("Unnamed: 0", inplace=True)
  
  # Load the features with corresponding weights in feature_importance
  genes = list(data.columns.values)
  coef_dict = dict(zip(genes, clf.coef_.T))
  feature_importance = dict()
  for key, item in coef_dict.items():
      if item.any():
          feature_importance[key] = item[0]
        
  # Sort the list and keep only the feature names
  selected_genes = sorted(feature_importance.items(), key=operator.itemgetter(1))
  selected_genes.reverse()
  selected_genes = [x[0] for x in selected_genes]

  return selected_genes

def select_genes_rf(classifier, data):
  # Load the model and data files
  clf = joblib.load(settings.MEDIA_ROOT + str(classifier))
  data = pd.read_csv(settings.MEDIA_ROOT + str(data))
  data.set_index("Unnamed: 0", inplace=True)

  # Load the features with corresponding weights in feature_importance
  importances = clf.feature_importances_
  feature_importance = dict()
  for i in range(data.shape[1]):
      if importances[i] > 0:
        feature_importance[data.columns[i]] = importances[i]
        
  # Sort the list and keep only the feature names
  selected_genes = sorted(feature_importance.items(), key=operator.itemgetter(1))
  selected_genes.reverse()
  selected_genes = [x[0] for x in selected_genes]

  return selected_genes