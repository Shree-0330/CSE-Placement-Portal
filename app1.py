
import os
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

# ============================================================
# CSE PLACEMENT ROADMAP & MENTORSHIP PORTAL
# Python + Streamlit + SQLite
# ============================================================

st.set_page_config(
    page_title="CSE Placement Roadmap & Mentorship Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
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
# PROFESSIONAL DESIGN
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #f4f7fb;
    color: #202b3c;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #142746;
}

[data-testid="stSidebar"] * {
    color: #f7f9fc !important;
}

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e4eaf2;
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 4px 14px rgba(20,39,70,.05);
}

.portal-hero {
    background: linear-gradient(110deg,#17345d,#3269a8);
    border-radius: 18px;
    padding: 25px 28px;
    color: white;
    margin-bottom: 20px;
}

.portal-hero h1 {
    color: white;
    font-size: 28px;
    margin: 0 0 7px 0;
}

.portal-hero p {
    color: #e4efff;
    margin: 0;
}

div.stButton > button,
div.stFormSubmitButton > button {
    border-radius: 9px;
    min-height: 40px;
    font-weight: 600;
}

.section-note {
    background: #edf4ff;
    border-left: 4px solid #3976bd;
    padding: 12px 15px;
    border-radius: 7px;
    margin: 8px 0 16px 0;
}

</style>
""", unsafe_allow_html=True)


def banner(title, subtitle):
    st.markdown(
        f"""
        <div class="portal-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def db_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")

    return con


def db_execute(sql, params=()):
    con = db_connection()

    try:
        cur = con.execute(sql, params)
        con.commit()
        return cur.lastrowid

    finally:
        con.close()


def db_all(sql, params=()):
    con = db_connection()

    try:
        return [
            dict(row)
            for row in con.execute(sql, params).fetchall()
        ]

    finally:
        con.close()


def db_one(sql, params=()):
    rows = db_all(sql, params)
    return rows[0] if rows else None


def total(sql, params=()):
    row = db_one(sql, params)
    return int(row["n"]) if row else 0


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def password_hash(password):
    salt = "cse-placement-portal-v1"

    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        180000
    ).hex()


def init_db():

    con = db_connection()

    try:

        con.executescript("""

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL
                CHECK(role IN ('student','mentor')),
            academic_year TEXT DEFAULT 'First Year',
            branch TEXT DEFAULT 'CSE',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            task_key TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
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

    default_user = os.getenv(
        "PORTAL_MENTOR_USERNAME",
        "mentor"
    )

    default_pass = os.getenv(
        "PORTAL_MENTOR_PASSWORD",
        "Mentor@123"
    )

    existing = db_one(
        "SELECT id FROM users WHERE username=?",
        (default_user,)
    )

    if not existing:

        db_execute(
            """
            INSERT INTO users
            (username,password_hash,full_name,role,created_at)
            VALUES(?,?,?,'mentor',?)
            """,
            (
                default_user,
                password_hash(default_pass),
                "Placement Mentor",
                timestamp()
            )
        )


# ============================================================
# REGISTRATION AND LOGIN
# ============================================================

def register_user(role):

    is_student = role == "student"

    title = (
        "Student Registration"
        if is_student
        else "Mentor Registration"
    )

    st.subheader(title)

    with st.form(
        f"{role}_registration_form",
        clear_on_submit=True
    ):

        full_name = st.text_input("Full Name")

        username = st.text_input("Create Username")

        password = st.text_input(
            "Create Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        academic_year = "First Year"
        branch = "CSE"

        if is_student:

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
                "Mentor accounts receive mentor permissions. "
                "Only authorised mentors should register."
            )

        submitted = st.form_submit_button(
            f"Create {role.title()} Account",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if (
            not full_name.strip()
            or not username.strip()
            or not password
        ):

            st.error("Please complete all required fields.")

        elif len(username.strip()) < 3:

            st.error(
                "Username must contain at least 3 characters."
            )

        elif len(password) < 8:

            st.error(
                "Password must contain at least 8 characters."
            )

        elif password != confirm:

            st.error("Passwords do not match.")

        else:

            try:

                db_execute(
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
                    VALUES(?,?,?,?,?,?,?)
                    """,
                    (
                        username.strip(),
                        password_hash(password),
                        full_name.strip(),
                        role,
                        academic_year,
                        branch.strip(),
                        timestamp()
                    )
                )

                st.success(
                    f"{title} completed. You can now sign in."
                )

            except sqlite3.IntegrityError:

                st.error(
                    "That username is already registered."
                )


