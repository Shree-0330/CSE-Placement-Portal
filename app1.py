
import os
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CSE Placement Roadmap & Mentorship Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = Path(
    os.getenv(
        "PORTAL_DB_PATH",
        str(BASE_DIR / "placement_portal_v5.db")
    )
)

YEARS = [
    "First Year",
    "Second Year",
    "Third Year",
    "Final Year"
]

STATUSES = [
    "Applied",
    "Online Assessment",
    "Interview Scheduled",
    "Interview Completed",
    "Selected",
    "Rejected",
    "Offer Received"
]

ROADMAP = {
    "First Year": {
        "Programming": [
            "Programming fundamentals",
            "Python / Java basics",
            "Basic coding problems"
        ],
        "DSA": [
            "Arrays and Strings",
            "Linked Lists",
            "Stacks and Queues",
            "Trees and Graphs basics"
        ],
        "Projects": [
            "Learn Git and GitHub",
            "Build a mini project",
            "Write project documentation"
        ],
        "Aptitude": [
            "Number systems",
            "Percentages and ratios",
            "Logical reasoning",
            "Verbal ability"
        ],
        "Communication": [
            "Practise self-introduction",
            "Read technical articles",
            "Group discussion basics"
        ],
        "Placement": [
            "Explore career roles",
            "Create a basic resume",
            "Build a learning routine"
        ]
    },

    "Second Year": {
        "Programming": [
            "Object-oriented programming",
            "SQL and DBMS",
            "JavaScript practice",
            "Problem-solving practice"
        ],
        "DSA": [
            "Recursion",
            "Searching and sorting",
            "Hashing",
            "Trees and graphs"
        ],
        "Projects": [
            "Build a CRUD application",
            "Connect a database",
            "Publish a project on GitHub"
        ],
        "Aptitude": [
            "Quantitative aptitude",
            "Logical reasoning",
            "Verbal ability",
            "Timed practice tests"
        ],
        "Communication": [
            "Presentation practice",
            "Group discussion practice",
            "Technical explanation practice"
        ],
        "Placement": [
            "Prepare a resume",
            "Apply for internships",
            "Practise technical interview questions"
        ]
    },

    "Third Year": {
        "Programming": [
            "Advanced programming",
            "Operating Systems",
            "Computer Networks",
            "DBMS revision"
        ],
        "DSA": [
            "Advanced trees and graphs",
            "Dynamic programming",
            "Greedy algorithms",
            "Company coding questions"
        ],
        "Projects": [
            "Build a major project",
            "Improve project documentation",
            "Prepare a GitHub portfolio"
        ],
        "Aptitude": [
            "Advanced quantitative aptitude",
            "Logical reasoning tests",
            "Verbal ability tests"
        ],
        "Communication": [
            "Technical presentations",
            "Group discussions",
            "Mock interviews"
        ],
        "Placement": [
            "Prepare an ATS-friendly resume",
            "Research target companies",
            "Apply for internships and jobs"
        ]
    },

    "Final Year": {
        "Programming": [
            "Revise one primary language",
            "Practise SQL queries",
            "Revise core CS subjects"
        ],
        "DSA": [
            "Arrays and strings revision",
            "Trees and graphs revision",
            "Dynamic programming revision",
            "Company-specific coding tests"
        ],
        "Projects": [
            "Complete final-year project",
            "Prepare project explanation",
            "Update GitHub portfolio"
        ],
        "Aptitude": [
            "Daily aptitude tests",
            "Timed reasoning tests",
            "Verbal ability revision"
        ],
        "Communication": [
            "Self-introduction",
            "HR interview practice",
            "Mock technical interviews"
        ],
        "Placement": [
            "Finalise resume",
            "Track job applications",
            "Prepare for interviews",
            "Review offer details"
        ]
    }
}


# ============================================================
# DATABASE
# ============================================================

def connect_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    con.row_factory = sqlite3.Row
    return con


def execute(sql, params=()):
    con = connect_db()

    try:
        cur = con.execute(sql, params)
        con.commit()
        return cur.lastrowid
    finally:
        con.close()


def fetch_all(sql, params=()):
    con = connect_db()

    try:
        return [
            dict(row)
            for row in con.execute(sql, params).fetchall()
        ]
    finally:
        con.close()


def fetch_one(sql, params=()):
    rows = fetch_all(sql, params)
    return rows[0] if rows else None


