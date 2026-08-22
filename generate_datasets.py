import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

def generate_jobs_dataset():
    """Generate comprehensive jobs dataset"""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Define job domains and their associated skills
    domains_skills = {
        'Software Development': [
            'Python, Java, C++, JavaScript, SQL, Git, Agile, REST APIs, Docker',
            'Java, Spring Boot, Microservices, AWS, Kubernetes, MySQL, Git',
            'Python, Django, PostgreSQL, Docker, CI/CD, Redis, REST APIs',
            'JavaScript, Node.js, React, MongoDB, Express, AWS, TypeScript',
            'C#, .NET Core, Azure, SQL Server, Entity Framework, Docker',
            'Python, FastAPI, PostgreSQL, Docker, Kubernetes, GraphQL, Redis',
            'Go, Microservices, gRPC, Kubernetes, Docker, PostgreSQL, AWS',
            'Ruby, Rails, PostgreSQL, Redis, Sidekiq, AWS, Docker'
        ],
        'Data Science': [
            'Python, R, SQL, Machine Learning, Statistics, Pandas, NumPy, Tableau',
            'Python, TensorFlow, PyTorch, Deep Learning, NLP, Computer Vision, AWS',
            'Python, Scikit-learn, XGBoost, Feature Engineering, A/B Testing, SQL',
            'R, Python, Statistical Modeling, Time Series Analysis, Data Visualization',
            'Python, Spark, Hadoop, Big Data, Machine Learning, SQL, AWS',
            'Python, Deep Learning, Neural Networks, Keras, TensorFlow, GPU Computing'
        ],
        'Web Development': [
            'HTML, CSS, JavaScript, React, Node.js, MongoDB, REST APIs',
            'JavaScript, TypeScript, Angular, RxJS, NgRx, SCSS, Jasmine',
            'React, Redux, Node.js, Express, PostgreSQL, Docker, AWS',
            'Vue.js, Vuex, JavaScript, CSS, HTML, REST APIs, Webpack',
            'PHP, Laravel, MySQL, JavaScript, Vue.js, Docker, Redis',
            'JavaScript, Next.js, React, Tailwind CSS, GraphQL, MongoDB'
        ],
        'Machine Learning': [
            'Python, TensorFlow, PyTorch, Deep Learning, Computer Vision, NLP',
            'Python, Scikit-learn, MLflow, Feature Store, Model Deployment, Docker',
            'Python, PyTorch, Transformers, BERT, GPT, Hugging Face, AWS',
            'Python, Reinforcement Learning, OpenAI Gym, TensorFlow, Kubernetes',
            'Python, Computer Vision, OpenCV, YOLO, TensorRT, CUDA',
            'Python, MLOps, Kubeflow, MLflow, Docker, Kubernetes, CI/CD'
        ],
        'Cloud Computing': [
            'AWS, Azure, GCP, Docker, Kubernetes, Terraform, CI/CD',
            'AWS, Lambda, API Gateway, DynamoDB, CloudFormation, Python',
            'Azure, Azure DevOps, PowerShell, ARM Templates, Docker, Kubernetes',
            'GCP, Google Kubernetes Engine, Cloud Functions, BigQuery, Python',
            'DevOps, Jenkins, Ansible, Docker, Kubernetes, AWS, Terraform',
            'AWS, ECS, EKS, Serverless, CloudWatch, IAM, Python'
        ],
        'Cybersecurity': [
            'Network Security, Penetration Testing, SIEM, Firewalls, Python, Linux',
            'Security Architecture, Risk Assessment, Compliance, ISO 27001, NIST',
            'Ethical Hacking, Vulnerability Assessment, Burp Suite, Metasploit',
            'Cloud Security, AWS Security, Azure Security, IAM, Encryption',
            'Incident Response, Digital Forensics, Malware Analysis, Python',
            'Security Operations, SOC, SIEM, Threat Hunting, Python, Splunk'
        ],
        'Mobile Development': [
            'Android, Kotlin, Java, Firebase, REST APIs, Material Design',
            'iOS, Swift, UIKit, SwiftUI, Core Data, REST APIs',
            'React Native, JavaScript, Redux, Firebase, REST APIs',
            'Flutter, Dart, Firebase, REST APIs, State Management',
            'Kotlin, Android Jetpack, Coroutines, Room Database, Retrofit',
            'Swift, iOS, Combine, SwiftUI, CoreData, Firebase'
        ],
        'DevOps': [
            'Docker, Kubernetes, Jenkins, GitLab CI, Terraform, AWS',
            'CI/CD, Jenkins, Ansible, Docker, Kubernetes, Python, Bash',
            'AWS, Terraform, Packer, Docker, Kubernetes, Monitoring',
            'Azure DevOps, PowerShell, ARM Templates, Docker, Kubernetes',
            'Site Reliability, Kubernetes, Prometheus, Grafana, Python, Go',
            'DevSecOps, Jenkins, SonarQube, Docker, Kubernetes, Security Scanning'
        ],
        'Database Administration': [
            'MySQL, PostgreSQL, Performance Tuning, Backup Recovery, Linux',
            'Oracle, PL/SQL, Database Design, Performance Tuning, RAC',
            'MongoDB, NoSQL, Redis, Database Design, Performance Optimization',
            'PostgreSQL, High Availability, Replication, Monitoring, Python',
            'SQL Server, T-SQL, SSIS, SSRS, Database Administration',
            'Cassandra, NoSQL, Distributed Systems, Data Modeling, Linux'
        ],
        'UI/UX Design': [
            'Figma, Adobe XD, User Research, Wireframing, Prototyping',
            'UI Design, Design Systems, Sketch, InVision, HTML, CSS',
            'UX Research, Usability Testing, Information Architecture, Figma',
            'Product Design, Interaction Design, Design Thinking, Figma, Adobe CC',
            'Visual Design, Branding, Typography, Figma, Adobe Creative Suite',
            'UX Design, Accessibility, User Testing, Prototyping, Figma'
        ]
    }
    
    # Define companies for each domain
    companies = {
        'Software Development': ['TechCorp', 'InnovateSoft', 'CodeMasters', 'DevGenius', 'SoftSolutions', 'AppWorks', 'ByteCraft', 'LogicLabs'],
        'Data Science': ['DataInsights', 'AnalyticsPro', 'DataMinds', 'InsightAnalytics', 'DataWorks', 'StatsCore', 'MLSolutions', 'DataDynamics'],
        'Web Development': ['WebCraft', 'SiteBuilder', 'WebGenius', 'FrontendPro', 'FullStack Inc', 'WebSolutions', 'DevStudio', 'CodeCrafters'],
        'Machine Learning': ['AI Innovations', 'MLWorks', 'DeepLearn', 'NeuralNet', 'AI Solutions', 'SmartML', 'IntelliSys', 'AI Dynamics'],
        'Cloud Computing': ['CloudTech', 'CloudWorks', 'InfraCloud', 'CloudNative', 'SkyComputing', 'CloudSys', 'VirtualCloud', 'CloudMasters'],
        'Cybersecurity': ['SecureNet', 'CyberGuard', 'SecurityPro', 'SecureWorks', 'CyberDefense', 'InfoSec', 'SecurityLabs', 'CyberShield'],
        'Mobile Development': ['AppWorks', 'MobileDev', 'AppCraft', 'MobileGenius', 'AppSolutions', 'DevMobile', 'SmartApps', 'AppMasters'],
        'DevOps': ['DevOpsPro', 'AutomateX', 'PipelineWorks', 'DevAutomation', 'OpsGenius', 'DevStream', 'AutoDeploy', 'DevOpsMasters'],
        'Database Administration': ['DataCore', 'DBAdmin', 'DataStorage', 'DBWorks', 'DatabasePro', 'DataManagement', 'DB Solutions', 'DataSystems'],
        'UI/UX Design': ['DesignStudio', 'UXWorks', 'CreativeDesign', 'DesignPro', 'UserFirst', 'DesignMasters', 'UXGenius', 'DesignWorks']
    }
    
    # Job titles for each domain
    job_titles = {
        'Software Development': [
            'Senior Software Engineer', 'Software Developer', 'Backend Developer',
            'Full Stack Developer', 'Java Developer', 'Python Developer',
            'Go Developer', 'Ruby Developer'
        ],
        'Data Science': [
            'Data Scientist', 'Senior Data Analyst', 'Machine Learning Engineer',
            'Data Engineer', 'Business Intelligence Analyst', 'Research Scientist',
            'Statistical Analyst', 'Data Science Manager'
        ],
        'Web Development': [
            'Frontend Developer', 'Full Stack Web Developer', 'React Developer',
            'Angular Developer', 'Vue.js Developer', 'PHP Developer',
            'WordPress Developer', 'UI Developer'
        ],
        'Machine Learning': [
            'ML Engineer', 'Deep Learning Engineer', 'Computer Vision Engineer',
            'NLP Engineer', 'AI Research Scientist', 'MLOps Engineer',
            'AI Engineer', 'Applied ML Scientist'
        ],
        'Cloud Computing': [
            'Cloud Architect', 'Cloud Engineer', 'AWS Solutions Architect',
            'Azure Cloud Engineer', 'GCP Cloud Engineer', 'Cloud DevOps Engineer',
            'Cloud Security Engineer', 'Cloud Infrastructure Engineer'
        ],
        'Cybersecurity': [
            'Security Engineer', 'Penetration Tester', 'Security Analyst',
            'Information Security Specialist', 'Security Architect',
            'Incident Response Analyst', 'Security Consultant', 'Ethical Hacker'
        ],
        'Mobile Development': [
            'Android Developer', 'iOS Developer', 'React Native Developer',
            'Flutter Developer', 'Mobile App Developer', 'Mobile Architect',
            'Cross-Platform Developer', 'Mobile UI Developer'
        ],
        'DevOps': [
            'DevOps Engineer', 'Site Reliability Engineer', 'Build Engineer',
            'Release Engineer', 'Infrastructure Engineer', 'Platform Engineer',
            'DevSecOps Engineer', 'Automation Engineer'
        ],
        'Database Administration': [
            'Database Administrator', 'MySQL DBA', 'PostgreSQL DBA',
            'Oracle DBA', 'MongoDB Administrator', 'Data Architect',
            'Database Developer', 'NoSQL Database Engineer'
        ],
        'UI/UX Design': [
            'UI Designer', 'UX Designer', 'Product Designer',
            'UX Researcher', 'Visual Designer', 'Interaction Designer',
            'Design Systems Designer', 'UX Architect'
        ]
    }
    
    # Generate jobs
    jobs = []
    job_id = 1
    
    for domain, skills_list in domains_skills.items():
        companies_for_domain = companies[domain]
        titles_for_domain = job_titles[domain]
        
        for i in range(30):  # 30 jobs per domain
            company = random.choice(companies_for_domain)
            job_title = random.choice(titles_for_domain)
            skills = random.choice(skills_list)
            
            # Determine experience level
            if 'Senior' in job_title or 'Architect' in job_title or 'Manager' in job_title:
                experience_required = random.randint(5, 10)
                job_type = 'Working Professional'
            elif 'Junior' in job_title or 'Entry' in job_title:
                experience_required = random.randint(0, 1)
                job_type = 'Recent Graduate'
            else:
                experience_required = random.randint(2, 5)
                job_type = random.choice(['Working Professional', 'Student', 'Recent Graduate'])
            
            # Generate HR email
            company_slug = company.lower().replace(' ', '')
            hr_email = f"hr@{company_slug}.com"
            
            job = {
                'job_id': job_id,
                'job_title': job_title,
                'company': company,
                'domain': domain,
                'required_skills': skills,
                'experience_required': experience_required,
                'job_type': job_type,
                'contact_email': hr_email,
                'posted_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            }
            
            jobs.append(job)
            job_id += 1
    
    # Create DataFrame
    jobs_df = pd.DataFrame(jobs)
    
    # Save to Excel
    os.makedirs('data', exist_ok=True)
    jobs_df.to_excel('data/jobs.xlsx', index=False)
    
    print(f"Generated {len(jobs_df)} jobs")
    print("\nJobs distribution by domain:")
    print(jobs_df['domain'].value_counts())
    
    return jobs_df

def generate_users_dataset():
    """Generate comprehensive users dataset"""
    
    np.random.seed(42)
    random.seed(42)
    
    # Define sample users with varied profiles
    users = [
        {
            'email': 'john.doe@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'profession': 'Working Professional',
            'experience': 5,
            'preferred_domain_1': 'Software Development',
            'preferred_domain_2': 'Cloud Computing',
            'preferred_domain_3': 'DevOps',
            'skills': 'Python, Java, SQL, AWS, Docker, Kubernetes, Git, REST APIs'
        },
        {
            'email': 'jane.smith@example.com',
            'password': 'password456',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'profession': 'Student',
            'experience': 0,
            'preferred_domain_1': 'Data Science',
            'preferred_domain_2': 'Machine Learning',
            'preferred_domain_3': 'Software Development',
            'skills': 'Python, R, SQL, Statistics, Machine Learning, Pandas, NumPy'
        },
        {
            'email': 'mike.johnson@example.com',
            'password': 'password789',
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'profession': 'Working Professional',
            'experience': 3,
            'preferred_domain_1': 'Web Development',
            'preferred_domain_2': 'Mobile Development',
            'preferred_domain_3': 'UI/UX Design',
            'skills': 'JavaScript, React, Node.js, HTML, CSS, MongoDB, Express'
        },
        {
            'email': 'sarah.williams@example.com',
            'password': 'password101',
            'first_name': 'Sarah',
            'last_name': 'Williams',
            'profession': 'Recent Graduate',
            'experience': 1,
            'preferred_domain_1': 'Machine Learning',
            'preferred_domain_2': 'Data Science',
            'preferred_domain_3': 'Software Development',
            'skills': 'Python, TensorFlow, PyTorch, Deep Learning, Computer Vision, NLP'
        },
        {
            'email': 'david.brown@example.com',
            'password': 'password202',
            'first_name': 'David',
            'last_name': 'Brown',
            'profession': 'Working Professional',
            'experience': 7,
            'preferred_domain_1': 'Cloud Computing',
            'preferred_domain_2': 'DevOps',
            'preferred_domain_3': 'Cybersecurity',
            'skills': 'AWS, Azure, Docker, Kubernetes, Terraform, Jenkins, CI/CD, Python'
        },
        {
            'email': 'emily.davis@example.com',
            'password': 'password303',
            'first_name': 'Emily',
            'last_name': 'Davis',
            'profession': 'Student',
            'experience': 0,
            'preferred_domain_1': 'Cybersecurity',
            'preferred_domain_2': 'Software Development',
            'preferred_domain_3': 'Cloud Computing',
            'skills': 'Network Security, Python, Linux, Penetration Testing, Firewalls'
        },
        {
            'email': 'alex.wilson@example.com',
            'password': 'password404',
            'first_name': 'Alex',
            'last_name': 'Wilson',
            'profession': 'Working Professional',
            'experience': 4,
            'preferred_domain_1': 'Mobile Development',
            'preferred_domain_2': 'Web Development',
            'preferred_domain_3': 'UI/UX Design',
            'skills': 'Android, Kotlin, Java, Firebase, React Native, JavaScript'
        },
        {
            'email': 'lisa.taylor@example.com',
            'password': 'password505',
            'first_name': 'Lisa',
            'last_name': 'Taylor',
            'profession': 'Recent Graduate',
            'experience': 0,
            'preferred_domain_1': 'Database Administration',
            'preferred_domain_2': 'Data Science',
            'preferred_domain_3': 'Software Development',
            'skills': 'MySQL, PostgreSQL, SQL, Python, Database Design, Data Modeling'
        },
        {
            'email': 'tom.anderson@example.com',
            'password': 'password606',
            'first_name': 'Tom',
            'last_name': 'Anderson',
            'profession': 'Working Professional',
            'experience': 8,
            'preferred_domain_1': 'DevOps',
            'preferred_domain_2': 'Cloud Computing',
            'preferred_domain_3': 'Software Development',
            'skills': 'Docker, Kubernetes, Jenkins, Ansible, Terraform, AWS, Python, Bash'
        },
        {
            'email': 'rachel.martin@example.com',
            'password': 'password707',
            'first_name': 'Rachel',
            'last_name': 'Martin',
            'profession': 'Student',
            'experience': 0,
            'preferred_domain_1': 'UI/UX Design',
            'preferred_domain_2': 'Web Development',
            'preferred_domain_3': 'Mobile Development',
            'skills': 'Figma, Adobe XD, HTML, CSS, JavaScript, User Research, Wireframing'
        },
        {
            'email': 'chris.garcia@example.com',
            'password': 'password808',
            'first_name': 'Chris',
            'last_name': 'Garcia',
            'profession': 'Working Professional',
            'experience': 6,
            'preferred_domain_1': 'Machine Learning',
            'preferred_domain_2': 'Data Science',
            'preferred_domain_3': 'Software Development',
            'skills': 'Python, TensorFlow, PyTorch, Scikit-learn, MLflow, Docker, Kubernetes'
        },
        {
            'email': 'amanda.martinez@example.com',
            'password': 'password909',
            'first_name': 'Amanda',
            'last_name': 'Martinez',
            'profession': 'Recent Graduate',
            'experience': 0,
            'preferred_domain_1': 'Web Development',
            'preferred_domain_2': 'Software Development',
            'preferred_domain_3': 'UI/UX Design',
            'skills': 'JavaScript, React, Vue.js, HTML, CSS, Node.js, MongoDB'
        }
    ]
    
    # Create DataFrame
    users_df = pd.DataFrame(users)
    
    # Save to Excel
    os.makedirs('data', exist_ok=True)
    users_df.to_excel('data/users.xlsx', index=False)
    
    print(f"\nGenerated {len(users_df)} users")
    print("\nUsers distribution by profession:")
    print(users_df['profession'].value_counts())
    
    return users_df

def generate_training_data():
    """Generate training data for ML models"""
    
    # Load existing data
    jobs_df = pd.read_excel('data/jobs.xlsx')
    users_df = pd.read_excel('data/users.xlsx')
    
    training_data = []
    
    for _, user in users_df.iterrows():
        user_skills = set(str(user['skills']).lower().split(','))
        user_skills = {s.strip() for s in user_skills if s.strip()}
        
        user_domains = [
            str(user['preferred_domain_1']).lower(),
            str(user['preferred_domain_2']).lower(),
            str(user['preferred_domain_3']).lower()
        ]
        
        for _, job in jobs_df.iterrows():
            job_skills = set(str(job['required_skills']).lower().split(','))
            job_skills = {s.strip() for s in job_skills if s.strip()}
            
            # Calculate match percentage
            if user_skills and job_skills:
                match_percentage = len(user_skills.intersection(job_skills)) / len(job_skills)
            else:
                match_percentage = 0
            
            # Check domain match
            job_domain = str(job['domain']).lower()
            domain_match = 1 if job_domain in user_domains else 0
            
            # Check profession match
            profession_match = 1 if str(user['profession']).lower() == str(job['job_type']).lower() else 0
            
            # Check experience match
            experience_match = 1 if user['experience'] >= job['experience_required'] else 0
            
            # Target: 1 if match percentage > 0.3 and domain matches
            target = 1 if (match_percentage > 0.3 and domain_match == 1) else 0
            
            training_data.append({
                'user_email': user['email'],
                'job_id': job['job_id'],
                'match_percentage': match_percentage,
                'domain_match': domain_match,
                'profession_match': profession_match,
                'experience_match': experience_match,
                'target': target
            })
    
    training_df = pd.DataFrame(training_data)
    
    # Save training data
    training_df.to_excel('data/training_data.xlsx', index=False)
    
    print(f"\nGenerated {len(training_df)} training samples")
    print(f"Positive samples: {training_df['target'].sum()}")
    print(f"Negative samples: {len(training_df) - training_df['target'].sum()}")
    
    return training_df

if __name__ == "__main__":
    print("Generating datasets...")
    print("\n" + "="*50)
    
    # Generate jobs
    print("\n1. Generating jobs dataset...")
    jobs_df = generate_jobs_dataset()
    
    # Generate users
    print("\n2. Generating users dataset...")
    users_df = generate_users_dataset()
    
    # Generate training data
    print("\n3. Generating training data...")
    training_df = generate_training_data()
    
    print("\n" + "="*50)
    print("All datasets generated successfully!")
    print("\nFiles created:")
    print("  - data/jobs.xlsx")
    print("  - data/users.xlsx")
    print("  - data/training_data.xlsx")