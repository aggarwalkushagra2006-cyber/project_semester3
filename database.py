"""
Database management for Job & Internship Portal using SQLite3.
Handles schema initialization, CRUD operations, and pre-seeded sample data.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portal.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database schema if tables do not exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT DEFAULT 'candidate',
        title TEXT,
        headline TEXT,
        bio TEXT,
        skills TEXT,
        experience_level TEXT,
        education TEXT,
        preferred_type TEXT,
        resume_text TEXT,
        avatar_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recruiter_id INTEGER,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        company_logo TEXT,
        location TEXT NOT NULL,
        is_remote INTEGER DEFAULT 0,
        job_type TEXT NOT NULL,
        category TEXT NOT NULL,
        experience_level TEXT NOT NULL,
        stipend_or_salary TEXT NOT NULL,
        required_skills TEXT NOT NULL,
        optional_skills TEXT,
        description TEXT NOT NULL,
        responsibilities TEXT,
        requirements TEXT,
        perks TEXT,
        deadline TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(recruiter_id) REFERENCES users(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER NOT NULL,
        candidate_id INTEGER NOT NULL,
        cover_letter TEXT,
        match_score INTEGER,
        status TEXT DEFAULT 'Applied',
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(job_id) REFERENCES jobs(id),
        FOREIGN KEY(candidate_id) REFERENCES users(id),
        UNIQUE(job_id, candidate_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        job_id INTEGER NOT NULL,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, job_id)
    );
    """)

    conn.commit()
    conn.close()


