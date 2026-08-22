import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

class KNNModel:
    def __init__(self):
        self.model = KNeighborsClassifier(
            n_neighbors=5,
            weights='distance',
            metric='minkowski'
        )
        self.model_name = "K-Nearest Neighbors"
    
    def train(self, X, y):
        """Train the KNN model"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        cv_scores = cross_val_score(self.model, X, y, cv=5)
        
        return {
            'model': self.model,
            'accuracy': accuracy,
            'cv_scores': cv_scores,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
    
    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)