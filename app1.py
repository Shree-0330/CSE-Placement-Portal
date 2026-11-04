
from pathlib import Path
import os
import sqlite3
import hashlib
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import streamlit as st

# ============================================================
# CSE PLACEMENT ROADMAP & ML MENTORSHIP PORTAL
# Python + Streamlit + Random Forest + SQLite
# ============================================================

st.set_page_config(
    page_title="CSE Placement Roadmap & Mentorship Portal",
    page_icon="🎓",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("PORTAL_DB_PATH", str(BASE_DIR / "placement_portal_v4.db")))
MODEL_PATH = BASE_DIR / "placement_model.pkl"
ENCODER_PATH = BASE_DIR / "label_encoder.pkl"

FEATURE_COLUMNS = [
    "Year",
    "Coding_Score",
    "DSA_Score",
    "Technical_Skills",
    "Projects_Score",
    "Communication_Score",
    "Aptitude_Score",
    "Internship_Experience",
    "Resume_Score",
]

YEARS = ["First Year", "Second Year", "Third Year", "Final Year"]

YEAR_NUMBER = {
    name: index for index, name in enumerate(YEARS, start=1)
}

STATUSES = [
    "Applied",
    "Online Assessment",
    "Interview Scheduled",
    "Interview Completed",
    "Selected",
    "Rejected",
    "Offer Received",
]

ROADMAP = {
    "First Year": {
        "Programming": [
            "Programming fundamentals",
            "Python / Java programming practice",
            "Basic coding problems",
        ],
        "DSA": [
            "Arrays and Strings practice",
            "Linked List problems",
            "Stack and Queue problems",
            "Trees and Graphs practice",
        ],
        "Projects": [
            "Project documentation",
            "GitHub project development",
            "Mini project implementation",
        ],
        "Aptitude": [
            "Quantitative aptitude",
            "Logical reasoning",
            "Verbal ability",
        ],
        "Communication": [
            "Communication practice",
            "Group discussion preparation",
            "Interview introduction practice",
        ],
        "Placement": [
            "Resume preparation",
            "Technical interview preparation",
            "HR interview preparation",
        ],
    },

    "Second Year": {
        "Programming": [
            "Object-oriented programming",
            "SQL and DBMS practice",
            "JavaScript programming practice",
        ],
        "DSA": [
            "Linked List problems",
            "Stack and Queue problems",
            "Recursion and Hashing",
            "Searching and Sorting",
        ],
        "Projects": [
            "CRUD application development",
            "Database project development",
            "Project documentation",
        ],
        "Aptitude": [
            "Quantitative aptitude",
            "Logical reasoning",
            "Verbal ability",
        ],
        "Communication": [
            "Presentation practice",
            "Group discussion practice",
            "Interview introduction practice",
        ],
        "Placement": [
            "Resume preparation",
            "Internship applications",
            "Technical interview preparation",
        ],
    },

    "Third Year": {
        "Programming": [
            "Advanced programming practice",
            "Operating Systems",
            "Computer Networks",
            "Database Management Systems",
        ],
        "DSA": [
            "Trees and Graphs",
            "Dynamic Programming",
            "Advanced coding problems",
        ],
        "Projects": [
            "Major project implementation",
            "GitHub project development",
            "Project documentation",
        ],
        "Aptitude": [
            "Advanced quantitative aptitude",
            "Logical reasoning tests",
            "Verbal ability practice",
        ],
        "Communication": [
            "Technical presentation",
            "Group discussion preparation",
            "Interview communication practice",
        ],
        "Placement": [
            "Resume preparation",
            "Technical interview preparation",
            "Mock interview practice",
        ],
    },

    "Final Year": {
        "Programming": [
            "Core programming revision",
            "SQL and DBMS revision",
            "Company-specific coding practice",
        ],
        "DSA": [
            "Arrays and Strings revision",
            "Trees and Graphs revision",
            "Advanced coding problems",
        ],
        "Projects": [
            "Final year project implementation",
            "Project documentation",
            "GitHub portfolio preparation",
        ],
        "Aptitude": [
            "Quantitative aptitude revision",
            "Logical reasoning tests",
            "Verbal ability revision",
        ],
        "Communication": [
            "Group discussion practice",
            "Self-introduction practice",
            "HR interview communication",
        ],
        "Placement": [
            "Resume preparation",
            "Technical interview preparation",
            "HR interview preparation",
            "Placement application tracking",
        ],
    },
}


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH, timeout=30)