def seed_sample_data(force=False):
    """Populates realistic candidates and job/internship listings."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs;")
    count = cursor.fetchone()[0]
    if count > 0 and not force:
        conn.close()
        return

    if force:
        cursor.execute("DELETE FROM applications;")
        cursor.execute("DELETE FROM saved_jobs;")
        cursor.execute("DELETE FROM jobs;")
        cursor.execute("DELETE FROM users;")

    candidates = [
        (
            1, "Aarav Patel", "aarav.patel@example.com", "candidate",
            "Aspiring Machine Learning & Data Science Engineer",
            "Computer Science Senior passionate about predictive modeling, NLP, and deep neural networks.",
            "Skilled in Python, PyTorch, Scikit-learn, and SQL. Completed capstone on transformer sentiment analysis. Looking for summer AI/ML research internships or junior data engineering roles.",
            "python, machine learning, scikit-learn, pandas, numpy, sql, pytorch, deep learning, git",
            "Fresher / Student",
            "B.Tech in Computer Science & Engineering, Expected 2026",
            "Internship",
            "Experienced with building end-to-end ML pipelines in Python using Scikit-Learn and PyTorch. Built NLP recommendation system with TF-IDF and transformer embeddings. Proficient in SQL querying and data wrangling with Pandas and NumPy. Active GitHub contributor.",
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"
        ),
        (
            2, "Sophia Rodriguez", "sophia.rodriguez@example.com", "candidate",
            "Frontend & React Developer",
            "Creative frontend developer passionate about accessible web experiences, responsive UI, and TypeScript.",
            "Specialized in modern JavaScript/TypeScript, React 18, Tailwind CSS, and Next.js. Built 5+ production-grade web applications with modern state management.",
            "javascript, typescript, react, tailwind, html, css, next.js, git, figma, rest api",
            "1-2 Years",
            "B.S. in Web Development & Design, 2025",
            "Full-time",
            "Frontend engineer with deep knowledge of React component lifecycle, Tailwind CSS styling, TypeScript typings, and REST API consumption. Familiar with modern bundle tools and Figma-to-code workflows.",
            "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80"
        ),
        (
            3, "Marcus Vance", "marcus.vance@example.com", "candidate",
            "Full-Stack Software Engineer",
            "Hands-on builder proficient in Python backends, Node.js microservices, Docker, and PostgreSQL.",
            "Experienced with FastAPI, Flask, PostgreSQL, Docker, Redis, and React. Passionate about scalable architecture and clean code standards.",
            "python, flask, fastapi, sql, postgresql, docker, git, rest api, nodejs, linux",
            "1-2 Years",
            "B.S. in Software Engineering, 2024",
            "Any",
            "Full-stack engineer skilled in building RESTful APIs using Python Flask/FastAPI and Node.js. Experience with relational databases (PostgreSQL), Docker containerization, and automated CI/CD pipelines.",
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80"
        ),
        (
            4, "Priya Sharma", "priya.sharma@example.com", "candidate",
            "Product & UI/UX Designer",
            "User-centered designer obsessed with wireframing, design systems, and delightful user journeys.",
            "Proficient in Figma, user research, rapid prototyping, design tokens, HTML/CSS principles, and usability testing.",
            "figma, ui/ux, user research, wireframing, prototyping, design systems, html, css",
            "Fresher / Student",
            "B.Des in Interaction Design, Expected 2026",
            "Internship",
            "Design intern candidate skilled in Figma component libraries, user empathy mapping, mobile-first design, interactive prototyping, and developer handoffs.",
            "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80"
        ),
        (
            5, "Tech recruiter", "recruiter@innovatetech.com", "recruiter",
            "Senior Talent Acquisition Partner",
            "Hiring the next generation of engineers, designers, and data pioneers.",
            "Specialized in tech hiring for fast-paced growth startups.",
            "recruiting, talent acquisition, interviewing",
            "5+ Years",
            "MBA in Human Resources",
            "Full-time",
            "",
            "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80"
        )
    ]

    cursor.executemany("""
    INSERT INTO users (id, name, email, role, title, headline, bio, skills, experience_level, education, preferred_type, resume_text, avatar_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, candidates)

    jobs = [
        (
            1, 5,
            "AI / Machine Learning Engineering Intern",
            "NeuralScale AI",
            "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=120&auto=format&fit=crop&q=80",
            "San Francisco, CA (or Remote)",
            1,
            "Internship",
            "Data & AI",
            "Fresher / Student",
            "$45 - $55 / hr",
            "python, machine learning, scikit-learn, pytorch, pandas, numpy",
            "sql, git, docker, deep learning, nlp",
            "Join our core AI research and applications team to build and evaluate predictive models, recommendation algorithms, and fine-tune open-source LLMs.",
            "Develop and test ML models using PyTorch and Scikit-learn; Clean, vectorize, and evaluate tabular and unstructured text datasets; Collaborate with senior engineers on model deployment.",
            "Solid proficiency in Python programming; Understanding of machine learning concepts (supervised/unsupervised learning, gradient descent, loss functions); Hands-on experience with Pandas/NumPy.",
            "Flexible remote work, 1-on-1 mentorship from ex-Google researchers, monthly tech stipend, return full-time offer potential.",
            "2026-11-30"
        ),
        (
            2, 5,
            "Junior Data Scientist / Analyst",
            "DataPulse Analytics",
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=120&auto=format&fit=crop&q=80",
            "New York, NY (Hybrid)",
            0,
            "Full-time",
            "Data & AI",
            "Fresher / Student",
            "$80,000 - $95,000 / yr",
            "python, sql, pandas, scikit-learn, data analysis",
            "machine learning, tableau, git, statistics",
            "We are seeking an inquisitive Junior Data Scientist to translate complex user behavior data into actionable product and business insights.",
            "Write complex SQL queries to extract data from data warehouses; Build statistical regression and classification models in Python; Construct interactive dashboards for stakeholders.",
            "Degree in Computer Science, Statistics, Mathematics, or equivalent; Proficiency with Python and SQL; Familiarity with predictive modeling and exploratory data analysis.",
            "Comprehensive healthcare, 401(k) matching, $2,000 annual learning budget, free catered lunches.",
            "2026-12-15"
        ),
        (
            3, 5,
            "Frontend React Developer Intern",
            "VividWeb Studio",
            "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=120&auto=format&fit=crop&q=80",
            "Remote",
            1,
            "Internship",
            "Software Engineering",
            "Fresher / Student",
            "$30 - $40 / hr",
            "react, javascript, tailwind, html, css",
            "typescript, next.js, git, figma",
            "We are looking for an enthusiastic Frontend Intern to craft sleek, responsive, and accessible user interfaces for our customer portal.",
            "Implement pixel-perfect web pages from Figma designs; Build reusable React components with Tailwind CSS; Optimize client-side performance and accessibility.",
            "Strong fundamentals in JavaScript (ES6+), HTML5, and CSS3; Hands-on experience with React; Passion for clean UI and micro-interactions.",
            "100% remote flexibility, equipment stipend, code review mentorship, sponsorship for web conferences.",
            "2026-10-31"
        ),
        (
            4, 5,
            "Software Engineer - Frontend (React / TypeScript)",
            "CloudSphere Systems",
            "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=120&auto=format&fit=crop&q=80",
            "Austin, TX (Hybrid)",
            0,
            "Full-time",
            "Software Engineering",
            "1-2 Years",
            "$95,000 - $115,000 / yr",
            "react, typescript, javascript, tailwind, rest api",
            "next.js, git, unit testing, docker",
            "CloudSphere is expanding its enterprise dashboard team. You will be responsible for creating data-dense, real-time dashboards used by thousands of IT teams worldwide.",
            "Architect and maintain modular React & TypeScript components; Integrate REST and WebSocket APIs; Write unit and integration tests to ensure rock-solid stability.",
            "1+ years experience building production React applications; Strong proficiency in TypeScript; Experience with modern state management and API integration.",
            "Stock options, unlimited PTO, health/dental/vision, home office setup budget.",
            "2026-11-15"
        ),
        (
            5, 5,
            "Full-Stack Python & React Engineer",
            "OmniFlow Technologies",
            "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=120&auto=format&fit=crop&q=80",
            "Remote (US / Global)",
            1,
            "Full-time",
            "Software Engineering",
            "1-2 Years",
            "$100,000 - $125,000 / yr",
            "python, react, fastapi, sql, postgresql",
            "docker, git, rest api, tailwind, redis",
            "Looking for an agile Full-Stack Engineer who enjoys moving across the entire stack—from developing high-throughput Python REST endpoints to polished React frontends.",
            "Design and build RESTful microservices with FastAPI/Flask; Model efficient relational schemas with PostgreSQL; Collaborate on frontend features using React and Tailwind.",
            "Solid experience with Python web frameworks (FastAPI, Flask, or Django); Experience with React and modern frontend toolchains; Working knowledge of SQL and Docker.",
            "Competitive equity, flexible hours, annual company retreats in Europe, health insurance.",
            "2026-12-01"
        ),
        (
            6, 5,
            "Backend Python Developer Intern",
            "DataGrid Labs",
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=120&auto=format&fit=crop&q=80",
            "Seattle, WA (or Remote)",
            1,
            "Internship",
            "Software Engineering",
            "Fresher / Student",
            "$35 - $45 / hr",
            "python, flask, sql, rest api, git",
            "docker, postgresql, linux, unit testing",
            "Kickstart your backend engineering career! You will work closely with senior systems architects to build scalable APIs and database queries.",
            "Write clean, testable Python backend services; Implement database migrations and query optimization; Document REST API endpoints.",
            "Enthusiastic student or recent graduate in Computer Science; Strong grasp of Python data structures and algorithms; Basic familiarity with relational databases and SQL.",
            "Dedicated senior mentor, high probability of conversion to full-time SWE, gaming and social events.",
            "2026-11-20"
        ),
        (
            7, 5,
            "Product & UI/UX Design Intern",
            "Aura Creative Labs",
            "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=120&auto=format&fit=crop&q=80",
            "Remote",
            1,
            "Internship",
            "UI/UX Design",
            "Fresher / Student",
            "$28 - $36 / hr",
            "figma, ui/ux, wireframing, prototyping, user research",
            "design systems, html, css",
            "Aura Creative is looking for a thoughtful UI/UX Design Intern who can turn complex workflows into simple, elegant, and intuitive digital experiences.",
            "Conduct qualitative user interviews and usability tests; Create wireframes, user flows, and high-fidelity clickable prototypes in Figma; Contribute to our unified design system.",
            "Demonstrated portfolio of design projects (academic or personal); Proficiency with Figma; Strong understanding of layout, typography, and visual hierarchy.",
            "Figma subscription covered, direct collaboration with founding designers, career portfolio coaching.",
            "2026-10-25"
        ),
        (
            8, 5,
            "DevOps & Cloud Engineering Intern",
            "InfraCloud Automation",
            "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=120&auto=format&fit=crop&q=80",
            "Chicago, IL (Hybrid)",
            0,
            "Internship",
            "DevOps & Cloud",
            "Fresher / Student",
            "$32 - $42 / hr",
            "docker, linux, git, python, cicd",
            "kubernetes, aws, bash, terraform",
            "Are you curious about how massive web applications stay online 99.99% of the time? Join our Cloud Infrastructure team to automate CI/CD and container workflows.",
            "Maintain Docker container builds; Write Bash and Python automation scripts; Assist in setting up GitHub Actions CI/CD pipelines.",
            "Familiarity with Linux command line environments; Basic understanding of Docker containers and Git version control; Eagerness to learn AWS / Kubernetes.",
            "Free AWS certification exam vouchers, modern workstation setup, hybrid schedule flexibility.",
            "2026-11-10"
        ),
        (
            9, 5,
            "Natural Language Processing (NLP) Research Intern",
            "CognitiveCore Labs",
            "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=120&auto=format&fit=crop&q=80",
            "Boston, MA (or Remote)",
            1,
            "Internship",
            "Data & AI",
            "Fresher / Student",
            "$48 - $60 / hr",
            "python, pytorch, nlp, machine learning, deep learning",
            "transformers, scikit-learn, git",
            "Conduct exploratory research on agentic workflows, prompt alignment, and retrieval-augmented generation (RAG) pipelines for enterprise knowledge search.",
            "Implement text similarity, tokenization, and vector search embeddings; Benchmark transformer models against standard NLP datasets; Document experiment findings.",
            "Strong mathematical foundation in linear algebra and probability; Hands-on coding experience with PyTorch; Familiarity with NLP concepts.",
            "Publish research papers at top AI workshops, compute credits on H100 GPU clusters, competitive stipend.",
            "2026-12-05"
        ),
        (
            10, 5,
            "Product Management Intern",
            "NextGen Horizons",
            "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=120&auto=format&fit=crop&q=80",
            "San Francisco, CA (Hybrid)",
            0,
            "Internship",
            "Product Management",
            "Fresher / Student",
            "$35 - $45 / hr",
            "product management, agile, scrum, data analysis, user research",
            "sql, figma, jira",
            "Work alongside product leaders to define product specs, analyze user metrics, and prioritize sprint backlogs for consumer mobile and web applications.",
            "Gather user feedback and synthesize requirements into clear user stories; Analyze product analytics funnels; Coordinate with engineering and design teams during sprint cycles.",
            "Strong communication and critical thinking skills; Passion for tech products and customer empathy; Basic analytical ability with spreadsheets or SQL.",
            "Mentorship from former Big-Tech PMs, lunch and learns, networking sessions.",
            "2026-11-28"
        )
    ]

    cursor.executemany("""
    INSERT INTO jobs (id, recruiter_id, title, company, company_logo, location, is_remote, job_type, category, experience_level, stipend_or_salary, required_skills, optional_skills, description, responsibilities, requirements, perks, deadline)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, jobs)

    applications = [
        (1, 1, 1, "I have built several ML projects using PyTorch and Scikit-Learn and would love to contribute to NeuralScale's research.", 94, "Shortlisted"),
        (2, 2, 1, "Very eager to apply my data wrangling and predictive modeling skills to real-world datasets.", 82, "Under Review"),
        (3, 3, 2, "I love React and Tailwind CSS and would be thrilled to bring my frontend expertise to VividWeb Studio.", 91, "Interviewing")
    ]

    cursor.executemany("""
    INSERT INTO applications (id, job_id, candidate_id, cover_letter, match_score, status)
    VALUES (?, ?, ?, ?, ?, ?);
    """, applications)

    cursor.execute("""
    INSERT OR IGNORE INTO saved_jobs (user_id, job_id) VALUES (1, 1), (1, 9);
    """)

    conn.commit()
    conn.close()


def get_candidates():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role = 'candidate' ORDER BY id ASC;")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_candidate(candidate_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?;", (candidate_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_candidate(candidate_id, data):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users SET
        name = ?,
        title = ?,
        headline = ?,
        bio = ?,
        skills = ?,
        experience_level = ?,
        education = ?,
        preferred_type = ?,
        resume_text = ?
    WHERE id = ?;
    """, (
        data.get("name"),
        data.get("title"),
        data.get("headline"),
        data.get("bio"),
        data.get("skills"),
        data.get("experience_level"),
        data.get("education"),
        data.get("preferred_type"),
        data.get("resume_text"),
        candidate_id
    ))
    conn.commit()
    conn.close()


