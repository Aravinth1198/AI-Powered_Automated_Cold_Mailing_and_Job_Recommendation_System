# AI-Powered_Automated_Cold_Mailing_and_Job_Recommendation_System


## 1. Problem Statement

* Job seekers often struggle to identify suitable job opportunities and contact relevant HR professionals efficiently.
* Manually searching for matching jobs and preparing individual cold emails is time-consuming and repetitive.
* The proposed system uses ML-based job recommendation to identify relevant job roles from a database based on user-provided skills and qualifications.
* It then uses n8n automation and Gemini AI to generate and send personalized cold emails to the HR contacts of all matching jobs.
  

## 2. Proposed Solution

* Collect user information such as skills, education, experience, and preferred job role.
* Validate and process the entered user data.
* Use a Machine Learning model to identify and rank suitable job opportunities.
* Match the user with one or more relevant jobs available in the database.
* Send matched job and HR details to n8n for automated processing.
* Use Gemini AI to generate personalized cold-mail content for each matched job.
* Automatically send the generated emails to the respective HR contacts through a mail agent.
* Display job recommendations and mailing status through a user-friendly Tkinter interface.


## 3. Process Flow

```text
     Start
       ↓
 User enters information
        ↓
    Validation
        ↓
   ML recommendation
        ↓
 Multiple matching jobs
        ↓
       n8n
        ↓
      Gemini
        ↓
  Emails generated
        ↓
   Emails sent
        ↓
```


## 4. Project Mapping

| V-Model Stage        |        Auotomatic Job Recommendation Project           |
| -------------------- | -----------------------------------------------------  |
| User  Requirement    | User wants automatic job discovery and cold mailing    |
| Requirement Analysis | Tkinter + ML + database + n8n + Gemini + mail          |
| Architecture Design  | Define Python → ML → n8n → Gemini → Mail architecture  |
| Module Design        | UI, validation, ML, database, n8n modules              |
| Implementation       | Python/Tkinter/ML/n8n development                      |
| Unit Testing         | Test each Python module independently                  |
| Integration Testing  | Test Python → n8n → Gemini → Mail                      |
| System Testing       | Test complete application                              |
| Demonstration        | Verify that the system satisfies project objectives    |


## 5. Project - Modular Application Development

Create separate functions:

```python
get_applicant_info()
validate_info()
uplload_details_database()
predict_match()
recommend_job()
```


## 6. Requirement Analysis

### 6.1 Functional Requirements

The system should:
*  User information input through Tkinter
*  User input validation
*	 Store user information
*	 Maintain job database
*	 Retrieve available jobs
*	 ML-based job recommendation
*	 Calculate and rank match scores
*	 Apply matching threshold
*	 Support multiple matching jobs
*	 Retrieve HR/recruiter information
*	 Send matched-job data to n8n
*	 Process multiple jobs in n8n
*	 Generate emails using Gemini
*	 Personalize emails for each job
*	 Automatically send emails
*	 Track email status
*	 Prevent duplicate emails
*	 Handle system/API/email errors
*	 Display recommended jobs
*	 Display final mailing summary

### 6.2 Non-Functional Requirements

The application should be:

* User-friendly
* Easy to understand
* Fast in generating recommendation
* Reliable
* Maintainable
* Scalable
* Secure with respect to applicant data
* Easy to test

### 6.3 User Requirement

The user should be able to:

* Enter applicant information.
* Validate the information for analysis.
* Calculate the threshold value.
* Job similarity calculation.
* Select the job for applicant.
* Send mail to the recruiter.

### 6.4 Identify System Inputs

The initial system can use:

* Applicant Name
* Applicant Email
* Applicant Phone
* Applicant Skills
* Applicant Education
* Applicant Experience
* Applicant Preferred Job Role
* Applicant Preferred Location