def count_rows(sql, params=()):
    row = fetch_one(sql, params)
    return row["total"] if row else 0


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def hash_password(password):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        b"cse-placement-portal-v1",
        180000
    ).hex()


def initialize_database():

    con = connect_db()

    try:

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
            topic TEXT NOT NULL,
            answer TEXT DEFAULT '',
            mentor_id INTEGER,
            asked_at TEXT NOT NULL,
            answered_at TEXT
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_type TEXT NOT NULL,
            student_id INTEGER NOT NULL,
            mentor_id INTEGER,
            question_id INTEGER,
            rating INTEGER NOT NULL,
            comment TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            coding INTEGER NOT NULL,
            dsa INTEGER NOT NULL,
            technical INTEGER NOT NULL,
            projects INTEGER NOT NULL,
            communication INTEGER NOT NULL,
            aptitude INTEGER NOT NULL,
            resume INTEGER NOT NULL,
            internship TEXT NOT NULL,
            score INTEGER NOT NULL,
            result TEXT NOT NULL,
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

        """)

        con.commit()

    finally:
        con.close()

    default_username = os.getenv(
        "PORTAL_MENTOR_USERNAME",
        "mentor"
    )

    default_password = os.getenv(
        "PORTAL_MENTOR_PASSWORD",
        "Mentor@123"
    )

    existing = fetch_one(
        "SELECT id FROM users WHERE username=?",
        (default_username,)
    )

    if not existing:

        execute(
            """
            INSERT INTO users
            (
                username,
                password_hash,
                full_name,
                role,
                created_at
            )
            VALUES (?, ?, ?, 'mentor', ?)
            """,
            (
                default_username,
                hash_password(default_password),
                "Placement Mentor",
                now()
            )
        )


# ============================================================
# COMMON PAGE HEADER
# Native Streamlit only - no custom HTML/CSS
# ============================================================

def page_header(title, description):

    st.title(title)
    st.caption(description)
    st.divider()


# ============================================================
# REGISTRATION
# ============================================================

def registration(role):

    st.subheader(
        "Student Registration"
        if role == "student"
        else "Mentor Registration"
    )

    with st.form(
        f"registration_{role}",
        clear_on_submit=True
    ):

        full_name = st.text_input("Full Name")
        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        academic_year = "First Year"
        branch = "CSE"

        if role == "student":

            academic_year = st.selectbox(
                "Academic Year",
                YEARS
            )

            branch = st.text_input(
                "Branch",
                value="Computer Science & Engineering"
            )

        else:

            st.info(
                "Only authorised mentors should create mentor accounts."
            )

        submitted = st.form_submit_button(
            "Create Account",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if not full_name.strip() or not username.strip() or not password:
            st.error("Please complete all required fields.")

        elif len(username.strip()) < 3:
            st.error("Username must contain at least 3 characters.")

        elif len(password) < 8:
            st.error("Password must contain at least 8 characters.")

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
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        username.strip(),
                        hash_password(password),
                        full_name.strip(),
                        role,
                        academic_year,
                        branch.strip(),
                        now()
                    )
                )

                st.success(
                    "Account created successfully. Please sign in."
                )

            except sqlite3.IntegrityError:

                st.error("This username is already registered.")


# ============================================================
# LOGIN
# ============================================================

def login_page():

    st.title("🎓 CSE Placement Roadmap & Mentorship Portal")

    st.write(
        "A complete platform for placement preparation, "
        "student development and mentor guidance."
    )

    st.divider()

    _, center, _ = st.columns([1, 1.5, 1])

    with center:

        sign_in, student_reg, mentor_reg = st.tabs(
            [
                "Sign In",
                "Student Registration",
                "Mentor Registration"
            ]
        )

        with sign_in:

            with st.form("login_form"):

                username = st.text_input("Username")

                password = st.text_input(
                    "Password",
                    type="password"
                )

                submitted = st.form_submit_button(
                    "Sign In",
                    type="primary",
                    use_container_width=True
                )

            if submitted:

                user = fetch_one(
                    """
                    SELECT *
                    FROM users
                    WHERE username=? AND password_hash=?
                    """,
                    (
                        username.strip(),
                        hash_password(password)
                    )
                )

                if user:

                    st.session_state["user"] = user
                    st.rerun()

                else:

                    st.error("Invalid username or password.")

            st.info(
                "Default mentor login: mentor / Mentor@123"
            )

        with student_reg:
            registration("student")

        with mentor_reg:
            registration("mentor")


# ============================================================
# STUDENT TASK PROGRESS
# ============================================================

def get_task_progress(student_id, year):

    keys = [
        f"{year}|{category}|{task}"
        for category, tasks in ROADMAP[year].items()
        for task in tasks
    ]

    rows = fetch_all(
        """
        SELECT task_key
        FROM tasks
        WHERE student_id=? AND completed=1
        """,
        (student_id,)
    )

    completed = {
        row["task_key"]
        for row in rows
    }

    done = sum(
        key in completed
        for key in keys
    )

    return done, len(keys), completed


# ============================================================
# STUDENT DASHBOARD
# ============================================================

def student_dashboard(user):

    page_header(
        f"Welcome, {user['full_name']}",
        "Your placement preparation dashboard."
    )

    year = user["academic_year"] or "First Year"

    if year not in ROADMAP:
        year = "First Year"

    done, total_tasks, _ = get_task_progress(
        user["id"],
        year
    )

    questions = count_rows(
        "SELECT COUNT(*) AS total FROM questions WHERE student_id=?",
        (user["id"],)
    )

    applications = count_rows(
        "SELECT COUNT(*) AS total FROM applications WHERE student_id=?",
        (user["id"],)
    )

    latest = fetch_one(
        """
        SELECT score, result, created_at
        FROM assessments
        WHERE student_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user["id"],)
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Roadmap Tasks", f"{done}/{total_tasks}")

    c2.metric(
        "Completion",
        f"{done / total_tasks * 100:.0f}%"
        if total_tasks else "0%"
    )

    c3.metric("Mentor Questions", questions)

    c4.metric("Applications", applications)

    st.subheader("Learning Progress")

    st.progress(
        done / total_tasks
        if total_tasks else 0
    )

    st.write(
        f"Completed {done} of {total_tasks} tasks."
    )

    left, right = st.columns(2)

    with left:

        st.subheader("Pending Activities")

        _, _, completed = get_task_progress(
            user["id"],
            year
        )

        pending = [
            task
            for category, tasks in ROADMAP[year].items()
            for task in tasks
            if f"{year}|{category}|{task}" not in completed
        ]

        if pending:

            for task in pending[:6]:
                st.write("•", task)

        else:

            st.success("All roadmap tasks completed.")

    with right:

        st.subheader("Latest Readiness Assessment")

        if latest:

            st.metric(
                "Readiness Score",
                f"{latest['score']}/100"
            )

            st.write(latest["result"])

            st.caption(latest["created_at"])

        else:

            st.info(
                "Complete your readiness assessment to see your result."
            )