def login_page():

    banner(
        "CSE Placement Roadmap & Mentorship Portal",
        "A structured workspace for placement preparation, "
        "mentorship and progress tracking."
    )

    left, center, right = st.columns([1, 1.35, 1])

    with center:

        login_tab, student_tab, mentor_tab = st.tabs(
            [
                "Sign In",
                "Student Registration",
                "Mentor Registration"
            ]
        )

        with login_tab:

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

                user = db_one(
                    """
                    SELECT * FROM users
                    WHERE username=? AND password_hash=?
                    """,
                    (
                        username.strip(),
                        password_hash(password)
                    )
                )

                if user:

                    st.session_state["user"] = user
                    st.rerun()

                else:

                    st.error("Invalid username or password.")

            st.caption(
                "Default mentor account: mentor / Mentor@123"
            )

        with student_tab:
            register_user("student")

        with mentor_tab:
            register_user("mentor")


# ============================================================
# TASK PROGRESS
# ============================================================

def task_progress(student_id, year):

    keys = [
        f"{year}|{category}|{task}"
        for category, tasks in ROADMAP[year].items()
        for task in tasks
    ]

    completed = db_all(
        """
        SELECT task_key FROM tasks
        WHERE student_id=? AND completed=1
        """,
        (student_id,)
    )

    done = {
        row["task_key"]
        for row in completed
    }

    count_done = sum(
        key in done
        for key in keys
    )

    return count_done, len(keys), done


# ============================================================
# STUDENT DASHBOARD
# ============================================================