def get_all_jobs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY id DESC;")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_job(job_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?;", (job_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def create_job(data):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO jobs (
        recruiter_id, title, company, company_logo, location, is_remote,
        job_type, category, experience_level, stipend_or_salary,
        required_skills, optional_skills, description, responsibilities,
        requirements, perks, deadline
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        data.get("recruiter_id", 5),
        data.get("title"),
        data.get("company"),
        data.get("company_logo", "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=120&auto=format&fit=crop&q=80"),
        data.get("location"),
        1 if data.get("is_remote") in [1, True, "1", "true", "on"] else 0,
        data.get("job_type", "Internship"),
        data.get("category", "Software Engineering"),
        data.get("experience_level", "Fresher / Student"),
        data.get("stipend_or_salary", "Competitive"),
        data.get("required_skills"),
        data.get("optional_skills", ""),
        data.get("description"),
        data.get("responsibilities", ""),
        data.get("requirements", ""),
        data.get("perks", ""),
        data.get("deadline", "Open Until Filled")
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def apply_to_job(job_id, candidate_id, cover_letter="", match_score=0):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO applications (job_id, candidate_id, cover_letter, match_score, status)
        VALUES (?, ?, ?, ?, 'Applied');
        """, (job_id, candidate_id, cover_letter, match_score))
        conn.commit()
        success = True
        msg = "Application submitted successfully!"
    except sqlite3.IntegrityError:
        success = False
        msg = "You have already applied for this position."
    conn.close()
    return success, msg


def get_candidate_applications(candidate_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT a.*, j.title, j.company, j.location, j.job_type, j.stipend_or_salary, j.is_remote
    FROM applications a
    JOIN jobs j ON a.job_id = j.id
    WHERE a.candidate_id = ?
    ORDER BY a.applied_at DESC;
    """, (candidate_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_job_applications(job_id=None):
    conn = get_db()
    cursor = conn.cursor()
    if job_id:
        cursor.execute("""
        SELECT a.*, u.name as candidate_name, u.email as candidate_email, u.title as candidate_title,
               u.skills as candidate_skills, u.experience_level as candidate_experience,
               u.avatar_url as candidate_avatar, j.title as job_title, j.company as job_company
        FROM applications a
        JOIN users u ON a.candidate_id = u.id
        JOIN jobs j ON a.job_id = j.id
        WHERE a.job_id = ?
        ORDER BY a.match_score DESC, a.applied_at DESC;
        """, (job_id,))
    else:
        cursor.execute("""
        SELECT a.*, u.name as candidate_name, u.email as candidate_email, u.title as candidate_title,
               u.skills as candidate_skills, u.experience_level as candidate_experience,
               u.avatar_url as candidate_avatar, j.title as job_title, j.company as job_company
        FROM applications a
        JOIN users u ON a.candidate_id = u.id
        JOIN jobs j ON a.job_id = j.id
        ORDER BY a.applied_at DESC;
        """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def update_application_status(app_id, new_status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE applications SET status = ? WHERE id = ?;
    """, (new_status, app_id))
    conn.commit()
    conn.close()


def toggle_saved_job(user_id, job_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM saved_jobs WHERE user_id = ? AND job_id = ?;", (user_id, job_id))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("DELETE FROM saved_jobs WHERE user_id = ? AND job_id = ?;", (user_id, job_id))
        saved = False
    else:
        cursor.execute("INSERT INTO saved_jobs (user_id, job_id) VALUES (?, ?);", (user_id, job_id))
        saved = True
    conn.commit()
    conn.close()
    return saved


def get_saved_job_ids(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT job_id FROM saved_jobs WHERE user_id = ?;", (user_id,))
    ids = [r[0] for r in cursor.fetchall()]
    conn.close()
    return set(ids)