def query(sql, params=(), one=False):
    with db() as con:
        con.row_factory = sqlite3.Row
        cursor = con.execute(sql, params)
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]

    return (result[0] if result else None) if one else result


def execute(sql, params=()):
    with db() as con:
        con.execute(sql, params)
        con.commit()


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def password_hash(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def setup_database():
    with db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            academic_year TEXT DEFAULT 'First Year',
            branch TEXT DEFAULT 'CSE',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            task_key TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            UNIQUE(student_id, task_key)
        );

        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            topic TEXT DEFAULT '',
            answer TEXT DEFAULT '',
            mentor_id INTEGER,
            asked_at TEXT NOT NULL,
            answered_at TEXT
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER UNIQUE NOT NULL,
            student_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            notes TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            coding INTEGER NOT NULL,
            aptitude INTEGER NOT NULL,
            dsa INTEGER NOT NULL,
            internship TEXT NOT NULL,
            technical INTEGER NOT NULL,
            resume INTEGER NOT NULL,
            projects INTEGER NOT NULL,
            communication INTEGER NOT NULL,
            score INTEGER NOT NULL,
            result TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)

        con.commit()


def create_default_mentor():
    username = os.getenv(
        "PORTAL_MENTOR_USERNAME",
        "mentor"
    )

    password = os.getenv(
        "PORTAL_MENTOR_PASSWORD",
        "Mentor@123"
    )

    existing = query(
        "SELECT id FROM users WHERE username=?",
        (username,),
        one=True
    )

    if not existing:
        execute(
            """
            INSERT INTO users
            (username, password_hash, full_name, role, created_at)
            VALUES (?, ?, ?, 'mentor', ?)
            """,
            (
                username,
                password_hash(password),
                "Placement Mentor",
                timestamp(),
            )
        )


# ============================================================
# MACHINE LEARNING MODEL
# ============================================================

@st.cache_resource
def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "placement_model.pkl is missing from the GitHub repository."
        )

    if not ENCODER_PATH.exists():
        raise FileNotFoundError(
            "label_encoder.pkl is missing from the GitHub repository."
        )

    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)

    if getattr(model, "n_features_in_", None) != len(FEATURE_COLUMNS):
        raise ValueError(
            "The ML model does not have the expected 9 input features."
        )

    return model, encoder


def year_value(user):

    return YEAR_NUMBER.get(
        user.get("academic_year", "First Year"),
        1
    )


def ml_predict(
    user,
    coding,
    dsa,
    technical,
    projects,
    communication,
    aptitude,
    internship,
    resume
):

    model, encoder = load_model()

    features = pd.DataFrame(
        [{
            "Year": year_value(user),
            "Coding_Score": int(coding),
            "DSA_Score": int(dsa),
            "Technical_Skills": int(technical),
            "Projects_Score": int(projects),
            "Communication_Score": int(communication),
            "Aptitude_Score": int(aptitude),
            "Internship_Experience": (
                1 if internship == "Yes" else 0
            ),
            "Resume_Score": int(resume),
        }],
        columns=FEATURE_COLUMNS
    )

    prediction_code = int(
        model.predict(features)[0]
    )

    prediction = str(
        encoder.inverse_transform(
            [prediction_code]
        )[0]
    )

    confidence = None

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(features)[0]
        confidence = float(np.max(probabilities)) * 100

    return prediction, confidence


# ============================================================
# COMMON UI FUNCTION
# ============================================================

def page_header(title, subtitle):

    st.title(title)
    st.caption(subtitle)
    st.divider()


# ============================================================
# LOGIN AND REGISTRATION
# ============================================================

