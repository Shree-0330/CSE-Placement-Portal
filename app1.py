import os
import sqlite3
import hashlib
import traceback
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

import pandas as pd
import streamlit as st

# =========================================================
# 1. CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CSE Placement Roadmap & Mentorship Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("PORTAL_DB_PATH", str(BASE_DIR / "placement_portal_v4.db")))

YEARS = ["First Year", "Second Year", "Third Year", "Final Year"]

STATUSES = [
    "Applied",
    "Online Assessment",
    "Interview Scheduled",
    "Interview Completed",
    "Selected",
    "Rejected",
    "Offer Received",
]

# =========================================================
# 2. RESOURCES AND TASKS
# =========================================================

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
            "Mock interview practice",
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
            "Mock interview practice",
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
            "HR interview preparation",
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
            "Mock interview practice",
            "Placement application tracking",
        ],
    },
}

# =========================================================
# 3. STYLING
# =========================================================

st.markdown("""
<style>
.stApp {
    background: #f4f7fc;
    color: #303746;
}
.block-container {
    padding-top: 1.4rem;
    max-width: 1450px;
}
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #14294f, #263e72);
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}
.hero {
    background: linear-gradient(110deg, #18356b, #386bc1);
    color: white;
    border-radius: 17px;
    padding: 24px 28px;
    margin-bottom: 22px;
}
.hero h1 {
    color: white !important;
    margin: 0;
    font-size: 28px;
}
.hero p {
    color: #e2eaff;
    margin: 8px 0 0;
}
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e4eaf4;
    border-radius: 13px;
    padding: 16px;
    box-shadow: 0 3px 14px #1c37600b;
}
div.stButton > button {
    border-radius: 9px;
    min-height: 40px;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. DATABASE FUNCTIONS
# =========================================================

@contextmanager
def connect():
    """Open a SQLite connection and always close it after use."""
    con = sqlite3.connect(DB_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def execute(sql, params=()):
    with connect() as con:
        con.execute(sql, params)


def fetch_all(sql, params=()):
    with connect() as con:
        return [
            dict(row)
            for row in con.execute(sql, params).fetchall()
        ]


def count_rows(sql, params=()):
    rows = fetch_all(sql, params)
    return rows[0]["total"] if rows else 0


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def setup_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect() as con:
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
        # =========================================================
# 5. CREATE DEFAULT MENTOR
# =========================================================

def create_default_mentor():
    username = os.getenv(
        "PORTAL_MENTOR_USERNAME", "mentor"
    )
    password = os.getenv(
        "PORTAL_MENTOR_PASSWORD", "Mentor@123"
    )

    existing = fetch_all(
        "SELECT id FROM users WHERE username=?",
        (username,),
    )

    if not existing:
        execute("""
            INSERT INTO users
            (username, password_hash, full_name, role, created_at)
            VALUES (?, ?, ?, 'mentor', ?)
        """, (
            username,
            hash_password(password),
            "Placement Mentor",
            now(),
        ))


# =========================================================
# 6. COMMON BANNER
# =========================================================

def banner(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 7. LOGIN AND REGISTRATION
# =========================================================

def login_page():
    banner(
        "🎓 CSE Placement Roadmap & Mentorship Portal",
        "Learn, practise, receive mentorship and prepare for placements.",
    )

    _, center, _ = st.columns([1, 1.4, 1])

    with center:
        login_tab, student_tab, mentor_tab = st.tabs([
            "Sign In",
            "Student Registration",
            "Mentor Registration",
        ])

        # -------------------------------------------------
        # LOGIN
        # -------------------------------------------------

        with login_tab:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input(
                    "Password", type="password"
                )

                submit = st.form_submit_button(
                    "Sign In",
                    type="primary",
                    use_container_width=True,
                )

            if submit:
                if not username.strip() or not password:
                    st.error("Enter both username and password.")
                else:
                    users = fetch_all("""
                        SELECT * FROM users
                        WHERE username=? AND password_hash=?
                    """, (
                        username.strip(),
                        hash_password(password),
                    ))

                    if users:
                        st.session_state.user = users[0]
                        st.rerun()
                    else:
                        st.error(
                            "Invalid username or password. "
                            "Check your details and try again."
                        )

            st.info(
                "Default mentor login: "
                "**mentor** / **Mentor@123**"
            )

        # -------------------------------------------------
        # STUDENT REGISTRATION
        # -------------------------------------------------

        with student_tab:
            with st.form("student_registration"):
                name = st.text_input("Full Name")
                username = st.text_input("Create Username")

                password = st.text_input(
                    "Create Password", type="password"
                )

                confirm = st.text_input(
                    "Confirm Password", type="password"
                )

                year = st.selectbox("Academic Year", YEARS)

                branch = st.text_input(
                    "Branch",
                    value="Computer Science & Engineering",
                )

                submit = st.form_submit_button(
                    "Register as Student",
                    type="primary",
                    use_container_width=True,
                )

            if submit:
                if not name.strip() or not username.strip():
                    st.error("Name and username are required.")

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
                        execute("""
                            INSERT INTO users
                            (username, password_hash, full_name, role,
                             academic_year, branch, created_at)
                            VALUES (?, ?, ?, 'student', ?, ?, ?)
                        """, (
                            username.strip(),
                            hash_password(password),
                            name.strip(),
                            year,
                            branch.strip(),
                            now(),
                        ))

                        st.success(
                            "Student account created. You can now sign in."
                        )

                    except sqlite3.IntegrityError:
                        st.error(
                            "That username is already registered."
                        )

        # -------------------------------------------------
        # MENTOR REGISTRATION
        # -------------------------------------------------

        with mentor_tab:
            st.warning(
                "Mentor registration is enabled for this local demo. "
                "For a public deployment, require an administrator-issued "
                "invitation code before granting mentor access."
            )

            with st.form("mentor_registration"):
                name = st.text_input("Mentor Full Name")

                username = st.text_input(
                    "Create Mentor Username",
                    key="mentor_username",
                )

                password = st.text_input(
                    "Create Password",
                    type="password",
                    key="mentor_password",
                )

                confirm = st.text_input(
                    "Confirm Password",
                    type="password",
                    key="mentor_confirm",
                )

                submit = st.form_submit_button(
                    "Register as Mentor",
                    type="primary",
                    use_container_width=True,
                )

            if submit:
                if not name.strip() or not username.strip():
                    st.error(
                        "Mentor name and username are required."
                    )

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
                        execute("""
                            INSERT INTO users
                            (username, password_hash, full_name, role, created_at)
                            VALUES (?, ?, ?, 'mentor', ?)
                        """, (
                            username.strip(),
                            hash_password(password),
                            name.strip(),
                            now(),
                        ))

                        st.success(
                            "Mentor account created. Sign in using "
                            "your new account."
                        )

                    except sqlite3.IntegrityError:
                        st.error(
                            "That username is already registered."
                        )


# =========================================================
# 8. RESOURCES & TASKS
# =========================================================

def resources_tasks_page(user):
    banner(
        "📚 Resources & Tasks",
        "Learn, practise and track your placement preparation.",
    )

    user_year = user.get("academic_year", "First Year")

    year = st.selectbox(
        "Select Academic Year",
        list(ROADMAP.keys()),
        index=(
            list(ROADMAP.keys()).index(user_year)
            if user_year in ROADMAP else 0
        ),
        key="resources_academic_year",
    )

    categories = ROADMAP[year]

    # Use unique task keys for each academic year.
    all_tasks = [
        f"{year}:{category}:{task}"
        for category, task_list in categories.items()
        for task in task_list
    ]

    completed_rows = fetch_all("""
        SELECT task_key FROM tasks
        WHERE student_id=? AND completed=1
    """, (user["id"],))

    completed_set = {
        row["task_key"] for row in completed_rows
    }

    # Only count tasks belonging to the selected year.
    completed_count = sum(
        1 for task_key in all_tasks
        if task_key in completed_set
    )

    total_count = len(all_tasks)

    progress = min(
        1.0,
        max(
            0.0,
            completed_count / max(1, total_count),
        ),
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Completed Tasks",
        f"{completed_count}/{total_count}",
    )

    col2.metric(
        "Completion Progress",
        f"{progress * 100:.1f}%",
    )

    st.progress(progress)

    st.caption(
        f"Resources and tasks for {year}"
    )

    st.divider()

    for category, task_list in categories.items():
        st.markdown(f"### 📌 {category}")

        for task in task_list:
            task_key = f"{year}:{category}:{task}"

            is_completed = task_key in completed_set

            checked = st.checkbox(
                task,
                value=is_completed,
                key=f"task_{user['id']}_{task_key}",
            )

            if checked != is_completed:
                if checked:
                    execute("""
                        INSERT INTO tasks
                        (student_id, task_key, completed)
                        VALUES (?, ?, 1)
                        ON CONFLICT(student_id, task_key)
                        DO UPDATE SET completed=1
                    """, (
                        user["id"],
                        task_key,
                    ))

                else:
                    execute("""
                        DELETE FROM tasks
                        WHERE student_id=? AND task_key=?
                    """, (
                        user["id"],
                        task_key,
                    ))

                st.rerun()

        st.divider()
        # =========================================================
# 8. STUDENT DASHBOARD
# =========================================================

def student_dashboard(user):
    banner(
        f"Welcome back, {user['full_name']} 👋",
        "Track your learning progress and placement preparation.",
    )

    year = user.get("academic_year", "First Year")
    roadmap = ROADMAP.get(year, ROADMAP["First Year"])

    task_keys = [
        f"{year}:{category}:{task}"
        for category, tasks in roadmap.items()
        for task in tasks
    ]

    completed_rows = fetch_all("""
        SELECT task_key FROM tasks
        WHERE student_id=? AND completed=1
    """, (user["id"],))

    completed_set = {
        row["task_key"] for row in completed_rows
    }

    completed_count = sum(
        1 for key in task_keys if key in completed_set
    )
    total_count = len(task_keys)

    progress = min(
        1.0,
        max(
            0.0,
            completed_count / max(1, total_count),
        ),
    )

    question_count = count_rows("""
        SELECT COUNT(*) AS total
        FROM questions WHERE student_id=?
    """, (user["id"],))

    application_count = count_rows("""
        SELECT COUNT(*) AS total
        FROM applications WHERE student_id=?
    """, (user["id"],))

    a, b, c, d = st.columns(4)

    a.metric(
        "Completed Tasks",
        f"{completed_count}/{total_count}",
    )
    b.metric(
        "Learning Progress",
        f"{progress * 100:.1f}%",
    )
    c.metric("Mentor Questions", question_count)
    d.metric("Applications", application_count)

    st.subheader("Learning Progress")
    st.progress(progress)

    st.caption(
        f"Completed {completed_count} of {total_count} tasks for {year}."
    )

    if completed_count == total_count:
        st.success(
            "🎉 You completed all tasks for this academic year."
        )
    elif completed_count == 0:
        st.info(
            "Start completing tasks in Resources & Tasks."
        )
    elif progress < 0.5:
        st.warning(
            "Keep going. Follow your learning roadmap."
        )
    else:
        st.success(
            "Good progress. Continue with your remaining tasks."
        )

    left, right = st.columns(2)

    with left:
        st.subheader("Next Tasks")

        pending = [
            task
            for category, tasks in roadmap.items()
            for task in tasks
            if f"{year}:{category}:{task}" not in completed_set
        ]

        if pending:
            for task in pending[:5]:
                st.write("◻️", task)
        else:
            st.success(
                "All roadmap tasks are complete."
            )

    with right:
        st.subheader("Recent Applications")

        rows = fetch_all("""
            SELECT company, role, status, applied_at
            FROM applications
            WHERE student_id=?
            ORDER BY id DESC LIMIT 5
        """, (user["id"],))

        if rows:
            st.dataframe(
                pd.DataFrame(rows),
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info(
                "Start tracking your applications."
            )


# =========================================================
# 9. PLACEMENT READINESS ASSESSMENT
# =========================================================

def placement_readiness(user):
    banner(
        "🎯 Placement Readiness Prediction",
        "Enter your current preparation level to assess your readiness.",
    )

    st.write(
        "Rate each skill from **0 to 100**. "
        "Use realistic scores to identify areas for improvement."
    )

    left, right = st.columns(2, gap="large")

    with left:
        coding = st.slider(
            "Coding Score", 0, 100, 50
        )
        dsa = st.slider(
            "DSA Score", 0, 100, 50
        )
        technical = st.slider(
            "Technical Skills", 0, 100, 50
        )
        projects = st.slider(
            "Projects Score", 0, 100, 50
        )
        communication = st.slider(
            "Communication Score", 0, 100, 50
        )

    with right:
        aptitude = st.slider(
            "Aptitude Score", 0, 100, 50
        )

        internship = st.selectbox(
            "Internship Experience",
            ["No", "Yes"],
        )

        resume = st.slider(
            "Resume Score", 0, 100, 50
        )

        st.markdown("### Assessment Guide")
        st.write("**0–39:** Needs improvement")
        st.write("**40–59:** Developing")
        st.write("**60–79:** Good preparation")
        st.write("**80–100:** Strong preparation")

        st.info(
            "This is a rule-based preparation score, not a verified "
            "probability of being hired."
        )

    if st.button(
        "🔮 Predict Placement Readiness",
        type="primary",
        use_container_width=True,
    ):
        score = round(
            coding * 0.20
            + aptitude * 0.15
            + dsa * 0.20
            + technical * 0.20
            + resume * 0.10
            + projects * 0.10
            + communication * 0.05
            + (3 if internship == "Yes" else 0)
        )

        score = max(0, min(100, score))

        if score >= 80:
            result = "Strong Preparation"
            st.success(
                f"Placement readiness: {result}"
            )

        elif score >= 60:
            result = "Good Preparation"
            st.success(
                f"Placement readiness: {result}"
            )

        elif score >= 40:
            result = "Developing"
            st.warning(
                f"Placement readiness: {result}"
            )

        else:
            result = "Needs Improvement"
            st.error(
                f"Placement readiness: {result}"
            )

        col1, col2 = st.columns([1, 2])

        col1.metric(
            "Readiness Score",
            f"{score}/100",
        )

        col2.write(
            f"**Assessment:** {result}"
        )

        col2.progress(score / 100)

        scores = {
            "Coding": coding,
            "Aptitude": aptitude,
            "DSA": dsa,
            "Technical Skills": technical,
            "Resume": resume,
            "Projects": projects,
            "Communication": communication,
        }

        weak = [
            name
            for name, value in scores.items()
            if value < 40
        ]

        medium = [
            name
            for name, value in scores.items()
            if 40 <= value < 60
        ]

        st.subheader("Skill Analysis")

        if weak:
            st.error(
                "Priority areas: " + ", ".join(weak)
            )

        if medium:
            st.warning(
                "Practise more: " + ", ".join(medium)
            )

        if not weak and not medium:
            st.success(
                "Your entered skill scores are well balanced."
            )

        # Save assessment in database.
        execute("""
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
        """, (
            user["id"],
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
            now(),
        ))

        st.success(
            "Your assessment has been saved successfully."
        )

    # Previous assessment history.
    st.divider()
    st.subheader("Previous Assessment History")

    history = fetch_all("""
        SELECT
            coding,
            aptitude,
            dsa,
            technical,
            resume,
            projects,
            communication,
            score,
            result,
            created_at
        FROM assessments
        WHERE student_id=?
        ORDER BY id DESC
        LIMIT 10
    """, (user["id"],))

    if history:
        st.dataframe(
            pd.DataFrame(history),
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info(
            "You have not completed any assessments yet."
        )


# =========================================================
# 10. ASK MENTOR
# =========================================================

def ask_mentor_page(user):
    banner(
        "💬 Ask Your Mentor",
        "Ask questions and get guidance from your placement mentor.",
    )

    st.subheader("Submit a Question")

    with st.form("ask_mentor_form"):
        topic = st.selectbox(
            "Select Topic",
            [
                "Programming",
                "Data Structures & Algorithms",
                "Database / SQL",
                "Aptitude",
                "Resume",
                "Interview Preparation",
                "Projects",
                "Career Guidance",
                "Other",
            ],
        )

        question = st.text_area(
            "Write Your Question",
            placeholder="Type your question here...",
            height=130,
        )

        submit = st.form_submit_button(
            "Submit Question",
            type="primary",
            use_container_width=True,
        )

    if submit:
        if not question.strip():
            st.error(
                "Please enter your question."
            )
        else:
            execute("""
                INSERT INTO questions
                (student_id, question, topic, asked_at)
                VALUES (?, ?, ?, ?)
            """, (
                user["id"],
                question.strip(),
                topic,
                now(),
            ))

            st.success(
                "Your question has been submitted to the mentor."
            )

            st.rerun()

    st.divider()

    st.subheader("My Questions and Answers")

    questions = fetch_all("""
        SELECT
            q.id,
            q.question,
            q.topic,
            q.answer,
            q.asked_at,
            q.answered_at,
            u.full_name AS mentor_name
        FROM questions q
        LEFT JOIN users u ON q.mentor_id = u.id
        WHERE q.student_id=?
        ORDER BY q.id DESC
    """, (user["id"],))

    if not questions:
        st.info(
            "You have not submitted any questions yet."
        )

    for item in questions:
        with st.expander(
            f"Q{item['id']} — {item['topic']} "
            f"({item['asked_at']})"
        ):
            st.markdown("**Your Question:**")
            st.write(item["question"])

            if item["answer"]:
                st.success("Mentor's Answer")
                st.write(item["answer"])

                if item["mentor_name"]:
                    st.caption(
                        f"Answered by: {item['mentor_name']}"
                    )

                st.caption(
                    f"Answered at: {item['answered_at']}"
                )

            else:
                st.warning(
                    "Waiting for mentor response."
                )
                # =========================================================
# 11. STUDENT FEEDBACK
# =========================================================

def responses_feedback(user):
    banner(
        "⭐ Mentor Responses & Feedback",
        "Review responses and rate their usefulness.",
    )

    rows = fetch_all("""
        SELECT q.*, f.rating, f.comment
        FROM questions q
        LEFT JOIN feedback f ON f.question_id=q.id
        WHERE q.student_id=?
        ORDER BY q.id DESC
    """, (user["id"],))

    if not rows:
        st.info("You have not asked a question yet.")
        return

    for row in rows:
        with st.container(border=True):
            st.write("**Question:**", row["question"])

            if not row["answer"]:
                st.warning("Mentor response pending.")
                continue

            st.write("**Mentor Response:**", row["answer"])

            if row["rating"] is not None:
                st.success(f"Your rating: {row['rating']}/5")
                if row["comment"]:
                    st.write(row["comment"])
                continue

            with st.form(f"feedback-{row['id']}"):
                rating = st.slider(
                    "Rate the response",
                    1, 5, 5,
                    key=f"rating-{row['id']}",
                )
                comment = st.text_area(
                    "Comment (optional)",
                    key=f"comment-{row['id']}",
                )
                submit = st.form_submit_button("Submit Feedback")

            if submit:
                execute("""
                    INSERT INTO feedback
                    (question_id, student_id, rating, comment, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    row["id"], user["id"], rating,
                    comment.strip(), now(),
                ))

                st.success("Feedback submitted.")
                st.rerun()


