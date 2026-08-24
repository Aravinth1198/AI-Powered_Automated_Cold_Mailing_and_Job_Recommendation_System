import pandas as pd
import numpy as np
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.random_forest_model import RandomForestJobMatcher
from generate_datasets import generate_jobs_dataset, generate_users_dataset, generate_training_data

def train_and_save_model():
    """Train the Random Forest model and save it as .pkl"""
    
    print("="*60)
    print("RANDOM FOREST MODEL TRAINING")
    print("="*60)
    
    # Check if data exists
    if not os.path.exists('data/training_data.xlsx'):
        print("\nGenerating training data...")
        if not os.path.exists('data/jobs.xlsx'):
            generate_jobs_dataset()
        if not os.path.exists('data/users.xlsx'):
            generate_users_dataset()
        generate_training_data()
    
    # Initialize model
    rf_model = RandomForestJobMatcher()
    
    # Train model
    print("\nTraining Random Forest model...")
    model, accuracy, f1 = rf_model.train_model(optimize=True)
    
    print("\n" + "="*60)
    print("MODEL TRAINING COMPLETE")
    print("="*60)
    print(f"Model saved successfully!")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    return model, accuracy, f1

def test_model_prediction():
    """Test the trained model with a sample user"""
    
    print("\n" + "="*60)
    print("TESTING MODEL PREDICTION")
    print("="*60)
    
    # Load model
    rf_model = RandomForestJobMatcher()
    
    if not rf_model.load_model():
        print("Model not found. Training new model...")
        train_and_save_model()
        rf_model.load_model()
    
    # Sample user data
    sample_user = {
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'profession': 'Student',
        'experience': 0,
        'preferred_domain_1': 'Data Science',
        'preferred_domain_2': 'Machine Learning',
        'preferred_domain_3': 'Software Development',
        'skills': 'Python, R, SQL, Statistics, Machine Learning, Pandas, NumPy'
    }
    
    # Load jobs
    jobs_df = pd.read_excel('data/jobs.xlsx')
    
    # Predict
    matching_jobs = rf_model.predict_jobs(sample_user, jobs_df)
    
    print(f"\nSample User: {sample_user['first_name']} {sample_user['last_name']}")
    print(f"Skills: {sample_user['skills']}")
    print(f"\nFound {len(matching_jobs)} matching jobs:")
    
    if not matching_jobs.empty:
        for i, (_, job) in enumerate(matching_jobs.head(5).iterrows(), 1):
            print(f"\n{i}. {job['job_title']} at {job['company']}")
            print(f"   Domain: {job['domain']}")
            # BUG FIX: predict_jobs() sets 'match_percentage', not 'match_score'.
            # The old key name here raised a KeyError every time this test ran.
            print(f"   Match Score: {job['match_percentage']:.2f}%")
    
    return matching_jobs

if __name__ == "__main__":
    # Train and save model
    train_and_save_model()
    
    # Test model
    test_model_prediction()