# ============================================================
# PLACEMENT ROADMAP
# ============================================================

def roadmap_page(user):

    page_header(
        "Placement Roadmap",
        "Follow the learning plan and mark activities as completed."
    )

    year = st.selectbox(
        "Select Academic Year",
        YEARS,
        index=(
            YEARS.index(user["academic_year"])
            if user["academic_year"] in YEARS else 0
        )
    )

    done, total_tasks, completed = get_task_progress(
        user["id"],
        year
    )

    c1, c2 = st.columns(2)

    c1.metric("Completed Tasks", f"{done}/{total_tasks}")

    c2.metric(
        "Progress",
        f"{done / total_tasks * 100:.1f}%"
        if total_tasks else "0%"
    )

    st.progress(
        done / total_tasks
        if total_tasks else 0
    )

    for category, tasks in ROADMAP[year].items():

        st.subheader(category)

        for task in tasks:

            key = f"{year}|{category}|{task}"

            checked = st.checkbox(
                task,
                value=key in completed,
                key=f"task_{user['id']}_{key}"
            )

            if checked != (key in completed):

                if checked:

                    execute(
                        """
                        INSERT INTO tasks
                        (student_id, task_key, completed)
                        VALUES (?, ?, 1)
                        ON CONFLICT(student_id, task_key)
                        DO UPDATE SET completed=1
                        """,
                        (user["id"], key)
                    )

                else:

                    execute(
                        """
                        DELETE FROM tasks
                        WHERE student_id=? AND task_key=?
                        """,
                        (user["id"], key)
                    )

                st.rerun()

        st.divider()


# ============================================================
# READINESS ASSESSMENT
# ============================================================

def readiness_label(score):

    if score >= 80:
        return "Placement Ready"

    elif score >= 60:
        return "Developing Well"

    elif score >= 40:
        return "Needs Focus"

    return "Early Preparation"


