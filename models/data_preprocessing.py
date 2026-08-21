import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import os

class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.tfidf = TfidfVectorizer(max_features=100)
    
    def load_data(self):
        """Load user and job data from Excel files"""
        users_file = 'data/users.xlsx'
        jobs_file = 'data/jobs.xlsx'
        
        users_df = pd.read_excel(users_file)
        jobs_df = pd.read_excel(jobs_file)
        
        return users_df, jobs_df
    
    def create_training_data(self, users_df, jobs_df):
        """Create training data by matching users with jobs"""
        training_data = []
        
        for _, user in users_df.iterrows():
            user_skills = set(str(user.get('skills', '')).lower().split(','))
            user_skills = {s.strip() for s in user_skills if s.strip()}
            
            for _, job in jobs_df.iterrows():
                job_skills = set(str(job.get('required_skills', '')).lower().split(','))
                job_skills = {s.strip() for s in job_skills if s.strip()}
                
                # Calculate skill match percentage
                if user_skills and job_skills:
                    match_percentage = len(user_skills.intersection(job_skills)) / len(job_skills)
                else:
                    match_percentage = 0
                
                # Check if domains match
                user_domains = [
                    str(user.get('preferred_domain_1', '')).lower(),
                    str(user.get('preferred_domain_2', '')).lower(),
                    str(user.get('preferred_domain_3', '')).lower()
                ]
                job_domain = str(job.get('domain', '')).lower()
                
                domain_match = 1 if job_domain in user_domains else 0
                
                # Target: 1 if match percentage > 0.5 and domain matches
                target = 1 if (match_percentage > 0.5 and domain_match == 1) else 0
                
                training_data.append({
                    'match_percentage': match_percentage,
                    'domain_match': domain_match,
                    'profession_match': 1 if str(user.get('profession', '')).lower() == str(job.get('job_type', '')).lower() else 0,
                    'experience_match': 1 if user.get('experience', 0) >= job.get('experience_required', 0) else 0,
                    'target': target
                })
        
        return pd.DataFrame(training_data)
    
    def preprocess_features(self, df):
        """Preprocess features for ML models"""
        features = df.drop('target', axis=1)
        target = df['target']
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        return features_scaled, target
    
    def prepare_user_features(self, user_data, job_data):
        """Prepare features for a single user-job pair"""
        user_skills = set(str(user_data.get('skills', '')).lower().split(','))
        user_skills = {s.strip() for s in user_skills if s.strip()}
        
        job_skills = set(str(job_data.get('required_skills', '')).lower().split(','))
        job_skills = {s.strip() for s in job_skills if s.strip()}
        
        # Calculate match percentage
        if user_skills and job_skills:
            match_percentage = len(user_skills.intersection(job_skills)) / len(job_skills)
        else:
            match_percentage = 0
        
        # Check domain match
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
        experience_match = 1 if user_data.get('experience', 0) >= job_data.get('experience_required', 0) else 0
        
        features = pd.DataFrame({
            'match_percentage': [match_percentage],
            'domain_match': [domain_match],
            'profession_match': [profession_match],
            'experience_match': [experience_match]
        })
        
        return features