"""
Recommendation Engine for Job & Internship Portal
Combines:
1. Normalized Skill Overlap (Required vs Optional)
2. Content-based Semantic Cosine Similarity (TF-IDF on candidate resume/bio vs job descriptions)
3. Experience & Job-Type Compatibility
4. Explainable Match Breakdown (Matched skills, Missing skills, Skill gap recommendations)
Includes pure-Python fallback if scikit-learn is not installed.
"""

import re
import math
from collections import Counter

# Try importing scikit-learn, otherwise use robust pure-Python fallback
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# Skill synonym mapping to normalize candidate and job skills
SKILL_SYNONYMS = {
    "react.js": "react",
    "reactjs": "react",
    "vue.js": "vue",
    "vuejs": "vue",
    "angular.js": "angular",
    "angularjs": "angular",
    "node.js": "nodejs",
    "node": "nodejs",
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "python3": "python",
    "golang": "go",
    "k8s": "kubernetes",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "aws": "amazon web services",
    "gcp": "google cloud",
    "azure": "microsoft azure",
    "rest": "rest api",
    "restful api": "rest api",
    "ci/cd": "cicd",
    "ci cd": "cicd",
    "docker": "docker",
    "git": "git",
    "github": "git",
    "html5": "html",
    "css3": "css",
}

# Standard technology vocabulary for skill extraction
KNOWN_TECH_SKILLS = [
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "php", "ruby", "swift", "kotlin", "scala",
    "react", "vue", "angular", "next.js", "svelte", "html", "css", "tailwind", "bootstrap", "sass",
    "nodejs", "express", "django", "flask", "fastapi", "spring boot", "asp.net", "laravel", "rails",
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "cassandra", "elasticsearch", "firebase",
    "docker", "kubernetes", "aws", "gcp", "azure", "linux", "git", "cicd", "terraform", "ansible",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "data analysis", "data science", "tableau", "power bi", "hadoop", "spark",
    "figma", "ui/ux", "user research", "wireframing", "prototyping", "product management", "agile", "scrum",
    "rest api", "graphql", "microservices", "unit testing", "cybersecurity", "penetration testing"
]


def normalize_skill(skill_str):
    """Normalize a single skill string."""
    if not skill_str:
        return ""
    clean = skill_str.strip().lower()
    return SKILL_SYNONYMS.get(clean, clean)


def parse_skill_list(skills_input):
    """Convert string (comma-separated or JSON) or list into a normalized set of skills."""
    if not skills_input:
        return set()
    if isinstance(skills_input, (list, tuple, set)):
        items = skills_input
    elif isinstance(skills_input, str):
        items = [s.strip() for s in re.split(r"[,;]+", skills_input) if s.strip()]
    else:
        items = []
    
    normalized = set()
    for item in items:
        norm = normalize_skill(item)
        if norm:
            normalized.add(norm)
    return normalized


def extract_skills_from_text(text):
    """Extract known technical skills automatically from raw text/resume."""
    if not text:
        return []
    text_lower = " " + text.lower() + " "
    found = set()

    for skill in KNOWN_TECH_SKILLS:
        pattern = r"(?:\b|_)" + re.escape(skill) + r"(?:\b|_)"
        if re.search(pattern, text_lower):
            found.add(skill)

    for syn, canonical in SKILL_SYNONYMS.items():
        pattern = r"(?:\b|_)" + re.escape(syn) + r"(?:\b|_)"
        if re.search(pattern, text_lower):
            found.add(canonical)

    return sorted(list(found))


def tokenize_text(text):
    """Simple alphanumeric tokenizer."""
    if not text:
        return []
    words = re.findall(r"\b[a-zA-Z0-9+#.-]{2,}\b", text.lower())
    stop_words = {
        "and", "the", "to", "of", "in", "a", "is", "for", "with", "on", "as", "at", "by", "an",
        "be", "this", "which", "or", "from", "are", "we", "you", "our", "will", "all", "your",
        "that", "can", "work", "role", "team", "looking", "have", "has", "who", "into"
    }
    return [w for w in words if w not in stop_words]


def compute_pure_cosine_similarity(text1, text2):
    """Calculate TF-IDF Cosine Similarity between two text documents in pure Python."""
    tokens1 = tokenize_text(text1)
    tokens2 = tokenize_text(text2)

    if not tokens1 or not tokens2:
        return 0.0

    tf1 = Counter(tokens1)
    tf2 = Counter(tokens2)
    all_words = set(tf1.keys()).union(set(tf2.keys()))

    idf = {}
    for word in all_words:
        doc_count = (1 if word in tf1 else 0) + (1 if word in tf2 else 0)
        idf[word] = math.log((2.0 + 1) / (doc_count + 1)) + 1.0

    vec1 = {}
    vec2 = {}
    for word in all_words:
        vec1[word] = (tf1.get(word, 0) / len(tokens1)) * idf[word]
        vec2[word] = (tf2.get(word, 0) / len(tokens2)) * idf[word]

    dot = sum(vec1[w] * vec2[w] for w in all_words)
    norm1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

    if norm1 == 0 or norm2 == 0:
        return 0.0
    return max(0.0, min(1.0, dot / (norm1 * norm2)))


def compute_text_similarity(candidate_text, job_text):
    """Compute text similarity using scikit-learn or pure Python fallback."""
    if not candidate_text or not job_text:
        return 0.0

    if SKLEARN_AVAILABLE:
        try:
            vectorizer = TfidfVectorizer(stop_words='english', token_pattern=r'(?u)\b\w+\b')
            matrix = vectorizer.fit_transform([candidate_text, job_text])
            score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
            return float(max(0.0, min(1.0, score)))
        except Exception:
            return compute_pure_cosine_similarity(candidate_text, job_text)
    else:
        return compute_pure_cosine_similarity(candidate_text, job_text)


