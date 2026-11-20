from db import get_conn, audit

def submit_application(student_id, internship_id, note=""):
    with get_conn() as c:
        c.execute(
            "INSERT INTO applications(student_id,internship_id,student_note) VALUES(?,?,?)",
            (student_id, internship_id, note)
        )
    audit(student_id, "APPLICATION_SUBMITTED", f"Internship ID {internship_id}")

def review_application(application_id, reviewer_role, decision, actor):
    if reviewer_role not in ("HOD", "Internship Head"):
        raise ValueError("Invalid reviewer role")
    if decision not in ("Approved", "Rejected"):
        raise ValueError("Decision must be Approved or Rejected")
    with get_conn() as c:
        app = c.execute("SELECT * FROM applications WHERE id=?", (application_id,)).fetchone()
        if not app:
            raise ValueError("Application not found")
        if reviewer_role == "HOD":
            if app["hod_status"] != "Pending":
                raise ValueError("HOD has already reviewed this application.")
            column = "hod_status"
        else:
            if app["hod_status"] != "Approved":
                raise ValueError("Internship Head review is available only after HOD approval.")
            if app["head_status"] != "Pending":
                raise ValueError("Internship Head has already reviewed this application.")
            column = "head_status"

        c.execute(f"UPDATE applications SET {column}=? WHERE id=?", (decision, application_id))
        updated = c.execute("SELECT * FROM applications WHERE id=?", (application_id,)).fetchone()
        if "Rejected" in (updated["hod_status"], updated["head_status"]):
            status = "Rejected"
        elif updated["hod_status"] == "Approved" and updated["head_status"] == "Approved":
            status = "Approved"
        elif updated["hod_status"] == "Approved":
            status = "Awaiting Internship Head Approval"
        else:
            status = "Awaiting HOD Approval"
        c.execute("UPDATE applications SET status=? WHERE id=?", (status, application_id))
    audit(actor, f"{reviewer_role.upper()}_{decision.upper()}", f"Application ID {application_id}")
    return status