def assessment_advice(scores):

    advice = {
        "Coding": "Practise coding problems daily and explain your approach.",
        "DSA": "Revise arrays, strings, linked lists, stacks, queues and trees.",
        "Technical Skills": "Revise DBMS, OOP, operating systems and networks.",
        "Projects": "Improve project functionality and documentation.",
        "Communication": "Practise self-introduction and mock interviews.",
        "Aptitude": "Practise quantitative and logical reasoning tests.",
        "Resume": "Improve project descriptions, skills and achievements."
    }

    weakest = sorted(
        scores.items(),
        key=lambda x: x[1]
    )[:3]

    return [
        (skill, value, advice[skill])
        for skill, value in weakest
        if value < 70
    ]


def readiness_page(user):

    page_header(
        "Placement Readiness Assessment",
        "Assess your skills and review your previous performance."
    )

    st.info(
        "Rate each skill honestly from 0 to 100. "
        "The result is a preparation indicator, not a placement guarantee."
    )

    with st.form("assessment_form"):

        left, right = st.columns(2)

        with left:

            coding = st.slider("Coding", 0, 100, 50)

            dsa = st.slider(
                "Data Structures & Algorithms",
                0, 100, 50
            )

            technical = st.slider(
                "Technical Skills",
                0, 100, 50
            )

            projects = st.slider(
                "Projects",
                0, 100, 50
            )

        with right:

            communication = st.slider(
                "Communication",
                0, 100, 50
            )

            aptitude = st.slider(
                "Aptitude",
                0, 100, 50
            )

            resume = st.slider(
                "Resume",
                0, 100, 50
            )

            internship = st.selectbox(
                "Internship Experience",
                ["No", "Yes"]
            )

        submitted = st.form_submit_button(
            "Calculate Readiness",
            type="primary",
            use_container_width=True
        )

    if submitted:

        scores = {
            "Coding": coding,
            "DSA": dsa,
            "Technical Skills": technical,
            "Projects": projects,
            "Communication": communication,
            "Aptitude": aptitude,
            "Resume": resume
        }

        weighted_score = (
            coding * 0.20
            + dsa * 0.20
            + technical * 0.20
            + projects * 0.10
            + communication * 0.10
            + aptitude * 0.10
            + resume * 0.10
        )

        score = round(
            min(
                100,
                weighted_score + (
                    3 if internship == "Yes" else 0
                )
            )
        )

        result = readiness_label(score)

        execute(
            """
            INSERT INTO assessments
            (
                student_id,
                coding,
                dsa,
                technical,
                projects,
                communication,
                aptitude,
                resume,
                internship,
                score,
                result,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user["id"],
                coding,
                dsa,
                technical,
                projects,
                communication,
                aptitude,
                resume,
                internship,
                score,
                result,
                now()
            )
        )

        st.session_state["assessment_result"] = {
            "scores": scores,
            "score": score,
            "result": result
        }

        st.success("Assessment saved successfully.")

    # Display latest saved result
    latest = fetch_one(
        """
        SELECT *
        FROM assessments
        WHERE student_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user["id"],)
    )

    if latest:

        scores = {
            "Coding": latest["coding"],
            "DSA": latest["dsa"],
            "Technical Skills": latest["technical"],
            "Projects": latest["projects"],
            "Communication": latest["communication"],
            "Aptitude": latest["aptitude"],
            "Resume": latest["resume"]
        }

        st.divider()

        st.subheader("Latest Assessment Result")

        col1, col2 = st.columns([1, 2])

        with col1:

            st.metric(
                "Readiness Score",
                f"{latest['score']}/100"
            )

            st.write(
                f"**Assessment Level:** {latest['result']}"
            )

            st.progress(latest["score"] / 100)

            st.caption(
                f"Date: {latest['created_at']}"
            )

        with col2:

            chart_data = pd.DataFrame(
                {
                    "Skill": list(scores.keys()),
                    "Score": list(scores.values())
                }
            ).set_index("Skill")

            st.bar_chart(
                chart_data,
                y="Score"
            )

        st.subheader("Personal Improvement Plan")

        recommendations = assessment_advice(scores)

        if recommendations:

            for skill, value, advice in recommendations:

                st.markdown(
                    f"**{skill}: {value}/100**"
                )

                st.write(advice)

        else:

            st.success(
                "All assessed skills are at 70 or above. "
                "Continue practising."
            )

    else:

        st.info(
            "Submit your first assessment to see your results."
        )

    # Previous assessment history
    st.divider()

    st.subheader("Previous Assessment History")

    history = fetch_all(
        """
        SELECT *
        FROM assessments
        WHERE student_id=?
        ORDER BY id DESC
        LIMIT 50
        """,
        (user["id"],)
    )

    if history:

        history_df = pd.DataFrame(history)

        display = history_df[
            ["created_at", "score", "result"]
        ].rename(
            columns={
                "created_at": "Assessment Date",
                "score": "Score / 100",
                "result": "Assessment Level"
            }
        )

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Assessment History",
            history_df.to_csv(index=False).encode("utf-8"),
            file_name="assessment_history.csv",
            mime="text/csv"
        )

        selected_id = st.selectbox(
            "View Previous Assessment",
            [row["id"] for row in history],
            format_func=lambda value: next(
                (
                    f"Assessment #{r['id']} - "
                    f"{r['created_at']} - {r['score']}/100"
                )
                for r in history
                if r["id"] == value
            )
        )

        selected = next(
            row
            for row in history
            if row["id"] == selected_id
        )

        st.write(
            f"**Score:** {selected['score']}/100"
        )

        st.write(
            f"**Result:** {selected['result']}"
        )

        detail = {
            "Coding": selected["coding"],
            "DSA": selected["dsa"],
            "Technical Skills": selected["technical"],
            "Projects": selected["projects"],
            "Communication": selected["communication"],
            "Aptitude": selected["aptitude"],
            "Resume": selected["resume"]
        }

        detail_df = pd.DataFrame(
            {
                "Skill": list(detail.keys()),
                "Score": list(detail.values())
            }
        ).set_index("Skill")

        st.bar_chart(detail_df, y="Score")

    else:

        st.info("No previous assessments found.")