def compute_match_score(candidate, job):
    cand_skills = parse_skill_list(candidate.get("skills", ""))
    job_req_skills = parse_skill_list(job.get("required_skills", ""))
    job_opt_skills = parse_skill_list(job.get("optional_skills", ""))

    matched_req = cand_skills.intersection(job_req_skills)
    missing_req = job_req_skills.difference(cand_skills)
    matched_opt = cand_skills.intersection(job_opt_skills)

    if job_req_skills:
        req_ratio = len(matched_req) / len(job_req_skills)
    else:
        req_ratio = 1.0

    if job_opt_skills:
        opt_ratio = len(matched_opt) / len(job_opt_skills)
    else:
        opt_ratio = 0.5

    skill_score = (req_ratio * 0.8 + opt_ratio * 0.2) * 100.0

    cand_content = " ".join([
        str(candidate.get("title", "")),
        str(candidate.get("headline", "")),
        str(candidate.get("bio", "")),
        str(candidate.get("resume_text", "")),
        " ".join(cand_skills)
    ])

    job_content = " ".join([
        str(job.get("title", "")),
        str(job.get("description", "")),
        str(job.get("requirements", "")),
        str(job.get("category", "")),
        " ".join(job_req_skills),
        " ".join(job_opt_skills)
    ])

    semantic_sim = compute_text_similarity(cand_content, job_content)
    semantic_score = semantic_sim * 100.0

    pref_score = 70.0
    cand_type = str(candidate.get("preferred_type", "")).lower()
    job_type = str(job.get("job_type", "")).lower()

    if cand_type and job_type:
        if cand_type in job_type or job_type in cand_type:
            pref_score += 20.0
        elif ("intern" in cand_type and "intern" in job_type):
            pref_score += 20.0
        elif ("full" in cand_type and "full" in job_type):
            pref_score += 20.0

    cand_exp = str(candidate.get("experience_level", "")).lower()
    job_exp = str(job.get("experience_level", "")).lower()
    if cand_exp and job_exp:
        if cand_exp in job_exp or job_exp in cand_exp:
            pref_score += 10.0
        elif "fresher" in cand_exp and ("intern" in job_type or "entry" in job_exp):
            pref_score += 10.0

    pref_score = min(100.0, pref_score)

    raw_final = (skill_score * 0.55) + (semantic_score * 0.30) + (pref_score * 0.15)
    final_percentage = int(round(max(5.0, min(99.0, raw_final))))

    if final_percentage >= 85:
        match_level = "Exceptional Match"
        match_color = "emerald"
    elif final_percentage >= 70:
        match_level = "Strong Match"
        match_color = "blue"
    elif final_percentage >= 50:
        match_level = "Good Match"
        match_color = "amber"
    elif final_percentage >= 35:
        match_level = "Potential Match"
        match_color = "purple"
    else:
        match_level = "Low Match"
        match_color = "slate"

    if job_req_skills:
        reason = f"Matches {len(matched_req)} of {len(job_req_skills)} core required skills."
        if matched_req:
            reason += f" Strong alignment in: {', '.join(sorted(list(matched_req))[:3])}."
    else:
        reason = "Profile content closely matches the job description and scope."

    if missing_req:
        top_missing = sorted(list(missing_req))[:3]
        learning = f"Acquiring {', '.join(top_missing)} could elevate your match score to {min(98, final_percentage + 18)}%."
    else:
        learning = "You possess all key requirements for this position. Great candidate to apply immediately!"

    return {
        "match_percentage": final_percentage,
        "skill_score": round(skill_score, 1),
        "semantic_score": round(semantic_score, 1),
        "preference_score": round(pref_score, 1),
        "matched_skills": sorted(list(matched_req.union(matched_opt))),
        "missing_skills": sorted(list(missing_req)),
        "bonus_skills": sorted(list(matched_opt)),
        "match_level": match_level,
        "match_color": match_color,
        "recommendation_reason": reason,
        "learning_suggestion": learning,
    }


def rank_jobs_for_candidate(candidate, jobs, min_score=0, job_type_filter=None, query=None):
    ranked = []
    query_terms = [q.lower().strip() for q in (query or "").split() if q.strip()]

    for job in jobs:
        if job_type_filter and job_type_filter.lower() != "all":
            if job_type_filter.lower() not in str(job.get("job_type", "")).lower():
                continue

        if query_terms:
            searchable_text = f"{job.get('title', '')} {job.get('company', '')} {job.get('description', '')} {job.get('location', '')} {job.get('required_skills', '')}".lower()
            if not all(term in searchable_text for term in query_terms):
                continue

        match_info = compute_match_score(candidate, job)
        if match_info["match_percentage"] >= min_score:
            job_copy = dict(job)
            job_copy["match"] = match_info
            ranked.append(job_copy)

    ranked.sort(key=lambda x: (x["match"]["match_percentage"], x.get("id", 0)), reverse=True)
    return ranked


def rank_candidates_for_job(job, candidates):
    ranked = []
    for cand in candidates:
        match_info = compute_match_score(cand, job)
        cand_copy = dict(cand)
        cand_copy["match"] = match_info
        ranked.append(cand_copy)

    ranked.sort(key=lambda x: x["match"]["match_percentage"], reverse=True)
    return ranked
