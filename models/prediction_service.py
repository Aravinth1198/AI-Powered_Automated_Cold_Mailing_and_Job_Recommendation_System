import pandas as pd
import numpy as np
import pickle
import os
import json

class PredictionService:
    """Service for loading model and making predictions"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_metadata = None
        
        # Correct paths
        self.model_path = os.path.join('models', 'saved', 'random_forest_model.pkl')
        self.scaler_path = os.path.join('models', 'saved', 'scaler.pkl')
        self.metadata_path = os.path.join('models', 'saved', 'model_metadata.json')
    
    def load_model(self):
        """Load the saved model, scaler, and metadata"""
        try:
            if not os.path.exists(self.model_path):
                print("Model not found. Training new model...")
                from models.random_forest_model import RandomForestJobMatcher
                rf_model = RandomForestJobMatcher()
                rf_model.train_model()
            
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, 'r') as f:
                    self.model_metadata = json.load(f)
            
            print("Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def prepare_features(self, user_data, job_data):
        """Prepare features for prediction"""
        # Simple skill extraction
        user_skills = self._extract_skills(user_data.get('skills', ''))
        job_skills = self._extract_skills(job_data.get('required_skills', ''))
        
        # Calculate match percentage
        if user_skills and job_skills:
            match_percentage = len(user_skills.intersection(job_skills)) / len(job_skills)
        else:
            match_percentage = 0
        
        # Domain match
        user_domains = [
            str(user_data.get('preferred_domain_1', '')).lower(),
            str(user_data.get('preferred_domain_2', '')).lower(),
            str(user_data.get('preferred_domain_3', '')).lower()
        ]
        job_domain = str(job_data.get('domain', '')).lower()
        domain_match = 1 if job_domain in user_domains else 0
        
        # Profession match
        profession_match = 1 if str(user_data.get('profession', '')).lower() == str(job_data.get('job_type', '')).lower() else 0
        
        # Experience match
        try:
            user_exp = float(user_data.get('experience', 0))
            job_exp = float(job_data.get('experience_required', 0))
            experience_match = 1 if user_exp >= job_exp else 0
        except:
            experience_match = 0
        
        return np.array([[match_percentage, domain_match, profession_match, experience_match]])
    
    def predict_jobs(self, user_data, jobs_df, top_n=10):
        """Predict matching jobs for a user"""
        if self.model is None:
            if not self.load_model():
                return pd.DataFrame()
        
        predictions = []
        
        for _, job in jobs_df.iterrows():
            features = self.prepare_features(user_data, job)
            features_scaled = self.scaler.transform(features)
            
            prediction = self.model.predict(features_scaled)[0]
            probability = self.model.predict_proba(features_scaled)[0][1]
            
            if prediction == 1:
                job_dict = job.to_dict()
                job_dict['match_probability'] = probability
                job_dict['match_percentage'] = features[0][0] * 100
                predictions.append(job_dict)
        
        if predictions:
            predictions_df = pd.DataFrame(predictions)
            predictions_df = predictions_df.sort_values('match_probability', ascending=False)
            return predictions_df.head(top_n)
        
        return pd.DataFrame()
    
    def _extract_skills(self, text):
        """Extract skills from text"""
        if not isinstance(text, str):
            return set()
        skills = [s.strip().lower() for s in text.split(',') if s.strip()]
        return set(skills)