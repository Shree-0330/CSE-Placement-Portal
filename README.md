
## Live Demo

🚀 **Live Project:** [CSE Placement Roadmap & Mentorship Portal](https://cse-placement-app-dtlfvt2hpca4p9xe2guv3s.streamlit.app/)

Explore the live application to access placement roadmaps, track preparation tasks, assess placement readiness, interact with mentors, submit feedback, and manage job applications.

# CSE Placement Roadmap & Mentorship Portal


## Project Overview

The CSE Placement Roadmap & Mentorship Portal is a web-based application developed using Python and Streamlit. It helps students prepare for campus placements through structured learning roadmaps, mentor interaction, placement readiness assessments, and job application tracking.

The portal provides students with a centralized platform to improve their technical skills, monitor their progress, and prepare for placement opportunities.

## Features

### 1. Student Registration and Login
- Student registration and authentication.
- Access to placement preparation resources.

### 2. Placement Roadmap
- Year-wise placement preparation roadmap.
- Programming fundamentals and coding practice.
- Data Structures and Algorithms (DSA).
- Project development and documentation.
- Aptitude and logical reasoning.
- Communication skills.
- Resume and interview preparation.

### 3. Resources and Tasks
- View learning resources and preparation tasks.
- Mark tasks as completed.
- Track placement preparation progress.

### 4. Placement Readiness Assessment
- Assess coding, DSA, technical skills, projects, communication, aptitude, and resume readiness.
- Get recommendations to improve placement readiness.

### 5. Ask a Mentor
- Submit questions to mentors.
- Receive career guidance and placement preparation advice.

### 6. Student Feedback
- Rate mentor responses.
- Submit written feedback about the guidance received.

### 7. Placement Tracker
- Record job applications.
- Track application status.
- Export application records to CSV.

### 8. Mentor Dashboard
- View student questions.
- Respond to student queries.
- Review student feedback and placement outcomes.

## Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Scikit-learn
- Joblib
- GitHub
- Streamlit Community Cloud

## Project Structure

    CSE_Placement_Portal/
    │
    ├── app1.py
    ├── requirements.txt
    ├── README.md
    └── placement_portal_v4.db

Note: The database file is created or used by the application, depending on its configuration. Do not publish a database containing private student information.

## Requirements

- Python 3.10 or later
- pip
- A web browser

## Installation and Execution

### Step 1: Open the Project Folder

Open the CSE_Placement_Portal folder in Visual Studio Code.

### Step 2: Create a Virtual Environment

    python -m venv .venv

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

    .venv\Scripts\activate

### Step 4: Install Dependencies

    pip install -r requirements.txt

### Step 5: Run the Application

    streamlit run app1.py

The application will run locally at:

    http://localhost:8501

## Deployment on Streamlit Community Cloud

1. Create a GitHub repository for the project.
2. Upload app1.py, requirements.txt, README.md, and any other required application files.
3. Open https://share.streamlit.io/
4. Sign in using GitHub.
5. Select Create app.
6. Choose the project repository and the main branch.
7. Set the main file path to app1.py.
8. Click Deploy.

After successful deployment, Streamlit Community Cloud will provide a public URL for accessing the application.

## Security and Database Considerations

- Do not upload passwords, secret keys, or private student records to a public repository.
- Use secure password hashing and role-based access control.
- Restrict mentor registration and administrative access.
- SQLite files stored on Streamlit Cloud should not be treated as permanent storage.
- Use a persistent hosted database for production use.

## Future Enhancements

- Persistent cloud database integration.
- Secure authentication and role-based access.
- Email notifications for mentor responses.
- Advanced placement analytics.
- Resume analysis and recommendations.
- Job and internship listing integration.

## Conclusion

The CSE Placement Roadmap & Mentorship Portal aims to simplify placement preparation by combining learning roadmaps, task tracking, mentor guidance, student feedback, readiness assessment, and job application management in one platform.

**Project Name:** CSE Placement Roadmap & Mentorship Portal

**Framework:** Streamlit

**Programming Language:** Python

**Database:** SQLite

**Deployment Platform:** Streamlit Community Cloud