# ============================================================
# ASK A MENTOR
# ============================================================

def ask_mentor_page(user):

    page_header(
        "Ask a Mentor",
        "Submit questions and receive guidance from your mentor."
    )

    with st.form("ask_mentor_form"):

        topic = st.selectbox(
            "Topic",
            [
                "Programming",
                "DSA",
                "DBMS / SQL",
                "Aptitude",
                "Resume",
                "Interview Preparation",
                "Projects",
                "Career Guidance",
                "Other"
            ]
        )

        question = st.text_area(
            "Your Question",
            height=130
        )

        submitted = st.form_submit_button(
            "Submit Question",
            type="primary"
        )

    if submitted:

        if not question.strip():

            st.error("Please enter your question.")

        else:

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
                    now()
                )
            )

            st.success("Your question has been submitted.")
            st.rerun()

    st.subheader("My Questions")

    rows = fetch_all(
        """
        SELECT q.*, u.full_name AS mentor_name
        FROM questions q
        LEFT JOIN users u ON u.id=q.mentor_id
        WHERE q.student_id=?
        ORDER BY q.id DESC
        """,
        (user["id"],)
    )

    if not rows:
        st.info("You have not submitted any questions.")

    for row in rows:

        with st.container(border=True):

            st.caption(
                f"Question #{row['id']} · "
                f"{row['topic']} · {row['asked_at']}"
            )

            st.write(row["question"])

            if row["answer"]:

                st.success("Mentor Response")

                st.write(row["answer"])

                st.caption(
                    f"Answered by {row['mentor_name'] or 'Mentor'}"
                )

            else:

                st.warning("Awaiting mentor response.")


# ============================================================
# STUDENT FEEDBACK ABOUT MENTOR
# ============================================================

