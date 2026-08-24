import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import joblib
import pickle
import os
import json
from datetime import datetime
import re
from difflib import SequenceMatcher

class RandomForestJobMatcher:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
        # Correct paths - remove duplicate 'models'
        self.model_path = os.path.join('models', 'saved', 'random_forest_model.pkl')
        self.scaler_path = os.path.join('models', 'saved', 'scaler.pkl')
        self.metadata_path = os.path.join('models', 'saved', 'model_metadata.json')
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Feature columns
        self.feature_columns = [
            'match_percentage', 
            'domain_match', 
            'profession_match', 
            'experience_match'
        ]
        
        # Spelling mistakes dictionary
        self.common_mistakes = {
            'pyhton': 'python', 'pythn': 'python', 'pyton': 'python',
            'javascrpt': 'javascript', 'java script': 'javascript',
            'node js': 'node.js', 'nodejs': 'node.js',
            'react js': 'react', 'reactjs': 'react',
            'anguler': 'angular', 'angular js': 'angular',
            'vue js': 'vue.js', 'vuejs': 'vue.js',
            'mongo db': 'mongodb', 'mongodb database': 'mongodb',
            'postgres': 'postgresql', 'postgre': 'postgresql',
            'my sql': 'mysql', 'mysq': 'mysql',
            'aws cloud': 'aws', 'amazon web services': 'aws',
            'azure cloud': 'azure', 'google cloud': 'gcp',
            'docker container': 'docker', 'kubernetes cluster': 'kubernetes',
            'k8s': 'kubernetes', 'ml': 'machine learning',
            'deep learning': 'deep learning', 'neural network': 'neural networks',
            'nlp': 'natural language processing', 'computer vision': 'computer vision',
            'devops': 'devops', 'dev ops': 'devops',
            'ci/cd': 'ci/cd', 'cicd': 'ci/cd',
            'front end': 'frontend', 'front-end': 'frontend',
            'back end': 'backend', 'back-end': 'backend',
            'full stack': 'fullstack', 'full-stack': 'fullstack'
        }
    
    def clean_text(self, text):
        """Clean and normalize text with spelling correction"""
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s,]', '', text)
        
        for wrong, correct in self.common_mistakes.items():
            if wrong in text:
                text = text.replace(wrong, correct)
        
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def fuzzy_match_score(self, str1, str2):
        """Calculate fuzzy matching score"""
        if not str1 or not str2:
            return 0.0
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def extract_skills(self, text):
        """Extract and clean skills"""
        if not isinstance(text, str):
            return set()
        
        text = self.clean_text(text)
        skills = re.split(r'[,;]', text)
        
        cleaned_skills = set()
        for skill in skills:
            skill = skill.strip()
            if skill and len(skill) > 1:
                cleaned_skills.add(skill)
        
        return cleaned_skills
    
    def calculate_skill_match(self, user_skills, job_skills):
        """Calculate skill match with fuzzy matching"""
        if not user_skills or not job_skills:
            return 0.0
        
        exact_matches = user_skills.intersection(job_skills)
        fuzzy_match_count = 0
        
        for user_skill in user_skills:
            for job_skill in job_skills:
                similarity = self.fuzzy_match_score(user_skill, job_skill)
                if similarity > 0.8:
                    fuzzy_match_count += 1
                    break
        
        total_job_skills = len(job_skills)
        if total_job_skills == 0:
            return 0.0
        
        exact_score = len(exact_matches) / total_job_skills
        fuzzy_score = (fuzzy_match_count / total_job_skills) * 0.7
        
        return min(1.0, exact_score + fuzzy_score)
    
    def prepare_features(self, user_data, job_data):
        """Prepare features for prediction"""
        user_skills = self.extract_skills(user_data.get('skills', ''))
        job_skills = self.extract_skills(job_data.get('required_skills', ''))
        
        skill_match = self.calculate_skill_match(user_skills, job_skills)
        
        user_domains = [
            self.clean_text(user_data.get('preferred_domain_1', '')),
            self.clean_text(user_data.get('preferred_domain_2', '')),
            self.clean_text(user_data.get('preferred_domain_3', ''))
        ]
        
        job_domain = self.clean_text(job_data.get('domain', ''))
        
        domain_match = 0
        for user_domain in user_domains:
            if user_domain and job_domain:
                if self.fuzzy_match_score(user_domain, job_domain) > 0.7:
                    domain_match = 1
                    break
        
        user_profession = self.clean_text(user_data.get('profession', ''))
        job_type = self.clean_text(job_data.get('job_type', ''))
        profession_match = 1 if user_profession == job_type else 0
        
        try:
            user_exp = float(user_data.get('experience', 0))
            job_exp = float(job_data.get('experience_required', 0))
            experience_match = 1 if user_exp >= job_exp - 1 else 0
        except:
            experience_match = 0
        
        features = {
            'match_percentage': skill_match,
            'domain_match': domain_match,
            'profession_match': profession_match,
            'experience_match': experience_match
        }
        
        return features, user_skills, job_skills
    
    def train_model(self, optimize=False):
        """Train the Random Forest model"""
        print("Loading training data...")
        
        training_file = 'data/training_data.xlsx'
        if not os.path.exists(training_file):
            from generate_datasets import generate_training_data
            generate_training_data()
        
        df = pd.read_excel(training_file)
        
        X = df[['match_percentage', 'domain_match', 'profession_match', 'experience_match']].values
        y = df['target'].values
        
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            random_state=42,
            n_jobs=-1
        )
        
        # BUG FIX: the old code fit the model on the FULL dataset first,
        # then immediately overwrote self.model by re-fitting on only the
        # 80% train split — so accuracy/f1 were reported honestly, but the
        # model that actually got pickled and saved to disk (and later used
        # for live predictions in the app) had only ever seen 80% of the data.
        # Fix: evaluate on the held-out split, then do one final fit on all
        # the data before saving, so the deployed model uses every example.
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        print(f"Model evaluated on held-out test set:")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"F1-Score: {f1:.4f}")
        
        # Final fit on 100% of the data for the model that actually ships
        self.model.fit(X_scaled, y)
        print("Final model retrained on full dataset for deployment.")
        
        self.save_model(accuracy=accuracy, f1=f1)
        
        return self.model, accuracy, f1
    
    def save_model(self, accuracy=None, f1=None):
        """Save model and scaler to .pkl files"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # BUG FIX: metadata previously listed a stale/incorrect 10-item
        # feature_columns list left over from an earlier version of this
        # file, which no longer matched the 4 features actually produced
        # by prepare_features()/generate_training_data(). Kept in sync now,
        # and accuracy/f1 are recorded so job_matching.py can display them.
        metadata = {
            'model_type': 'Random Forest',
            'timestamp': datetime.now().isoformat(),
            'model_path': self.model_path,
            'scaler_path': self.scaler_path,
            'feature_columns': self.feature_columns,
            'accuracy': accuracy,
            'f1_score': f1
        }
        
        with open(self.metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        print(f"Model saved to: {self.model_path}")
    
    def load_model(self):
        """Load model from .pkl files"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            print(f"Model loaded from: {self.model_path}")
            return True
        except FileNotFoundError:
            print("Model files not found. Training new model...")
            self.train_model()
            return True
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
    
    def predict_jobs(self, user_data, jobs_df, top_n=10):
        """Predict matching jobs for user"""
        if self.model is None:
            if not self.load_model():
                return pd.DataFrame()
        
        matching_jobs = []
        
        for _, job in jobs_df.iterrows():
            features, _, _ = self.prepare_features(user_data, job)
            
            feature_array = np.array([[
                features['match_percentage'],
                features['domain_match'],
                features['profession_match'],
                features['experience_match']
            ]])
            
            feature_scaled = self.scaler.transform(feature_array)
            
            prediction = self.model.predict(feature_scaled)[0]
            probability = self.model.predict_proba(feature_scaled)[0][1]
            
            if prediction == 1:
                job_dict = job.to_dict()
                job_dict['match_probability'] = probability
                job_dict['match_percentage'] = features['match_percentage'] * 100
                matching_jobs.append(job_dict)
        
        if matching_jobs:
            matching_jobs.sort(key=lambda x: x['match_probability'], reverse=True)
            return pd.DataFrame(matching_jobs[:top_n])
        
        return pd.DataFrame()