def student_dashboard(user):

    year = user.get("academic_year") or "First Year"

    if year not in ROADMAP:
        year = "First Year"

    done, task_count, _ = task_progress(
        user["id"],
        year
    )

    q_count = total(
        """
        SELECT COUNT(*) AS n
        FROM questions
        WHERE student_id=?
        """,
        (user["id"],)
    )

    app_count = total(
        """
        SELECT COUNT(*) AS n
        FROM applications
        WHERE student_id=?
        """,
        (user["id"],)
    )

    last = db_one(
        """
        SELECT score,result,created_at
        FROM assessments
        WHERE student_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user["id"],)
    )

    banner(
        f"Welcome, {user['full_name']}",
        "Your placement preparation overview."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Roadmap Tasks",
        f"{done}/{task_count}"
    )

    c2.metric(
        "Task Completion",
        f"{(done / task_count * 100) if task_count else 0:.0f}%"
    )

    c3.metric(
        "Mentor Questions",
        q_count
    )

    c4.metric(
        "Job Applications",
        app_count
    )

    st.subheader("Your Learning Progress")

    st.progress(
        done / task_count if task_count else 0
    )

    st.caption(
        f"{done} of {task_count} tasks completed for {year}."
    )

    left, right = st.columns(2)

    with left:

        st.subheader("Next Steps")

        _, _, completed_keys = task_progress(
            user["id"],
            year
        )

        pending = [
            (category, task)
            for category, tasks in ROADMAP[year].items()
            for task in tasks
            if f"{year}|{category}|{task}" not in completed_keys
        ]

        if pending:

            for category, task in pending[:6]:

                st.write(
                    f"**{category}** · {task}"
                )

        else:

            st.success(
                "You have completed this year's roadmap."
            )

    with right:

        st.subheader("Latest Readiness Assessment")

        if last:

            st.metric(
                "Readiness Score",
                f"{last['score']}/100"
            )

            st.write(
                f"**Result:** {last['result']}"
            )

            st.caption(
                f"Assessed on {last['created_at']}"
            )

        else:

            st.info(
                "Complete your first placement readiness assessment."
            )


# ============================================================
# PLACEMENT ROADMAP
# ============================================================

def roadmap_page(user):

    banner(
        "Placement Roadmap",
        "Choose an academic year and track each preparation activity."
    )

    year = st.selectbox(
        "Academic Year",
        YEARS,
        index=(
            YEARS.index(user.get("academic_year", "First Year"))
            if user.get("academic_year", "First Year") in YEARS
            else 0
        )
    )

    done, count, completed = task_progress(
        user["id"],
        year
    )

    a, b = st.columns(2)

    a.metric(
        "Completed",
        f"{done}/{count}"
    )

    b.metric(
        "Progress",
        f"{(done/count*100) if count else 0:.1f}%"
    )

    st.progress(
        done / count if count else 0
    )

    for category, tasks in ROADMAP[year].items():

        st.subheader(category)

        for task in tasks:

            key = f"{year}|{category}|{task}"

            checked = st.checkbox(
                task,
                value=key in completed,
                key=f"roadmap_{user['id']}_{key}"
            )

            if checked != (key in completed):

                if checked:

                    db_execute(
                        """
                        INSERT INTO tasks
                        (student_id,task_key,completed)
                        VALUES(?,?,1)
                        ON CONFLICT(student_id,task_key)
                        DO UPDATE SET completed=1
                        """,
                        (
                            user["id"],
                            key
                        )
                    )

                else:

                    db_execute(
                        """
                        DELETE FROM tasks
                        WHERE student_id=? AND task_key=?
                        """,
                        (
                            user["id"],
                            key
                        )
                    )

                st.rerun()

        st.divider()


# ============================================================
# PLACEMENT READINESS ASSESSMENT
# ============================================================

def classify_readiness(score):

    if score >= 80:
        return "Placement Ready"

    if score >= 60:
        return "Developing Well"

    if score >= 40:
        return "Needs Focus"

    return "Early Preparation"


def assessment_recommendations(scores):

    advice = {

        "Coding":
            "Practise one or two coding problems daily and explain your approach.",

        "DSA":
            "Revise arrays, strings, linked lists, stacks, queues, trees and sorting.",

        "Technical Skills":
            "Revise DBMS, OOP, operating systems and computer networks.",

        "Projects":
            "Strengthen project functionality, documentation and your explanation.",

        "Communication":
            "Practise self-introduction, project explanation and mock interviews.",

        "Aptitude":
            "Practise timed quantitative, logical and verbal questions.",

        "Resume":
            "Improve project descriptions, skills, links and measurable achievements."
    }

    weak = sorted(
        scores.items(),
        key=lambda item: item[1]
    )[:3]

    return [
        (skill, value, advice[skill])
        for skill, value in weak
        if value < 70
    ]


def readiness_page(user):

    banner(
        "Placement Readiness Assessment",
        "Evaluate your current preparation and identify "
        "the skills that need attention."
    )

    st.info(
        "Enter honest scores from 0 to 100. "
        "This assessment is a preparation indicator, "
        "not a guarantee of placement."
    )

    with st.form("readiness_assessment_form"):

        left, right = st.columns(2)

        with left:

            coding = st.slider(
                "Coding",
                0, 100, 50
            )

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

        weighted = (
            coding * .20
            + dsa * .20
            + technical * .20
            + projects * .10
            + communication * .10
            + aptitude * .10
            + resume * .10
        )

        score = round(
            min(
                100,
                weighted + (3 if internship == "Yes" else 0)
            )
        )

        result = classify_readiness(score)

        db_execute(
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
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
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
                timestamp()
            )
        )

        st.session_state["latest_assessment"] = {
            "scores": scores,
            "score": score,
            "result": result
        }

    latest = st.session_state.get(
        "latest_assessment"
    )

    saved_latest = db_one(
        """
        SELECT *
        FROM assessments
        WHERE student_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user["id"],)
    )

    if latest and saved_latest:

        scores = latest["scores"]
        score = latest["score"]
        result = latest["result"]

    elif saved_latest:

        scores = {
            "Coding": saved_latest["coding"],
            "DSA": saved_latest["dsa"],
            "Technical Skills": saved_latest["technical"],
            "Projects": saved_latest["projects"],
            "Communication": saved_latest["communication"],
            "Aptitude": saved_latest["aptitude"],
            "Resume": saved_latest["resume"]
        }

        score = saved_latest["score"]
        result = saved_latest["result"]

    else:

        scores = None

    if scores:

        st.divider()

        st.subheader("Your Assessment Result")

        c1, c2 = st.columns([1, 2])

        with c1:

            st.metric(
                "Readiness Score",
                f"{score}/100"
            )

            st.write(
                f"**Assessment Level:** {result}"
            )

            st.progress(score / 100)

        with c2:

            chart_df = pd.DataFrame(
                {
                    "Skill": list(scores.keys()),
                    "Score": list(scores.values())
                }
            ).set_index("Skill")

            st.bar_chart(
                chart_df,
                y="Score",
                height=260
            )

        recommendations = assessment_recommendations(
            scores
        )

        st.subheader(
            "Recommended Improvement Plan"
        )

        if recommendations:

            for skill, value, suggestion in recommendations:

                st.markdown(
                    f"**{skill} — {value}/100**"
                )

                st.write(suggestion)

        else:

            st.success(
                "All assessed skills are at 70 or above. "
                "Maintain your preparation."
            )

    else:

        st.info(
            "Submit the assessment to view your score, "
            "skill chart and improvement plan."
        )

    # --------------------------------------------------------
    # PREVIOUS ASSESSMENT HISTORY
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Previous Assessment History"
    )

    history = db_all(
        """
        SELECT
            id,
            score,
            result,
            coding,
            dsa,
            technical,
            projects,
            communication,
            aptitude,
            resume,
            internship,
            created_at
        FROM assessments
        WHERE student_id=?
        ORDER BY id DESC
        LIMIT 20
        """,
        (user["id"],)
    )

    if history:

        history_df = pd.DataFrame(history)

        display_df = history_df[
            ["created_at", "score", "result"]
        ].rename(
            columns={
                "created_at": "Date",
                "score": "Score / 100",
                "result": "Assessment Level"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Assessment History CSV",
            history_df.to_csv(index=False).encode("utf-8"),
            file_name="my_assessment_history.csv",
            mime="text/csv"
        )

        selected_id = st.selectbox(
            "View assessment details",
            [row["id"] for row in history],
            format_func=lambda value: next(
                (
                    f"Assessment #{r['id']} · "
                    f"{r['created_at']} · {r['score']}/100"
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

        detail_scores = {
            "Coding": selected["coding"],
            "DSA": selected["dsa"],
            "Technical Skills": selected["technical"],
            "Projects": selected["projects"],
            "Communication": selected["communication"],
            "Aptitude": selected["aptitude"],
            "Resume": selected["resume"]
        }

        st.write(
            f"**Result:** {selected['result']} · "
            f"**Score:** {selected['score']}/100"
        )

        detail_df = pd.DataFrame(
            {
                "Skill": list(detail_scores.keys()),
                "Score": list(detail_scores.values())
            }
        ).set_index("Skill")

        st.bar_chart(
            detail_df,
            y="Score"
        )

    else:

        st.info(
            "Your assessment history will appear here "
            "after your first submission."
        )


# ============================================================
# ASK A MENTOR
# ============================================================

def ask_mentor_page(user):

    banner(
        "Ask a Mentor",
        "Send a placement or career question to the mentor team."
    )

    with st.form("ask_mentor_form"):

        topic = st.selectbox(
            "Question Topic",
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

            st.error(
                "Please enter your question."
            )

        else:

            db_execute(
                """
                INSERT INTO questions
                (student_id,question,topic,asked_at)
                VALUES(?,?,?,?)
                """,
                (
                    user["id"],
                    question.strip(),
                    topic,
                    timestamp()
                )
            )

            st.success(
                "Your question has been sent."
            )

            st.rerun()

    st.subheader("My Questions")

    rows = db_all(
        """
        SELECT
            q.*,
            u.full_name AS mentor_name
        FROM questions q
        LEFT JOIN users u
            ON u.id=q.mentor_id
        WHERE q.student_id=?
        ORDER BY q.id DESC
        """,
        (user["id"],)
    )

    if not rows:

        st.info(
            "You have not submitted any questions yet."
        )

    for row in rows:

        with st.container(border=True):

            st.caption(
                f"Question #{row['id']} · "
                f"{row['topic']} · {row['asked_at']}"
            )

            st.write(row["question"])

            if row["answer"]:

                st.success("Mentor response")

                st.write(row["answer"])

                st.caption(
                    f"Answered by {row['mentor_name'] or 'Mentor'} "
                    f"· {row['answered_at']}"
                )

            else:

                st.warning(
                    "Awaiting mentor response."
                )


# ============================================================
# STUDENT FEEDBACK ABOUT MENTOR RESPONSES
# ============================================================

def student_feedback_page(user):

    banner(
        "Student Feedback",
        "Rate the guidance you received from your mentor."
    )

    rows = db_all(
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
            "Feedback forms appear here after a mentor "
            "answers one of your questions."
        )

        return

    for row in rows:

        with st.container(border=True):

            st.caption(
                f"Question #{row['id']} · {row['topic']}"
            )

            st.write("**Your question**")
            st.write(row["question"])

            st.write("**Mentor response**")
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
                        "Rate this mentor response",
                        options=[1, 2, 3, 4, 5],
                        value=5
                    )

                    comment = st.text_area(
                        "Feedback (optional)"
                    )

                    submitted = st.form_submit_button(
                        "Submit Feedback"
                    )

                if submitted:

                    db_execute(
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
                        VALUES(
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
                            timestamp()
                        )
                    )

                    st.success(
                        "Thank you. Your feedback has been saved."
                    )

                    st.rerun()


# ============================================================
# PLACEMENT TRACKER
# ============================================================

def placement_tracker(user):

    banner(
        "Placement Tracker",
        "Record applications and follow each recruitment stage."
    )

    with st.form(
        "application_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            company = st.text_input(
                "Company Name"
            )

            role = st.text_input(
                "Job Role"
            )

        with col2:

            status = st.selectbox(
                "Application Status",
                STATUSES
            )

            notes = st.text_input(
                "Notes (optional)"
            )

        submitted = st.form_submit_button(
            "Add Application",
            type="primary"
        )

    if submitted:

        if not company.strip() or not role.strip():

            st.error(
                "Company name and job role are required."
            )

        else:

            db_execute(
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
                VALUES(?,?,?,?,?,?)
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

            st.success(
                "Application saved."
            )

            st.rerun()

    rows = db_all(
        """
        SELECT *
        FROM applications
        WHERE student_id=?
        ORDER BY id DESC
        """,
        (user["id"],)
    )

    if rows:

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
                    "applied_at": "Applied At",
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

        chosen = st.selectbox(
            "Choose application",
            [r["id"] for r in rows],
            format_func=lambda value: next(
                (
                    f"#{r['id']} · "
                    f"{r['company']} · {r['role']}"
                )
                for r in rows
                if r["id"] == value
            )
        )

        current = next(
            r for r in rows
            if r["id"] == chosen
        )

        new_status = st.selectbox(
            "New status",
            STATUSES,
            index=(
                STATUSES.index(current["status"])
                if current["status"] in STATUSES
                else 0
            )
        )

        u1, u2 = st.columns(2)

        with u1:

            if st.button(
                "Save Status",
                use_container_width=True
            ):

                db_execute(
                    """
                    UPDATE applications
                    SET status=?
                    WHERE id=? AND student_id=?
                    """,
                    (
                        new_status,
                        chosen,
                        user["id"]
                    )
                )

                st.success(
                    "Application status updated."
                )

                st.rerun()

        with u2:

            if st.button(
                "Delete Application",
                use_container_width=True
            ):

                db_execute(
                    """
                    DELETE FROM applications
                    WHERE id=? AND student_id=?
                    """,
                    (
                        chosen,
                        user["id"]
                    )
                )

                st.success(
                    "Application deleted."
                )

                st.rerun()

    else:

        st.info(
            "No applications have been added yet."
        )


# ============================================================
# MENTOR DASHBOARD
# ============================================================

def mentor_dashboard(user):

    banner(
        f"Welcome, {user['full_name']}",
        "Mentor workspace · student support and placement progress."
    )

    students = total(
        """
        SELECT COUNT(*) AS n
        FROM users
        WHERE role='student'
        """
    )

    question_count = total(
        """
        SELECT COUNT(*) AS n
        FROM questions
        """
    )

    pending = total(
        """
        SELECT COUNT(*) AS n
        FROM questions
        WHERE answer='' OR answer IS NULL
        """
    )

    feedback_count = total(
        """
        SELECT COUNT(*) AS n
        FROM feedback
        """
    )

    a, b, c, d = st.columns(4)

    a.metric("Registered Students", students)
    b.metric("Total Questions", question_count)
    c.metric("Pending Responses", pending)
    d.metric("Feedback Received", feedback_count)

    st.subheader("Latest Student Questions")

    rows = db_all(
        """
        SELECT
            q.id,
            u.full_name,
            q.topic,
            q.question,
            q.asked_at
        FROM questions q
        JOIN users u
            ON u.id=q.student_id
        ORDER BY q.id DESC
        LIMIT 8
        """
    )

    if rows:

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No student questions yet."
        )


# ============================================================
# MENTOR ANSWERS STUDENT QUESTIONS
# ============================================================

def mentor_questions_page(user):

    banner(
        "Student Questions",
        "Review student questions and provide useful, actionable answers."
    )

    rows = db_all(
        """
        SELECT
            q.*,
            u.full_name
        FROM questions q
        JOIN users u
            ON u.id=q.student_id
        ORDER BY q.id DESC
        """
    )

    if not rows:

        st.info(
            "No student questions have been submitted."
        )

        return

    for row in rows:

        with st.container(border=True):

            st.caption(
                f"Question #{row['id']} · "
                f"{row['full_name']} · "
                f"{row['topic']} · "
                f"{row['asked_at']}"
            )

            st.write(row["question"])

            with st.form(
                f"mentor_answer_{row['id']}"
            ):

                answer = st.text_area(
                    "Mentor Response",
                    value=row["answer"] or "",
                    key=f"answer_text_{row['id']}",
                    height=110
                )

                submitted = st.form_submit_button(
                    "Save Response"
                )

            if submitted:

                if not answer.strip():

                    st.error(
                        "Response cannot be empty."
                    )

                else:

                    db_execute(
                        """
                        UPDATE questions
                        SET
                            answer=?,
                            mentor_id=?,
                            answered_at=?
                        WHERE id=?
                        """,
                        (
                            answer.strip(),
                            user["id"],
                            timestamp(),
                            row["id"]
                        )
                    )

                    st.success(
                        "Response saved."
                    )

                    st.rerun()


# ============================================================
# MENTOR GIVES FEEDBACK TO STUDENTS
# ============================================================

def mentor_feedback_page(user):

    banner(
        "Mentor Feedback",
        "Provide constructive feedback to help students improve."
    )

    students = db_all(
        """
        SELECT
            id,
            full_name,
            username,
            academic_year
        FROM users
        WHERE role='student'
        ORDER BY full_name
        """
    )

    if not students:

        st.info(
            "No students are registered yet."
        )

        return

    with st.form("mentor_feedback_form"):

        student_id = st.selectbox(
            "Select Student",
            [r["id"] for r in students],
            format_func=lambda value: next(
                (
                    f"{r['full_name']} · "
                    f"{r['academic_year'] or 'Year not set'}"
                )
                for r in students
                if r["id"] == value
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
            "Submit Mentor Feedback",
            type="primary"
        )

    if submitted:

        if not comment.strip():

            st.error(
                "Please enter feedback before submitting."
            )

        else:

            db_execute(
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
                VALUES(
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
                    timestamp()
                )
            )

            st.success(
                "Feedback has been shared with the student."
            )

            st.rerun()

    st.divider()

    st.subheader(
        "Feedback Submitted by You"
    )

    given = db_all(
        """
        SELECT
            f.rating,
            f.comment,
            f.created_at,
            u.full_name
        FROM feedback f
        JOIN users u
            ON u.id=f.student_id
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

        st.info(
            "Your submitted student feedback will appear here."
        )


# ============================================================
# MENTOR VIEWS STUDENT FEEDBACK
# ============================================================

def mentor_student_feedback_page():

    banner(
        "Student Feedback",
        "Review ratings and comments students have submitted about mentor responses."
    )

    rows = db_all(
        """
        SELECT
            f.rating,
            f.comment,
            f.created_at,
            u.full_name,
            q.topic
        FROM feedback f
        JOIN users u
            ON u.id=f.student_id
        LEFT JOIN questions q
            ON q.id=f.question_id
        WHERE f.feedback_type='student_to_mentor'
        ORDER BY f.id DESC
        """
    )

    if not rows:

        st.info(
            "No student feedback has been submitted yet."
        )

        return

    average = sum(
        r["rating"] for r in rows
    ) / len(rows)

    c1, c2 = st.columns(2)

    c1.metric(
        "Average Mentor Rating",
        f"{average:.1f}/5"
    )

    c2.metric(
        "Feedback Responses",
        len(rows)
    )

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MENTOR VIEWS PLACEMENT OUTCOMES
# ============================================================

def mentor_outcomes_page():

    banner(
        "Placement Outcomes",
        "Review placement applications recorded by students."
    )

    rows = db_all(
        """
        SELECT
            u.full_name,
            a.company,
            a.role,
            a.status,
            a.applied_at,
            a.notes
        FROM applications a
        JOIN users u
            ON u.id=a.student_id
        ORDER BY a.id DESC
        """
    )

    if not rows:

        st.info(
            "No placement applications are available."
        )

        return

    df = pd.DataFrame(rows)

    options = ["All"] + sorted(
        df["status"].dropna().unique().tolist()
    )

    selected = st.selectbox(
        "Filter by Status",
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
        "Download Placement Outcomes CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="placement_outcomes.csv",
        mime="text/csv"
    )


# ============================================================
# STUDENT VIEWS FEEDBACK FROM MENTOR
# ============================================================

def student_mentor_feedback_view(user):

    banner(
        "Feedback From Your Mentor",
        "Review guidance and improvement feedback shared by your mentor."
    )

    rows = db_all(
        """
        SELECT
            f.rating,
            f.comment,
            f.created_at,
            u.full_name
        FROM feedback f
        JOIN users u
            ON u.id=f.mentor_id
        WHERE
            f.feedback_type='mentor_to_student'
            AND f.student_id=?
        ORDER BY f.id DESC
        """,
        (user["id"],)
    )

    if rows:

        for row in rows:

            with st.container(border=True):

                st.caption(
                    f"{row['created_at']} · "
                    f"Mentor: {row['full_name']}"
                )

                st.write(
                    f"**Progress rating:** {row['rating']}/5"
                )

                st.write(
                    row["comment"]
                )

    else:

        st.info(
            "Your mentor's feedback will appear here "
            "when it is shared."
        )


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

def main():

    init_db()

    if "user" not in st.session_state:

        login_page()
        return

    user = st.session_state["user"]

    fresh = db_one(
        "SELECT * FROM users WHERE id=?",
        (user["id"],)
    )

    if not fresh:

        st.session_state.pop("user", None)
        st.rerun()

    user = fresh
    st.session_state["user"] = user

    with st.sidebar:

        st.markdown("## 🎓 CSE PORTAL")

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
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.pop("user", None)
            st.rerun()

    if user["role"] == "student":

        routes = {

            "Dashboard":
                lambda: student_dashboard(user),

            "Placement Roadmap":
                lambda: roadmap_page(user),

            "Readiness Assessment":
                lambda: readiness_page(user),

            "Ask a Mentor":
                lambda: ask_mentor_page(user),

            "Student Feedback":
                lambda: student_feedback_page(user),

            "Feedback From Mentor":
                lambda: student_mentor_feedback_view(user),

            "Placement Tracker":
                lambda: placement_tracker(user)
        }

    else:

        routes = {

            "Dashboard":
                lambda: mentor_dashboard(user),

            "Student Questions":
                lambda: mentor_questions_page(user),

            "Mentor Feedback":
                lambda: mentor_feedback_page(user),

            "Student Feedback":
                mentor_student_feedback_page,

            "Placement Outcomes":
                mentor_outcomes_page
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
            "The application encountered an error."
        )

        st.exception(exc)