def login_page():

    st.title(
        "🎓 CSE Placement Roadmap & Mentorship Portal"
    )

    st.write(
        "Learn, practise, receive mentorship and prepare for placements."
    )

    sign_in, register = st.tabs(
        ["Sign In", "Student Registration"]
    )

    with sign_in:

        with st.form("login_form"):

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            submit = st.form_submit_button(
                "Sign In",
                type="primary"
            )

        if submit:

            user = query(
                """
                SELECT * FROM users
                WHERE username=? AND password_hash=?
                """,
                (
                    username.strip(),
                    password_hash(password)
                ),
                one=True
            )

            if user:
                st.session_state["user"] = user
                st.rerun()

            else:
                st.error("Invalid username or password.")

        st.info(
            "Default mentor login: **mentor** / **Mentor@123**"
        )

    with register:

        with st.form("student_register"):

            full_name = st.text_input("Full Name")

            username = st.text_input(
                "Create Username",
                key="reg_username"
            )

            password = st.text_input(
                "Create Password",
                type="password",
                key="reg_password"
            )

            confirm = st.text_input(
                "Confirm Password",
                type="password"
            )

            academic_year = st.selectbox(
                "Academic Year",
                YEARS
            )

            branch = st.text_input(
                "Branch",
                value="Computer Science & Engineering"
            )

            submit = st.form_submit_button(
                "Register",
                type="primary"
            )

        if submit:

            if not full_name.strip() or not username.strip():
                st.error("Name and username are required.")

            elif len(password) < 8:
                st.error(
                    "Password must contain at least 8 characters."
                )

            elif password != confirm:
                st.error("Passwords do not match.")

            else:

                try:

                    execute(
                        """
                        INSERT INTO users
                        (
                            username,
                            password_hash,
                            full_name,
                            role,
                            academic_year,
                            branch,
                            created_at
                        )
                        VALUES (?, ?, ?, 'student', ?, ?, ?)
                        """,
                        (
                            username.strip(),
                            password_hash(password),
                            full_name.strip(),
                            academic_year,
                            branch.strip(),
                            timestamp()
                        )
                    )

                    st.success(
                        "Registration successful. Please sign in."
                    )

                except sqlite3.IntegrityError:

                    st.error(
                        "That username is already registered."
                    )


# ============================================================
# STUDENT DASHBOARD
# ============================================================

