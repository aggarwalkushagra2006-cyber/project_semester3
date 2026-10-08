"""
Job & Internship Portal with Recommendation Engine
Built with Python Flask, SQLite, and Hybrid TF-IDF / Skill Vector Matching.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
import database as db
import recommendation as reco

app = Flask(__name__)
app.secret_key = "job_portal_secret_key_antigravity_2026"

with app.app_context():
    db.init_db()
    db.seed_sample_data(force=False)


@app.context_processor
def inject_global_data():
    all_candidates = db.get_candidates()
    current_user_id = session.get("user_id", 1)
    current_user = db.get_candidate(current_user_id)
    if not current_user and all_candidates:
        current_user = all_candidates[0]
        session["user_id"] = current_user["id"]

    saved_job_ids = db.get_saved_job_ids(current_user["id"]) if current_user else set()
    user_role = session.get("role", "candidate")

    return {
        "current_user": current_user,
        "all_candidates": all_candidates,
        "saved_job_ids": saved_job_ids,
        "user_role": user_role
    }


@app.route("/")
def index():
    current_user_id = session.get("user_id", 1)
    current_user = db.get_candidate(current_user_id)
    all_jobs = db.get_all_jobs()

    search_query = request.args.get("q", "").strip()
    job_type = request.args.get("type", "All")
    min_match = int(request.args.get("min_match", 0))
    category = request.args.get("category", "All")
    remote_only = request.args.get("remote", "0") == "1"

    filtered_jobs = all_jobs
    if category != "All":
        filtered_jobs = [j for j in filtered_jobs if j["category"].lower() == category.lower()]
    if remote_only:
        filtered_jobs = [j for j in filtered_jobs if j["is_remote"] == 1]

    ranked_jobs = reco.rank_jobs_for_candidate(
        candidate=current_user,
        jobs=filtered_jobs,
        min_score=min_match,
        job_type_filter=job_type,
        query=search_query
    )

    top_picks = [j for j in ranked_jobs if j["match"]["match_percentage"] >= 70][:3]
    categories = sorted(list(set(j["category"] for j in all_jobs)))

    return render_template(
        "index.html",
        jobs=ranked_jobs,
        top_picks=top_picks,
        total_jobs=len(all_jobs),
        filtered_count=len(ranked_jobs),
        categories=categories,
        selected_category=category,
        selected_type=job_type,
        search_query=search_query,
        min_match=min_match,
        remote_only=remote_only
    )


@app.route("/job/<int:job_id>")
def job_detail(job_id):
    job = db.get_job(job_id)
    if not job:
        flash("Job not found", "error")
        return redirect(url_for("index"))

    current_user_id = session.get("user_id", 1)
    current_user = db.get_candidate(current_user_id)
    match_analysis = reco.compute_match_score(current_user, job)

    applications = db.get_candidate_applications(current_user_id)
    applied_app = next((a for a in applications if a["job_id"] == job_id), None)

    all_jobs = [j for j in db.get_all_jobs() if j["id"] != job_id]
    similar_jobs = reco.rank_jobs_for_candidate(current_user, all_jobs)[:3]

    return render_template(
        "job_detail.html",
        job=job,
        match=match_analysis,
        applied_app=applied_app,
        similar_jobs=similar_jobs
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    current_user_id = session.get("user_id", 1)
    
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "title": request.form.get("title"),
            "headline": request.form.get("headline"),
            "bio": request.form.get("bio"),
            "skills": request.form.get("skills"),
            "experience_level": request.form.get("experience_level"),
            "education": request.form.get("education"),
            "preferred_type": request.form.get("preferred_type"),
            "resume_text": request.form.get("resume_text")
        }
        db.update_candidate(current_user_id, data)
        flash("Profile updated successfully! Recommendation scores have been refreshed.", "success")
        return redirect(url_for("profile"))

    current_user = db.get_candidate(current_user_id)
    skills_list = [s.strip() for s in current_user.get("skills", "").split(",") if s.strip()]
    return render_template("profile.html", candidate=current_user, skills_list=skills_list)


@app.route("/applications")
def applications():
    current_user_id = session.get("user_id", 1)
    apps = db.get_candidate_applications(current_user_id)
    return render_template("applications.html", applications=apps)


@app.route("/recruiter")
def recruiter():
    jobs = db.get_all_jobs()
    selected_job_id = request.args.get("job_id", type=int)

    if not selected_job_id and jobs:
        selected_job_id = jobs[0]["id"]

    selected_job = db.get_job(selected_job_id) if selected_job_id else None
    job_applications = db.get_job_applications(selected_job_id) if selected_job_id else []

    all_candidates = db.get_candidates()
    ranked_talent = reco.rank_candidates_for_job(selected_job, all_candidates) if selected_job else []

    return render_template(
        "recruiter.html",
        jobs=jobs,
        selected_job=selected_job,
        applications=job_applications,
        ranked_talent=ranked_talent
    )


@app.route("/api/apply/<int:job_id>", methods=["POST"])
def apply(job_id):
    current_user_id = session.get("user_id", 1)
    current_user = db.get_candidate(current_user_id)
    job = db.get_job(job_id)

    if not job:
        return jsonify({"success": False, "message": "Job not found"}), 404

    cover_letter = request.form.get("cover_letter", "")
    match_analysis = reco.compute_match_score(current_user, job)
    score = match_analysis["match_percentage"]

    success, message = db.apply_to_job(job_id, current_user_id, cover_letter, score)
    return jsonify({"success": success, "message": message, "match_score": score})


@app.route("/api/save/<int:job_id>", methods=["POST"])
def save_job(job_id):
    current_user_id = session.get("user_id", 1)
    is_saved = db.toggle_saved_job(current_user_id, job_id)
    return jsonify({"saved": is_saved, "job_id": job_id})


@app.route("/api/extract-skills", methods=["POST"])
def extract_skills():
    text = request.json.get("text", "")
    skills = reco.extract_skills_from_text(text)
    return jsonify({"skills": skills, "count": len(skills)})


@app.route("/api/jobs/create", methods=["POST"])
def create_job_api():
    data = {
        "title": request.form.get("title"),
        "company": request.form.get("company"),
        "location": request.form.get("location"),
        "is_remote": request.form.get("is_remote") == "1",
        "job_type": request.form.get("job_type"),
        "category": request.form.get("category"),
        "experience_level": request.form.get("experience_level"),
        "stipend_or_salary": request.form.get("stipend_or_salary"),
        "required_skills": request.form.get("required_skills"),
        "optional_skills": request.form.get("optional_skills", ""),
        "description": request.form.get("description"),
        "responsibilities": request.form.get("responsibilities", ""),
        "requirements": request.form.get("requirements", ""),
        "perks": request.form.get("perks", ""),
        "deadline": request.form.get("deadline", "Open Until Filled")
    }
    new_id = db.create_job(data)
    flash("New job/internship listing successfully posted!", "success")
    return redirect(url_for("recruiter", job_id=new_id))


@app.route("/api/applications/<int:app_id>/status", methods=["POST"])
def update_status(app_id):
    status = request.form.get("status")
    db.update_application_status(app_id, status)
    flash(f"Application status updated to '{status}'", "info")
    return redirect(request.referrer or url_for("recruiter"))


@app.route("/switch-user/<int:user_id>")
def switch_user(user_id):
    cand = db.get_candidate(user_id)
    if cand:
        session["user_id"] = user_id
        flash(f"Switched profile to {cand['name']} ({cand['title']})", "info")
    return redirect(request.referrer or url_for("index"))


@app.route("/reset-demo")
def reset_demo():
    db.seed_sample_data(force=True)
    flash("Database reset with fresh sample candidates, jobs, and applications.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 Job & Internship Portal with Recommendation Engine")
    print("🌐 Running locally on: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5000)
