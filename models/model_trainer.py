import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

from models.data_preprocessing import DataPreprocessor

class ModelTrainer:
    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Logistic Regression': LogisticRegression(random_state=42),
            'SVM': SVC(kernel='rbf', random_state=42, probability=True),
            'KNN': KNeighborsClassifier(n_neighbors=5),
            'Naive Bayes': GaussianNB(),
            'Decision Tree': DecisionTreeClassifier(random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42)
        }
        self.best_model = None
        self.best_model_name = None
        self.best_accuracy = 0
    
    def train_all_models(self):
        """Train all models and select the best one"""
        # Load and preprocess data
        users_df, jobs_df = self.preprocessor.load_data()
        training_data = self.preprocessor.create_training_data(users_df, jobs_df)
        
        if training_data.empty:
            # If no training data, use default model
            self.best_model = RandomForestClassifier()
            self.best_model_name = 'Random Forest'
            self.best_accuracy = 100
            return
        
        # Prepare features
        X, y = self.preprocessor.preprocess_features(training_data)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train and evaluate each model
        results = {}
        for name, model in self.models.items():
            try:
                # Train model
                model.fit(X_train, y_train)
                
                # Predict
                y_pred = model.predict(X_test)
                
                # Calculate accuracy
                accuracy = accuracy_score(y_test, y_pred) * 100
                
                # Cross-validation score
                cv_scores = cross_val_score(model, X, y, cv=5)
                cv_mean = cv_scores.mean() * 100
                
                results[name] = {
                    'model': model,
                    'accuracy': accuracy,
                    'cv_score': cv_mean
                }
                
                print(f"{name}: Accuracy={accuracy:.2f}%, CV Score={cv_mean:.2f}%")
                
            except Exception as e:
                print(f"Error training {name}: {str(e)}")
        
        # Select best model based on CV score
        if results:
            best_name = max(results, key=lambda x: results[x]['cv_score'])
            self.best_model = results[best_name]['model']
            self.best_model_name = best_name
            self.best_accuracy = results[best_name]['accuracy']
            
            # Save best model
            self.save_model()
    
    def train_and_predict(self, user_data):
        """Train models and predict matching jobs for a user"""
        # Train models if not already trained
        if self.best_model is None:
            self.train_all_models()
        
        # Load jobs data
        _, jobs_df = self.preprocessor.load_data()
        
        # Find matching jobs
        matching_jobs = []
        
        for _, job in jobs_df.iterrows():
            # Prepare features for this user-job pair
            features = self.preprocessor.prepare_user_features(user_data, job)
            
            # Scale features if scaler is fitted
            if hasattr(self.preprocessor.scaler, 'mean_'):
                features_scaled = self.preprocessor.scaler.transform(features)
            else:
                features_scaled = features.values
            
            # Predict
            try:
                prediction = self.best_model.predict(features_scaled)
                if prediction[0] == 1:
                    matching_jobs.append(job)
            except:
                # If prediction fails, use simple matching
                if self.simple_match(user_data, job):
                    matching_jobs.append(job)
        
        if matching_jobs:
            matching_jobs_df = pd.DataFrame(matching_jobs)
        else:
            matching_jobs_df = pd.DataFrame()
        
        return self.best_model_name, self.best_accuracy, matching_jobs_df
    
    def simple_match(self, user_data, job_data):
        """Simple matching algorithm as fallback"""
        user_skills = set(str(user_data.get('skills', '')).lower().split(','))
        user_skills = {s.strip() for s in user_skills if s.strip()}
        
        job_skills = set(str(job_data.get('required_skills', '')).lower().split(','))
        job_skills = {s.strip() for s in job_skills if s.strip()}
        
        if user_skills and job_skills:
            match_percentage = len(user_skills.intersection(job_skills)) / len(job_skills)
            return match_percentage > 0.5
        
        return False
    
    def save_model(self):
        """Save the best model to disk"""
        if self.best_model is not None:
            os.makedirs('models/saved', exist_ok=True)
            joblib.dump(self.best_model, 'models/saved/best_model.joblib')
            joblib.dump(self.preprocessor.scaler, 'models/saved/scaler.joblib')
    
    def load_model(self):
        """Load the best model from disk"""
        try:
            self.best_model = joblib.load('models/saved/best_model.joblib')
            self.preprocessor.scaler = joblib.load('models/saved/scaler.joblib')
            return True
        except:
            return False