# =========================================================
# 12. PLACEMENT TRACKER
# =========================================================

def placement_tracker(user):
    banner(
        "📋 Placement Tracker",
        "Track applications, interviews and offers.",
    )

    with st.form("application_form"):
        company = st.text_input("Company Name")
        role = st.text_input("Job Role")
        status = st.selectbox("Application Status", STATUSES)
        notes = st.text_input("Notes (optional)")
        submit = st.form_submit_button(
            "Add Application", type="primary"
        )

    if submit:
        if not company.strip() or not role.strip():
            st.error("Company and job role are required.")
        else:
            execute("""
                INSERT INTO applications
                (student_id, company, role, status, applied_at, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user["id"], company.strip(), role.strip(),
                status, now(), notes.strip(),
            ))

            st.success("Application added.")
            st.rerun()

    rows = fetch_all("""
        SELECT * FROM applications
        WHERE student_id=?
        ORDER BY id DESC
    """, (user["id"],))

    if not rows:
        st.info("No applications recorded yet.")
        return

    df = pd.DataFrame(rows)

    st.dataframe(
        df[["company", "role", "status", "applied_at", "notes"]],
        hide_index=True,
        use_container_width=True,
    )

    st.download_button(
        "Download Applications CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="placement_applications.csv",
        mime="text/csv",
    )

    with st.expander("Update or Delete Application"):
        choices = {
            f"#{row['id']} — {row['company']} / {row['role']}": row
            for row in rows
        }

        label = st.selectbox(
            "Select Application", list(choices.keys())
        )
        selected = choices[label]

        new_status = st.selectbox(
            "New Status",
            STATUSES,
            index=(
                STATUSES.index(selected["status"])
                if selected["status"] in STATUSES else 0
            ),
        )

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Save Status"):
                execute("""
                    UPDATE applications SET status=?
                    WHERE id=? AND student_id=?
                """, (
                    new_status, selected["id"], user["id"]
                ))
                st.success("Status updated.")
                st.rerun()

        with c2:
            if st.button("Delete Application"):
                execute("""
                    DELETE FROM applications
                    WHERE id=? AND student_id=?
                """, (selected["id"], user["id"]))

                st.success("Application deleted.")
                st.rerun()


# =========================================================
# 13. MENTOR DASHBOARD
# =========================================================

def mentor_dashboard(user):
    banner(
        f"Welcome, {user['full_name']}",
        "Manage student questions, feedback and placement outcomes.",
    )

    students = count_rows(
        "SELECT COUNT(*) AS total FROM users WHERE role='student'"
    )
    questions = count_rows(
        "SELECT COUNT(*) AS total FROM questions"
    )
    pending = count_rows(
        "SELECT COUNT(*) AS total FROM questions WHERE answer=''"
    )
    offers = count_rows("""
        SELECT COUNT(*) AS total FROM applications
        WHERE status IN ('Selected', 'Offer Received')
    """)

    a, b, c, d = st.columns(4)
    a.metric("Students", students)
    b.metric("Questions", questions)
    c.metric("Pending Replies", pending)
    d.metric("Selections / Offers", offers)

    st.subheader("Recent Student Questions")

    rows = fetch_all("""
        SELECT u.full_name, q.topic, q.question, q.asked_at
        FROM questions q
        JOIN users u ON u.id=q.student_id
        ORDER BY q.id DESC LIMIT 10
    """)

    if rows:
        st.dataframe(
            pd.DataFrame(rows),
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("No student questions yet.")


def mentor_questions(user):
    banner(
        "📨 Student Questions",
        "Read questions and provide mentor responses.",
    )

    rows = fetch_all("""
        SELECT q.*, u.full_name
        FROM questions q
        JOIN users u ON u.id=q.student_id
        ORDER BY q.id DESC
    """)

    if not rows:
        st.info("No student questions yet.")
        return

    for row in rows:
        with st.expander(
            f"{row['full_name']} — Question #{row['id']}"
        ):
            st.write("**Topic:**", row["topic"])
            st.write(row["question"])

            with st.form(f"mentor-answer-{row['id']}"):
                answer = st.text_area(
                    "Mentor Response",
                    value=row["answer"] or "",
                    key=f"answer-{row['id']}",
                )
                submit = st.form_submit_button("Save Response")

            if submit:
                if not answer.strip():
                    st.error("Response cannot be empty.")
                else:
                    execute("""
                        UPDATE questions
                        SET answer=?, mentor_id=?, answered_at=?
                        WHERE id=?
                    """, (
                        answer.strip(), user["id"],
                        now(), row["id"]
                    ))

                    st.success("Response saved.")
                    st.rerun()


def mentor_feedback():
    banner(
        "⭐ Student Feedback",
        "Review student ratings and comments.",
    )

    rows = fetch_all("""
        SELECT u.full_name, q.question, f.rating,
               f.comment, f.created_at
        FROM feedback f
        JOIN users u ON u.id=f.student_id
        JOIN questions q ON q.id=f.question_id
        ORDER BY f.id DESC
    """)

    if not rows:
        st.info("No feedback submitted yet.")
        return

    average = sum(row["rating"] for row in rows) / len(rows)
    st.metric("Average Rating", f"{average:.1f}/5")

    st.dataframe(
        pd.DataFrame(rows),
        hide_index=True,
        use_container_width=True,
    )


def mentor_outcomes():
    banner(
        "🎯 Placement Outcomes",
        "Review student applications and outcomes.",
    )

    rows = fetch_all("""
        SELECT u.full_name, a.company, a.role,
               a.status, a.applied_at, a.notes
        FROM applications a
        JOIN users u ON u.id=a.student_id
        ORDER BY a.id DESC
    """)

    if not rows:
        st.info("No placement applications recorded yet.")
        return

    df = pd.DataFrame(rows)

    statuses = ["All"] + sorted(
        df["status"].dropna().unique().tolist()
    )

    selected = st.selectbox("Filter Status", statuses)

    if selected != "All":
        df = df[df["status"] == selected]

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
    )

    st.download_button(
        "Download Placement Outcomes CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="placement_outcomes.csv",
        mime="text/csv",
    )
    # =========================================================
# 14. CONNECT ASK MENTOR PAGE
# =========================================================

def ask_mentor(user):
    ask_mentor_page(user)


# =========================================================
# 15. MAIN APPLICATION AND NAVIGATION
# =========================================================

def main():
    # Initialize database and default mentor account.
    setup_database()
    create_default_mentor()

    user = st.session_state.get("user")

    # Show login page if the user is not logged in.
    if user is None:
        login_page()
        return

    # -----------------------------------------------------
    # SIDEBAR NAVIGATION
    # -----------------------------------------------------

    with st.sidebar:
        st.markdown("## 🎓 CSE PLACEMENT PORTAL")

        st.write(f"**{user['full_name']}**")
        st.caption(user["role"].upper())

        st.divider()

        if user["role"] == "mentor":

            pages = [
                "Dashboard",
                "Student Questions",
                "Student Feedback",
                "Placement Outcomes",
            ]

        else:

            pages = [
                "Dashboard",
                "Resources & Tasks",
                "Placement Readiness Assessment",
                "Ask a Mentor",
                "Mentor Responses & Feedback",
                "Placement Tracker",
            ]

        page = st.radio(
            "Navigation",
            pages,
            label_visibility="collapsed",
        )

        st.divider()

        # -------------------------------------------------
        # LOGOUT
        # -------------------------------------------------

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):
            st.session_state.pop("user", None)
            st.rerun()

    # -----------------------------------------------------
    # MENTOR PAGES
    # -----------------------------------------------------

    if user["role"] == "mentor":

        routes = {
            "Dashboard": lambda: mentor_dashboard(user),

            "Student Questions":
                lambda: mentor_questions(user),

            "Student Feedback":
                mentor_feedback,

            "Placement Outcomes":
                mentor_outcomes,
        }

    # -----------------------------------------------------
    # STUDENT PAGES
    # -----------------------------------------------------

    else:

        routes = {
            "Dashboard":
                lambda: student_dashboard(user),

            "Resources & Tasks":
                lambda: resources_tasks_page(user),

            "Placement Readiness Assessment":
                lambda: placement_readiness(user),

            "Ask a Mentor":
                lambda: ask_mentor(user),

            "Mentor Responses & Feedback":
                lambda: responses_feedback(user),

            "Placement Tracker":
                lambda: placement_tracker(user),
        }

    # Display selected page.
    routes[page]()


# =========================================================
# 16. APPLICATION ENTRY POINT AND ERROR HANDLING
# =========================================================

if __name__ == "__main__":

    try:
        main()

    except sqlite3.Error as error:

        print(traceback.format_exc())

        st.error("A database error occurred.")

        st.code(str(error))

        st.warning(
            "Back up your database before attempting database changes."
        )

    except Exception as error:

        print(traceback.format_exc())

        st.error(
            "The application encountered an unexpected error."
        )

        st.code(
            f"{type(error).__name__}: {error}"
        )

        st.info(
            "The full error traceback has been written "
            "to the application logs."
        )