def student_dashboard(user):

    page_header(
        f"Welcome, {user['full_name']} 👋",
        "Your placement preparation overview."
    )

    year = user.get(
        "academic_year",
        "First Year"
    )

    tasks = [
        f"{year}:{category}:{task}"
        for category, items in ROADMAP[year].items()
        for task in items
    ]

    completed = query(
        """
        SELECT task_key FROM tasks
        WHERE student_id=? AND completed=1
        """,
        (user["id"],)
    )

    done = {
        row["task_key"]
        for row in completed
    }

    completed_count = sum(
        key in done
        for key in tasks
    )

    total = len(tasks)

    questions = query(
        """
        SELECT COUNT(*) AS n
        FROM questions
        WHERE student_id=?
        """,
        (user["id"],),
        one=True
    )["n"]

    applications = query(
        """
        SELECT COUNT(*) AS n
        FROM applications
        WHERE student_id=?
        """,
        (user["id"],),
        one=True
    )["n"]

    a, b, c = st.columns(3)

    a.metric(
        "Tasks completed",
        f"{completed_count}/{total}"
    )

    b.metric(
        "Mentor questions",
        questions
    )

    c.metric(
        "Applications",
        applications
    )

    st.subheader("Learning progress")

    st.progress(
        completed_count / total if total else 0
    )

    st.write(
        f"{completed_count} of {total} roadmap tasks completed for {year}."
    )

    st.subheader("Recent placement applications")

    rows = query(
        """
        SELECT company, role, status, applied_at
        FROM applications
        WHERE student_id=?
        ORDER BY id DESC
        LIMIT 5
        """,
        (user["id"],)
    )

    if rows:

        st.dataframe(
            pd.DataFrame(rows),
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info(
            "No applications recorded yet. Add one in Placement Tracker."
        )


# ============================================================
# RESOURCES AND TASKS
# ============================================================

def resources_page(user):

    page_header(
        "📚 Resources & Tasks",
        "Complete your year-wise placement preparation roadmap."
    )

    year = st.selectbox(
        "Academic Year",
        YEARS,
        index=YEAR_NUMBER.get(
            user.get("academic_year", "First Year"),
            1
        ) - 1
    )

    items = ROADMAP[year]

    keys = [
        f"{year}:{category}:{task}"
        for category, tasks in items.items()
        for task in tasks
    ]

    done_rows = query(
        """
        SELECT task_key FROM tasks
        WHERE student_id=? AND completed=1
        """,
        (user["id"],)
    )

    done = {
        row["task_key"]
        for row in done_rows
    }

    count = sum(
        key in done
        for key in keys
    )

    st.metric(
        "Completion",
        f"{count}/{len(keys)}"
    )

    st.progress(
        count / len(keys) if keys else 0
    )

    for category, tasks in items.items():

        with st.expander(category, expanded=True):

            for task in tasks:

                key = f"{year}:{category}:{task}"

                checked = st.checkbox(
                    task,
                    value=key in done,
                    key=f"task_{user['id']}_{key}"
                )

                if checked and key not in done:

                    execute(
                        """
                        INSERT OR REPLACE INTO tasks
                        (student_id, task_key, completed)
                        VALUES (?, ?, 1)
                        """,
                        (user["id"], key)
                    )

                    st.rerun()

                if not checked and key in done:

                    execute(
                        """
                        DELETE FROM tasks
                        WHERE student_id=? AND task_key=?
                        """,
                        (user["id"], key)
                    )

                    st.rerun()


# ============================================================
# ML PLACEMENT READINESS PREDICTION
# ============================================================

def readiness_page(user):

    page_header(
        "🤖 ML Placement Readiness Prediction",
        "The Random Forest model predicts a preparation category from your skills."
    )

    st.info(
        "Enter honest scores from 0 to 100. "
        "This model estimates a readiness category; it does not "
        "guarantee a job or represent a real hiring probability."
    )

    left, right = st.columns(2)

    with left:

        coding = st.number_input(
            "Coding Score",
            min_value=0,
            max_value=100,
            value=50
        )

        dsa = st.number_input(
            "DSA Score",
            min_value=0,
            max_value=100,
            value=50
        )

        technical = st.number_input(
            "Technical Skills",
            min_value=0,
            max_value=100,
            value=50
        )

        projects = st.number_input(
            "Projects Score",
            min_value=0,
            max_value=100,
            value=50
        )

        communication = st.number_input(
            "Communication Score",
            min_value=0,
            max_value=100,
            value=50
        )

    with right:

        aptitude = st.number_input(
            "Aptitude Score",
            min_value=0,
            max_value=100,
            value=50
        )

        internship = st.selectbox(
            "Internship Experience",
            ["No", "Yes"]
        )

        resume = st.number_input(
            "Resume Score",
            min_value=0,
            max_value=100,
            value=50
        )

        st.text_input(
            "Academic Year",
            value=user.get("academic_year", "First Year"),
            disabled=True
        )

        st.caption(
            "Academic year is automatically converted to the Year feature used during model training."
        )

    if st.button(
        "Predict with Machine Learning",
        type="primary",
        use_container_width=True
    ):

        try:

            prediction, confidence = ml_predict(
                user,
                coding,
                dsa,
                technical,
                projects,
                communication,
                aptitude,
                internship,
                resume
            )

            st.session_state["latest_ml_result"] = {
                "prediction": prediction,
                "confidence": confidence,
                "coding": coding,
                "dsa": dsa,
                "technical": technical,
                "projects": projects,
                "communication": communication,
                "aptitude": aptitude,
                "internship": internship,
                "resume": resume,
            }

            average_score = int(
                round(
                    np.mean([
                        coding,
                        dsa,
                        technical,
                        projects,
                        communication,
                        aptitude,
                        resume
                    ])
                )
            )

            execute(
                """
                INSERT INTO assessments
                (
                    student_id,
                    coding,
                    aptitude,
                    dsa,
                    internship,
                    technical,
                    resume,
                    projects,
                    communication,
                    score,
                    result,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user["id"],
                    int(coding),
                    int(aptitude),
                    int(dsa),
                    internship,
                    int(technical),
                    int(resume),
                    int(projects),
                    int(communication),
                    average_score,
                    prediction,
                    timestamp()
                )
            )

        except Exception as exc:

            st.error(
                f"ML prediction could not be completed: "
                f"{type(exc).__name__}: {exc}"
            )

            st.caption(
                "Check that both model files are in the same GitHub folder as app1.py."
            )

    result = st.session_state.get(
        "latest_ml_result"
    )

    if result:

        st.divider()

        st.subheader("Your ML prediction")

        st.metric(
            "Predicted readiness category",
            result["prediction"]
        )

        if result["confidence"] is not None:

            st.metric(
                "Model confidence for this classification",
                f"{result['confidence']:.1f}%"
            )

        st.caption(
            "Confidence is the model's classification confidence "
            "on this input, not the probability of getting placed."
        )

        score_values = {
            "Coding": result["coding"],
            "DSA": result["dsa"],
            "Technical": result["technical"],
            "Projects": result["projects"],
            "Communication": result["communication"],
            "Aptitude": result["aptitude"],
            "Resume": result["resume"],
        }

        weak = [
            name
            for name, value in score_values.items()
            if value < 45
        ]

        if weak:

            st.warning(
                "Focus on improving: " + ", ".join(weak)
            )

        else:

            st.success(
                "No skill score is below 45. Continue practising consistently."
            )

        st.bar_chart(
            pd.DataFrame({"Score": score_values})
        )

    st.subheader("Previous ML assessments")

    history = query(
        """
        SELECT score, result, created_at
        FROM assessments
        WHERE student_id=?
        ORDER BY id DESC
        LIMIT 10
        """,
        (user["id"],)
    )

    if history:

        st.dataframe(
            pd.DataFrame(history),
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info(
            "No assessments saved yet."
        )


# ============================================================
# ASK A MENTOR
# ============================================================

def ask_mentor_page(user):

    page_header(
        "💬 Ask a Mentor",
        "Submit placement and learning questions."
    )

    with st.form("ask_question"):

        topic = st.selectbox(
            "Topic",
            [
                "Programming",
                "Data Structures & Algorithms",
                "Database / SQL",
                "Aptitude",
                "Resume",
                "Interview Preparation",
                "Projects",
                "Career Guidance",
                "Other"
            ]
        )

        question = st.text_area(
            "Your question"
        )

        submit = st.form_submit_button(
            "Submit Question",
            type="primary"
        )

    if submit:

        if question.strip():

            execute(
                """
                INSERT INTO questions
                (student_id, question, topic, asked_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    user["id"],
                    question.strip(),
                    topic,
                    timestamp()
                )
            )

            st.success("Question submitted.")
            st.rerun()

        else:

            st.error(
                "Please enter your question."
            )

    st.subheader("My questions")

    rows = query(
        """
        SELECT * FROM questions
        WHERE student_id=?
        ORDER BY id DESC
        """,
        (user["id"],)
    )

    for row in rows:

        with st.expander(
            f"{row['topic']} — {row['asked_at']}"
        ):

            st.write(row["question"])

            if row["answer"]:

                st.success(row["answer"])

            else:

                st.info(
                    "Waiting for mentor response."
                )


# ============================================================
# PLACEMENT TRACKER
# ============================================================

def tracker_page(user):

    page_header(
        "📋 Placement Tracker",
        "Record and manage job applications."
    )

    with st.form("add_application"):

        company = st.text_input("Company")

        role = st.text_input("Job Role")

        status = st.selectbox(
            "Status",
            STATUSES
        )

        notes = st.text_area(
            "Notes (optional)"
        )

        submit = st.form_submit_button(
            "Add Application",
            type="primary"
        )

    if submit:

        if company.strip() and role.strip():

            execute(
                """
                INSERT INTO applications
                (
                    student_id,
                    company,
                    role,
                    status,
                    applied_at,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user["id"],
                    company.strip(),
                    role.strip(),
                    status,
                    timestamp(),
                    notes.strip()
                )
            )

            st.success("Application saved.")
            st.rerun()

        else:

            st.error(
                "Company and job role are required."
            )

    rows = query(
        """
        SELECT * FROM applications
        WHERE student_id=?
        ORDER BY id DESC
        """,
        (user["id"],)
    )

    if rows:

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )

        st.download_button(
            "Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            "placement_applications.csv",
            "text/csv"
        )

    else:

        st.info(
            "No applications recorded yet."
        )


# ============================================================
# MENTOR DASHBOARD
# ============================================================

def mentor_dashboard(user):

    page_header(
        "Mentor Dashboard",
        "Review student activity and questions."
    )

    students = query(
        "SELECT COUNT(*) AS n FROM users WHERE role='student'",
        one=True
    )["n"]

    questions = query(
        "SELECT COUNT(*) AS n FROM questions",
        one=True
    )["n"]

    pending = query(
        "SELECT COUNT(*) AS n FROM questions WHERE answer=''",
        one=True
    )["n"]

    a, b, c = st.columns(3)

    a.metric("Students", students)
    b.metric("Questions", questions)
    c.metric("Pending replies", pending)


# ============================================================
# MENTOR QUESTIONS
# ============================================================

def mentor_questions(user):

    page_header(
        "Student Questions",
        "Respond to questions submitted by students."
    )

    rows = query(
        """
        SELECT q.*, u.full_name
        FROM questions q
        JOIN users u ON u.id=q.student_id
        ORDER BY q.id DESC
        """
    )

    if not rows:

        st.info("No questions yet.")

    for row in rows:

        with st.expander(
            f"{row['full_name']} — {row['topic']} — #{row['id']}"
        ):

            st.write(row["question"])

            with st.form(
                f"answer_{row['id']}"
            ):

                answer = st.text_area(
                    "Mentor response",
                    value=row["answer"] or ""
                )

                submit = st.form_submit_button(
                    "Save Response"
                )

            if submit:

                if answer.strip():

                    execute(
                        """
                        UPDATE questions
                        SET answer=?, mentor_id=?, answered_at=?
                        WHERE id=?
                        """,
                        (
                            answer.strip(),
                            user["id"],
                            timestamp(),
                            row["id"]
                        )
                    )

                    st.success("Response saved.")
                    st.rerun()

                else:

                    st.error(
                        "Response cannot be empty."
                    )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    setup_database()
    create_default_mentor()

    user = st.session_state.get("user")

    if not user:

        login_page()
        return

    with st.sidebar:

        st.title(
            "🎓 CSE Placement Portal"
        )

        st.write(
            f"**{user['full_name']}**"
        )

        st.caption(
            user["role"].upper()
        )

        st.divider()

        if user["role"] == "mentor":

            pages = [
                "Dashboard",
                "Student Questions"
            ]

        else:

            pages = [
                "Dashboard",
                "Resources & Tasks",
                "ML Readiness Prediction",
                "Ask a Mentor",
                "Placement Tracker"
            ]

        page = st.radio(
            "Navigation",
            pages,
            label_visibility="collapsed"
        )

        st.divider()

        if st.button(
            "Logout",
            use_container_width=True
        ):

            st.session_state.pop(
                "user",
                None
            )

            st.session_state.pop(
                "latest_ml_result",
                None
            )

            st.rerun()

    if user["role"] == "mentor":

        if page == "Dashboard":

            mentor_dashboard(user)

        elif page == "Student Questions":

            mentor_questions(user)

    else:

        routes = {
            "Dashboard": lambda: student_dashboard(user),

            "Resources & Tasks": lambda: resources_page(user),

            "ML Readiness Prediction": lambda: readiness_page(user),

            "Ask a Mentor": lambda: ask_mentor_page(user),

            "Placement Tracker": lambda: tracker_page(user),
        }

        routes[page]()


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except Exception as exc:

        st.error(
            f"Application error: {type(exc).__name__}: {exc}"
        )

        st.exception(exc)
