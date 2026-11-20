"""Single student-facing assistant; all framework orchestration is internal."""
def _local_answer(question, student_id):
    from db import get_conn
    from agents import recommend

    with get_conn() as conn:
        student_row = conn.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
        internships = conn.execute("SELECT * FROM internships WHERE active=1").fetchall()
        apps = conn.execute(
            """SELECT a.status, a.hod_status, a.head_status, i.title
               FROM applications a JOIN internships i ON i.id=a.internship_id
               WHERE a.student_id=? ORDER BY a.created_at DESC""", (student_id,)
        ).fetchall()

    if not student_row:
        return "I could not find your student profile. Please contact the administrator."
    student = dict(student_row)
    q = question.lower()
    if any(w in q for w in ("eligible", "eligibility", "qualify", "internship", "internships", "recommend", "apply")):
        recs = recommend(student, [dict(x) for x in internships])
        eligible = [x for x in recs if x["eligible"]]
        if not eligible:
            return "No current opportunity meets all listed academic criteria. Review each opportunity's CGPA, backlog and credit requirements."
        return "Opportunities matching your current eligibility:\\n" + "\\n".join(
            f"• {x['title']} at {x['company']} — {x['skill_match']}% skill match; "
            f"matched: {', '.join(x['matched_skills']) or 'None'}; "
            f"to develop: {', '.join(x['missing_skills']) or 'None'}."
            for x in eligible
        )
    if any(w in q for w in ("profile", "cgpa", "skills", "backlog", "credit")):
        return (f"Your profile: CGPA {student['cgpa']}, backlogs {student['backlogs']}, "
                f"credits {student['credits']}, skills: {student['skills']}.")
    if any(w in q for w in ("approval", "hod", "coordinator", "status", "application")):
        if not apps:
            return "You have not submitted an application yet. Explore internships and apply when eligible."
        return "\\n".join(
            f"• {a['title']}: {a['status']} (HOD: {a['hod_status']}; Internship Head: {a['head_status']})"
            for a in apps
        )
    return ("I can help with your profile, internship opportunities, eligibility, "
            "application approvals and progress tracking. What would you like to know?")

def answer_student_question(question, student_id):
    """Return a user-facing answer; never expose stack traces or framework internals."""
    try:
        from integrations.langgraph_orchestrator import run_portal_assistant
        result = run_portal_assistant(question, student_id)
        answer = result.get("answer")
        if answer:
            return answer
    except Exception:
        # Keep the portal usable if an external provider or MCP service is unavailable.
        pass
    try:
        return _local_answer(question, student_id)
    except Exception:
        return ("I couldn't retrieve that information right now. "
                "Please check your profile and application pages, then try again.")


def answer_staff_question(question, role):
    """Internal staff assistant for HOD / Internship Head dashboard questions."""
    from db import get_conn
    q = question.lower()
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) n FROM applications").fetchone()["n"]
        pending_hod = conn.execute("SELECT COUNT(*) n FROM applications WHERE hod_status='Pending'").fetchone()["n"]
        pending_head = conn.execute("SELECT COUNT(*) n FROM applications WHERE hod_status='Approved' AND head_status='Pending'").fetchone()["n"]
        approved = conn.execute("SELECT COUNT(*) n FROM applications WHERE status='Approved'").fetchone()["n"]
        progress = conn.execute("""
            SELECT s.full_name, i.title, i.total_hours, COALESCE(SUM(p.hours),0) completed
            FROM applications a JOIN students s ON s.student_id=a.student_id
            JOIN internships i ON i.id=a.internship_id
            LEFT JOIN progress_logs p ON p.application_id=a.id
            WHERE a.status='Approved'
            GROUP BY a.id ORDER BY s.full_name
        """).fetchall()
        student_count = conn.execute("SELECT COUNT(*) n FROM students").fetchone()["n"]
    if any(w in q for w in ("pending", "awaiting", "review", "approval")):
        return (f"Portal review summary: {total} applications submitted; "
                f"{pending_hod} awaiting HOD review; {pending_head} awaiting Internship Head review; "
                f"{approved} fully approved.")
    if any(w in q for w in ("progress", "hours", "monitor", "completed")):
        if not progress:
            return "There are no fully approved internships with progress tracking yet."
        return "Approved internship progress:\\n" + "\\n".join(
            f"• {r['full_name']} — {r['title']}: {float(r['completed']):g}/{float(r['total_hours'] or 0):g} hours."
            for r in progress
        )
    if any(w in q for w in ("student", "profile", "how many")):
        return f"There are {student_count} student profiles and {total} submitted applications in the portal."
    return ("I can summarize pending approvals, student application counts and approved internship progress. "
            "Ask about pending reviews, student profiles or progress hours.")