def student_feedback_page(user):

    page_header(
        "Student Feedback",
        "Share your feedback about the mentor guidance you received."
    )

    rows = fetch_all(
        """
        SELECT
            q.id,
            q.topic,
            q.question,
            q.answer,
            q.answered_at,
            f.id AS feedback_id,
            f.rating,
            f.comment
        FROM questions q
        LEFT JOIN feedback f
            ON f.question_id=q.id
            AND f.feedback_type='student_to_mentor'
        WHERE q.student_id=?
            AND q.answer<>''
        ORDER BY q.id DESC
        """,
        (user["id"],)
    )

    if not rows:

        st.info(
            "You can submit feedback after your mentor answers a question."
        )

        return

    for row in rows:

        with st.container(border=True):

            st.caption(
                f"Question #{row['id']} · {row['topic']}"
            )

            st.write("**Your Question**")
            st.write(row["question"])

            st.write("**Mentor Response**")
            st.write(row["answer"])

            if row["feedback_id"]:

                st.success(
                    f"Your rating: {row['rating']}/5"
                )

                if row["comment"]:
                    st.write(row["comment"])

            else:

                with st.form(
                    f"student_feedback_{row['id']}"
                ):

                    rating = st.select_slider(
                        "Rate this response",
                        options=[1, 2, 3, 4, 5],
                        value=5
                    )

                    comment = st.text_area(
                        "Your Feedback (optional)"
                    )

                    submitted = st.form_submit_button(
                        "Submit Feedback"
                    )

                if submitted:

                    execute(
                        """
                        INSERT INTO feedback
                        (
                            feedback_type,
                            student_id,
                            mentor_id,
                            question_id,
                            rating,
                            comment,
                            created_at
                        )
                        VALUES (
                            'student_to_mentor',
                            ?,
                            NULL,
                            ?,
                            ?,
                            ?,
                            ?
                        )
                        """,
                        (
                            user["id"],
                            row["id"],
                            rating,
                            comment.strip(),
                            now()
                        )
                    )

                    st.success("Feedback saved.")
                    st.rerun()


# ============================================================
# FEEDBACK FROM MENTOR TO STUDENT
# ============================================================

def student_mentor_feedback_page(user):

    page_header(
        "Feedback From Your Mentor",
        "Review improvement suggestions shared by your mentor."
    )

    rows = fetch_all(
        """
        SELECT
            f.rating,
            f.comment,
            f.created_at,
            u.full_name
        FROM feedback f
        JOIN users u ON u.id=f.mentor_id
        WHERE
            f.feedback_type='mentor_to_student'
            AND f.student_id=?
        ORDER BY f.id DESC
        """,
        (user["id"],)
    )

    if not rows:

        st.info(
            "Your mentor feedback will appear here."
        )

        return

    for row in rows:

        with st.container(border=True):

            st.caption(
                f"{row['created_at']} · Mentor: {row['full_name']}"
            )

            st.write(
                f"**Progress Rating:** {row['rating']}/5"
            )

            st.write(row["comment"])


# ============================================================
# PLACEMENT TRACKER
# ============================================================

def placement_tracker(user):

    page_header(
        "Placement Tracker",
        "Track company applications and recruitment progress."
    )

    with st.form(
        "application_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            company = st.text_input("Company Name")
            role = st.text_input("Job Role")

        with col2:

            status = st.selectbox(
                "Application Status",
                STATUSES
            )

            notes = st.text_input("Notes")

        submitted = st.form_submit_button(
            "Add Application",
            type="primary"
        )

    if submitted:

        if not company.strip() or not role.strip():

            st.error("Enter company and job role.")

        else:

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
                    now(),
                    notes.strip()
                )
            )

            st.success("Application added.")
            st.rerun()

    rows = fetch_all(
        """
        SELECT *
        FROM applications
        WHERE student_id=?
        ORDER BY id DESC
        """,
        (user["id"],)
    )

    if not rows:

        st.info("No applications added yet.")
        return

    df = pd.DataFrame(rows)

    st.dataframe(
        df[
            [
                "company",
                "role",
                "status",
                "applied_at",
                "notes"
            ]
        ].rename(
            columns={
                "company": "Company",
                "role": "Role",
                "status": "Status",
                "applied_at": "Applied Date",
                "notes": "Notes"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Applications CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="placement_applications.csv",
        mime="text/csv"
    )

    st.subheader("Update Application")

    selected_id = st.selectbox(
        "Select Application",
        [row["id"] for row in rows],
        format_func=lambda value: next(
            f"{r['company']} - {r['role']}"
            for r in rows
            if r["id"] == value
        )
    )

    selected = next(
        row
        for row in rows
        if row["id"] == selected_id
    )

    new_status = st.selectbox(
        "New Status",
        STATUSES,
        index=(
            STATUSES.index(selected["status"])
            if selected["status"] in STATUSES else 0
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Update Status", use_container_width=True):

            execute(
                """
                UPDATE applications
                SET status=?
                WHERE id=? AND student_id=?
                """,
                (
                    new_status,
                    selected_id,
                    user["id"]
                )
            )

            st.success("Status updated.")
            st.rerun()

    with col2:

        if st.button("Delete Application", use_container_width=True):

            execute(
                """
                DELETE FROM applications
                WHERE id=? AND student_id=?
                """,
                (
                    selected_id,
                    user["id"]
                )
            )

            st.success("Application deleted.")
            st.rerun()


# ============================================================
# MENTOR DASHBOARD
# ============================================================

def mentor_dashboard(user):

    page_header(
        f"Welcome, {user['full_name']}",
        "Mentor dashboard for student support and progress."
    )

    students = count_rows(
        "SELECT COUNT(*) AS total FROM users WHERE role='student'"
    )

    questions = count_rows(
        "SELECT COUNT(*) AS total FROM questions"
    )

    pending = count_rows(
        """
        SELECT COUNT(*) AS total
        FROM questions
        WHERE answer='' OR answer IS NULL
        """
    )

    feedback_count = count_rows(
        "SELECT COUNT(*) AS total FROM feedback"
    )

    a, b, c, d = st.columns(4)

    a.metric("Registered Students", students)
    b.metric("Total Questions", questions)
    c.metric("Pending Questions", pending)
    d.metric("Feedback Responses", feedback_count)

    st.subheader("Recent Student Questions")

    rows = fetch_all(
        """
        SELECT
            q.id,
            u.full_name,
            q.topic,
            q.question,
            q.asked_at
        FROM questions q
        JOIN users u ON u.id=q.student_id
        ORDER BY q.id DESC
        LIMIT 10
        """
    )

    if rows:

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No student questions yet.")


# ============================================================
# MENTOR ANSWERS
# ============================================================

def mentor_questions_page(user):

    page_header(
        "Student Questions",
        "Review questions and provide guidance."
    )

    rows = fetch_all(
        """
        SELECT q.*, u.full_name
        FROM questions q
        JOIN users u ON u.id=q.student_id
        ORDER BY q.id DESC
        """
    )

    if not rows:

        st.info("No questions submitted.")
        return

    for row in rows:

        with st.container(border=True):

            st.caption(
                f"#{row['id']} · {row['full_name']} · "
                f"{row['topic']} · {row['asked_at']}"
            )

            st.write(row["question"])

            with st.form(
                f"answer_form_{row['id']}"
            ):

                answer = st.text_area(
                    "Mentor Response",
                    value=row["answer"] or "",
                    height=110
                )

                submitted = st.form_submit_button(
                    "Save Response"
                )

            if submitted:

                if not answer.strip():

                    st.error("Response cannot be empty.")

                else:

                    execute(
                        """
                        UPDATE questions
                        SET answer=?, mentor_id=?, answered_at=?
                        WHERE id=?
                        """,
                        (
                            answer.strip(),
                            user["id"],
                            now(),
                            row["id"]
                        )
                    )

                    st.success("Response saved.")
                    st.rerun()


# ============================================================
# MENTOR FEEDBACK
# ============================================================

def mentor_feedback_page(user):

    page_header(
        "Mentor Feedback",
        "Give constructive feedback to students."
    )

    students = fetch_all(
        """
        SELECT id, full_name, academic_year
        FROM users
        WHERE role='student'
        ORDER BY full_name
        """
    )

    if not students:

        st.info("No students registered.")
        return

    with st.form("mentor_feedback_form"):

        student_id = st.selectbox(
            "Select Student",
            [s["id"] for s in students],
            format_func=lambda value: next(
                f"{s['full_name']} · {s['academic_year']}"
                for s in students
                if s["id"] == value
            )
        )

        category = st.selectbox(
            "Feedback Category",
            [
                "Technical Skills",
                "Coding Practice",
                "DSA",
                "Projects",
                "Communication",
                "Aptitude",
                "Resume",
                "Interview Preparation",
                "Overall Progress"
            ]
        )

        rating = st.select_slider(
            "Progress Rating",
            options=[1, 2, 3, 4, 5],
            value=3
        )

        comment = st.text_area(
            "Mentor Feedback",
            height=120
        )

        submitted = st.form_submit_button(
            "Submit Feedback",
            type="primary"
        )

    if submitted:

        if not comment.strip():

            st.error("Please enter feedback.")

        else:

            execute(
                """
                INSERT INTO feedback
                (
                    feedback_type,
                    student_id,
                    mentor_id,
                    question_id,
                    rating,
                    comment,
                    created_at
                )
                VALUES (
                    'mentor_to_student',
                    ?,
                    ?,
                    NULL,
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    student_id,
                    user["id"],
                    rating,
                    f"{category}: {comment.strip()}",
                    now()
                )
            )

            st.success("Feedback shared with student.")
            st.rerun()

    st.divider()

    st.subheader("Feedback Submitted by You")

    given = fetch_all(
        """
        SELECT
            f.rating,
            f.comment,
            f.created_at,
            u.full_name
        FROM feedback f
        JOIN users u ON u.id=f.student_id
        WHERE
            f.feedback_type='mentor_to_student'
            AND f.mentor_id=?
        ORDER BY f.id DESC
        """,
        (user["id"],)
    )

    if given:

        st.dataframe(
            pd.DataFrame(given),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No feedback submitted yet.")


# ============================================================
# MENTOR VIEWS STUDENT FEEDBACK
# ============================================================

def mentor_student_feedback_page():

    page_header(
        "Student Feedback",
        "Review feedback about mentor responses."
    )

    rows = fetch_all(
        """
        SELECT
            f.rating,
            f.comment,
            f.created_at,
            u.full_name,
            q.topic
        FROM feedback f
        JOIN users u ON u.id=f.student_id
        LEFT JOIN questions q ON q.id=f.question_id
        WHERE f.feedback_type='student_to_mentor'
        ORDER BY f.id DESC
        """
    )

    if not rows:

        st.info("No student feedback received yet.")
        return

    average = sum(
        row["rating"]
        for row in rows
    ) / len(rows)

    c1, c2 = st.columns(2)

    c1.metric("Average Rating", f"{average:.1f}/5")
    c2.metric("Feedback Received", len(rows))

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MENTOR PLACEMENT OUTCOMES
# ============================================================

def mentor_outcomes_page():

    page_header(
        "Placement Outcomes",
        "Review student placement applications."
    )

    rows = fetch_all(
        """
        SELECT
            u.full_name,
            a.company,
            a.role,
            a.status,
            a.applied_at,
            a.notes
        FROM applications a
        JOIN users u ON u.id=a.student_id
        ORDER BY a.id DESC
        """
    )

    if not rows:

        st.info("No placement applications found.")
        return

    df = pd.DataFrame(rows)

    options = ["All"] + sorted(
        df["status"].dropna().unique().tolist()
    )

    selected = st.selectbox(
        "Filter Application Status",
        options
    )

    if selected != "All":
        df = df[df["status"] == selected]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Placement Outcomes",
        df.to_csv(index=False).encode("utf-8"),
        file_name="placement_outcomes.csv",
        mime="text/csv"
    )


# ============================================================
# SIDEBAR AND APPLICATION ROUTING
# ============================================================

def main():

    initialize_database()

    if "user" not in st.session_state:

        login_page()
        return

    user = fetch_one(
        "SELECT * FROM users WHERE id=?",
        (st.session_state["user"]["id"],)
    )

    if not user:

        st.session_state.pop("user", None)
        st.rerun()
        return

    st.session_state["user"] = user

    with st.sidebar:

        st.title("🎓 CSE PORTAL")

        st.write(
            f"**{user['full_name']}**"
        )

        st.caption(
            user["role"].upper()
        )

        st.divider()

        if user["role"] == "student":

            pages = [
                "Dashboard",
                "Placement Roadmap",
                "Readiness Assessment",
                "Ask a Mentor",
                "Student Feedback",
                "Feedback From Mentor",
                "Placement Tracker"
            ]

        else:

            pages = [
                "Dashboard",
                "Student Questions",
                "Mentor Feedback",
                "Student Feedback",
                "Placement Outcomes"
            ]

        page = st.radio(
            "NAVIGATION",
            pages,
            label_visibility="collapsed"
        )

        st.divider()

        if st.button(
            "Logout",
            use_container_width=True
        ):

            st.session_state.pop("user", None)
            st.rerun()

    if user["role"] == "student":

        routes = {
            "Dashboard": lambda: student_dashboard(user),
            "Placement Roadmap": lambda: roadmap_page(user),
            "Readiness Assessment": lambda: readiness_page(user),
            "Ask a Mentor": lambda: ask_mentor_page(user),
            "Student Feedback": lambda: student_feedback_page(user),
            "Feedback From Mentor": lambda: student_mentor_feedback_page(user),
            "Placement Tracker": lambda: placement_tracker(user)
        }

    else:

        routes = {
            "Dashboard": lambda: mentor_dashboard(user),
            "Student Questions": lambda: mentor_questions_page(user),
            "Mentor Feedback": lambda: mentor_feedback_page(user),
            "Student Feedback": mentor_student_feedback_page,
            "Placement Outcomes": mentor_outcomes_page
        }

    routes[page]()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except Exception as error:

        st.error("Application error")

        st.exception(error)
