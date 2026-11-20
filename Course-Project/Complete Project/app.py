from pathlib import Path
from datetime import date
import streamlit as st

from db import init_db, seed_data, get_conn, audit
from auth import verify_password
from agents import recommend, assess_eligibility
from workflow import submit_application, review_application
from assistant_service import answer_student_question
from offer_letter import generate_offer_letter, DEFAULT_TERMS, DRAFT_NOTICE

ROOT = Path(__file__).resolve().parent
UPLOAD_DIR = ROOT / "uploads"
OFFER_DIR = ROOT / "generated_offer_letters"
MARKS_DIR = ROOT / "marksheets"
for folder in (UPLOAD_DIR, OFFER_DIR, MARKS_DIR):
    folder.mkdir(exist_ok=True)

st.set_page_config(page_title="Internship Hub", page_icon="🎓", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
.stApp {background:#0b1524;color:#f4f8fc;font-family:'DM Sans',sans-serif;}
[data-testid="stHeader"] {background:rgba(11,21,36,.95);}
section[data-testid="stSidebar"] {background:#101f33;border-right:1px solid #29445c;}
section[data-testid="stSidebar"] * {color:#f2f7fb !important;}
h1,h2,h3,h4,p,label,span,div {color:inherit;}
h1,h2,h3 {font-family:'Manrope',sans-serif;color:#f7fbff;}
div[data-testid="stMetric"] {background:#152b40;border:1px solid #2b4b63;border-radius:15px;padding:14px;}
div[data-testid="stMetric"] label {color:#b7cad9 !important;}
div[data-testid="stMetricValue"] {color:#ffffff !important;}
div[data-testid="stVerticalBlockBorderWrapper"] {background:#12263a;border:1px solid #29465e;border-radius:16px;}
.stTextInput label,.stTextArea label,.stNumberInput label,.stSelectbox label,.stDateInput label,.stFileUploader label {color:#d9e8f2 !important;}
input,textarea,[data-baseweb="select"] > div {background:#172e44 !important;color:#ffffff !important;border-color:#3b5d76 !important;}
.stButton>button {background:#147d78;color:#fff;border:1px solid #299b91;border-radius:10px;font-weight:650;}
.stButton>button:hover {background:#19968e;color:white;border-color:#50c4b7;}
.stButton>button:disabled {background:#35495a;color:#a9b8c4;}
.stTabs [data-baseweb="tab"] {color:#c5d7e5;}
.stTabs [aria-selected="true"] {color:#6ce0ce !important;}
.portal-hero {background:linear-gradient(120deg,#102c43,#145b62);padding:25px 28px;border:1px solid #2b6a70;border-radius:19px;margin-bottom:18px;}
.portal-hero h1 {color:#fff;margin:0;}
.portal-hero p {color:#d5eeed;margin:7px 0 0;}
div[data-testid="stAlert"] p {color:inherit !important;}
small,.stCaption {color:#a9bfce !important;}
</style>
""", unsafe_allow_html=True)

init_db()
seed_data()

def rows(query, params=()):
    with get_conn() as c:
        return c.execute(query, params).fetchall()

def get_student(student_id):
    result = rows("SELECT * FROM students WHERE student_id=?", (student_id,))
    return dict(result[0]) if result else None

def get_application(application_id):
    result = rows("""
        SELECT a.*, s.full_name,s.department,s.cgpa,s.backlogs,s.credits,s.skills,
               i.title,i.company,i.department AS internship_department,i.description,
               i.required_skills,i.min_cgpa,i.max_backlogs,i.min_credits,i.duration,i.mode,i.total_hours
        FROM applications a
        JOIN students s ON s.student_id=a.student_id
        JOIN internships i ON i.id=a.internship_id
        WHERE a.id=?
    """, (application_id,))
    return dict(result[0]) if result else None

def login():
    left, center, right = st.columns([1, 1.2, 1])
    with center:
        st.markdown('<div class="portal-hero"><h1>Internship Hub</h1><p>Applications · Approvals · Progress · Outcomes</p></div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.subheader("Welcome back")
            with st.form("login"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Sign in", type="primary", use_container_width=True)
            if submit:
                found = rows("SELECT * FROM users WHERE username=?", (username.strip(),))
                if found and verify_password(password, found[0]["password_hash"]):
                    st.session_state.user = dict(found[0])
                    audit(username, "LOGIN", "Successful login")
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
            with st.expander("Demo accounts"):
                st.markdown("""
                **Students:** sangini / student123 · sindhu / student123 · chirag / student123 · kshitij / student123

                **HOD:** hod / hod123

                **Internship Head:** internshiphead / head123

                **Admin:** admin / admin123
                """)

def student_dashboard(user):
    student = get_student(user["student_id"])
    if not student:
        st.error("Student profile not found. Contact Admin.")
        return
    st.markdown(f'<div class="portal-hero"><h1>Welcome, {student["full_name"].split()[0]}</h1><p>Your internship journey in one place.</p></div>', unsafe_allow_html=True)
    st.subheader("My profile")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("CGPA",f"{student['cgpa']:.2f}/10")
    c2.metric("Backlogs",student["backlogs"])
    c3.metric("Credits",student["credits"])
    c4.metric("Student ID",student["student_id"])
    with st.container(border=True):
        a,b=st.columns([1,2])
        a.write("**Department**")
        a.write(student["department"])
        b.write("**Skills**")
        b.write(student["skills"])

    t1,t2,t3=st.tabs(["Explore internships","My internship & progress","Ask assistant"])
    with t1:
        st.subheader("Available internship offers")
        opportunities=[dict(x) for x in rows("SELECT * FROM internships WHERE active=1 ORDER BY id DESC")]
        for item in recommend(student, opportunities):
            with st.container(border=True):
                a,b=st.columns([4,1])
                with a:
                    st.markdown(f"### {item['title']}")
                    st.write(f"**{item['company']}** · {item['department']}")
                    st.write(item["description"])
                    st.caption(f"{item['duration']} · {item['mode']} · {item['total_hours']} hours")
                with b:
                    if item["eligible"]:
                        st.success("Eligible")
                    else:
                        st.error("Not eligible")
                    st.metric("Skill match",f"{item['skill_match']}%")
                with st.expander("Eligibility details"):
                    for label,passed in item["checks"].items():
                        st.write(("✓ " if passed else "✗ ")+label)
                    st.write("Matched skills:",", ".join(item["matched_skills"]) or "None")
                    st.write("Skills to develop:",", ".join(item["missing_skills"]) or "None")
                existing=rows("SELECT id,status FROM applications WHERE student_id=? AND internship_id=?",(student["student_id"],item["id"]))
                if existing:
                    st.info(f"Application already submitted · {existing[0]['status']}")
                elif item["eligible"]:
                    with st.form(f"apply_{item['id']}"):
                        note=st.text_area("Optional note for reviewers")
                        apply=st.form_submit_button("Apply")
                    if apply:
                        try:
                            submit_application(student["student_id"],item["id"],note)
                            st.success("Application submitted to HOD for review.")
                            st.rerun()
                        except Exception as exc:
                            st.error(str(exc))
                else:
                    st.button("Not eligible to apply",disabled=True,key=f"disabled_{item['id']}")
    with t2:
        st.subheader("My applications and internship progress")
        apps=rows("""
            SELECT a.*,i.title,i.company,i.total_hours FROM applications a
            JOIN internships i ON i.id=a.internship_id WHERE a.student_id=?
            ORDER BY a.created_at DESC
        """,(student["student_id"],))
        if not apps:
            st.info("Your submitted applications will appear here.")
        for app in apps:
            with st.container(border=True):
                st.markdown(f"### {app['title']} · {app['company']}")
                x,y,z=st.columns(3)
                x.metric("Application",app["status"])
                y.metric("HOD",app["hod_status"])
                z.metric("Internship Head",app["head_status"])
                letters=rows("SELECT * FROM offer_letters WHERE application_id=? ORDER BY uploaded_at DESC",(app["id"],))
                if letters:
                    st.markdown("**Your offer letters**")
                    for letter in letters:
                        path=Path(letter["file_path"])
                        if path.exists():
                            st.download_button(
                                f"Download {letter['filename']}",
                                data=path.read_bytes(),
                                file_name=letter["filename"],
                                mime="application/pdf",
                                key=f"download_{letter['id']}"
                            )
                if app["status"]=="Approved":
                    logs=rows("SELECT * FROM progress_logs WHERE application_id=? ORDER BY log_date DESC,id DESC",(app["id"],))
                    completed=sum(float(x["hours"]) for x in logs)
                    total=float(app["total_hours"] or 120)
                    p,q,r=st.columns(3)
                    p.metric("Total hours",f"{total:g}")
                    q.metric("Completed",f"{completed:g}")
                    r.metric("Remaining",f"{max(total-completed,0):g}")
                    st.progress(min(completed/total,1.0) if total else 0)
                    with st.form(f"daily_{app['id']}"):
                        d=st.date_input("Work date",date.today())
                        task=st.text_area("Work completed today")
                        hours=st.number_input("Hours worked",0.0,24.0,step=0.5)
                        learning=st.text_area("Learning / blockers")
                        save=st.form_submit_button("Submit daily update")
                    if save:
                        if not task.strip() or hours<=0:
                            st.error("Enter today's work and hours.")
                        elif completed+hours>total:
                            st.error("This update exceeds the internship's total required hours.")
                        else:
                            with get_conn() as c:
                                c.execute("INSERT INTO progress_logs(application_id,log_date,task_summary,hours,learning) VALUES(?,?,?,?,?)",
                                          (app["id"],str(d),task.strip(),hours,learning.strip()))
                            audit(student["student_id"],"PROGRESS_UPDATE",f"Application {app['id']} hours {hours}")
                            st.success("Progress updated.")
                            st.rerun()
                    if logs:
                        st.markdown("**Daily history**")
                        for log in logs:
                            with st.expander(f"{log['log_date']} · {log['hours']:g} hours"):
                                st.write(log["task_summary"])
                                if log["learning"]: st.caption(log["learning"])
                elif app["status"]=="Rejected":
                    st.error("Application rejected. Contact the reviewers for clarification.")
                else:
                    st.info("Daily progress opens after HOD and Internship Head approvals.")
                marks=rows("SELECT * FROM internship_marks WHERE application_id=?",(app["id"],))
                if marks:
                    st.markdown(f"**Internship assessment:** {marks[0]['marks']:g}/{marks[0]['max_marks']:g} · {marks[0]['grade']}")
                    if marks[0]["remarks"]: st.write(marks[0]["remarks"])
                    mpath=Path(marks[0]["marksheet_path"]) if marks[0]["marksheet_path"] else None
                    if mpath and mpath.exists():
                        st.download_button("Download marksheet",mpath.read_bytes(),file_name=mpath.name,key=f"student_marks_{app['id']}")
    with t3:
        st.subheader("Ask the Internship Hub assistant")
        st.caption("Ask about internships, eligibility, application decisions, offer letters or progress.")
        if "student_chat" not in st.session_state: st.session_state.student_chat=[]
        for msg in st.session_state.student_chat:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        prompt=st.chat_input("Ask a question...")
        if prompt:
            st.session_state.student_chat.append({"role":"user","content":prompt})
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Checking your portal information..."):
                    answer=answer_student_question(prompt,student["student_id"])
                st.markdown(answer)
            st.session_state.student_chat.append({"role":"assistant","content":answer})

def admin_dashboard(user):
    st.markdown('<div class="portal-hero"><h1>Admin workspace</h1><p>Manage students, internship offers and portal records.</p></div>',unsafe_allow_html=True)
    t1,t2,t3=st.tabs(["Publish internship","All student profiles","All applications"])
    with t1:
        with st.form("add_internship"):
            title=st.text_input("Internship title")
            company=st.text_input("Company / organization")
            department=st.text_input("Domain")
            description=st.text_area("Description")
            skills=st.text_input("Required skills (comma-separated)")
            a,b,c=st.columns(3)
            cgpa=a.number_input("Minimum CGPA",0.0,10.0,6.0,.1)
            backlog=b.number_input("Maximum backlogs",0,20,0)
            credits=c.number_input("Minimum credits",0,300,120)
            d,e=st.columns(2)
            duration=d.text_input("Duration","3 months")
            total_hours=e.number_input("Total internship hours",1,2000,120)
            mode=st.selectbox("Mode",["On-site","Hybrid","Remote"])
            publish=st.form_submit_button("Publish internship offer")
        if publish:
            if not title.strip() or not company.strip(): st.error("Title and company are required.")
            else:
                with get_conn() as c:
                    c.execute("""INSERT INTO internships(title,company,department,description,required_skills,min_cgpa,max_backlogs,min_credits,duration,mode,total_hours)
                                  VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                               (title,company,department,description,skills,cgpa,backlog,credits,duration,mode,total_hours))
                audit(user["username"],"INTERNSHIP_CREATED",title)
                st.success("Internship offer published.")
                st.rerun()
    with t2:
        students=rows("SELECT * FROM students ORDER BY full_name")
        st.dataframe([dict(x) for x in students],use_container_width=True)
        st.subheader("Add student profile")
        with st.form("add_student"):
            sid=st.text_input("Student ID")
            name=st.text_input("Full name")
            dept=st.text_input("Department","CS-AI")
            cg=st.number_input("CGPA",0.0,10.0,7.0,.1)
            backs=st.number_input("Backlogs",0,20,0)
            cred=st.number_input("Credits completed",0,300,120)
            sk=st.text_input("Skills, comma-separated")
            add=st.form_submit_button("Add student")
        if add:
            if not sid.strip() or not name.strip(): st.error("Student ID and name are required.")
            else:
                with get_conn() as c:
                    c.execute("INSERT INTO students(student_id,full_name,department,cgpa,backlogs,credits,skills) VALUES(?,?,?,?,?,?,?)",
                              (sid.strip(),name.strip(),dept,cg,backs,cred,sk))
                audit(user["username"],"STUDENT_CREATED",sid)
                st.success("Student profile added. Create a student login through account administration before login.")
                st.rerun()
    with t3:
        all_apps=rows("""SELECT a.id,s.full_name,s.student_id,i.title,i.company,a.status,a.hod_status,a.head_status
                         FROM applications a JOIN students s ON s.student_id=a.student_id
                         JOIN internships i ON i.id=a.internship_id ORDER BY a.created_at DESC""")
        st.dataframe([dict(x) for x in all_apps],use_container_width=True)

def offer_letter_tools(app, user):
    st.markdown("**Offer letter management**")
    st.caption("HOD or Internship Head can upload an externally issued PDF or generate the portal's approval letter.")
    existing=rows("SELECT * FROM offer_letters WHERE application_id=? ORDER BY uploaded_at DESC",(app["id"],))
    if existing:
        for letter in existing:
            p=Path(letter["file_path"])
            if p.exists():
                st.download_button(f"Download stored letter: {letter['filename']}",p.read_bytes(),file_name=letter["filename"],mime="application/pdf",key=f"review_dl_{letter['id']}")
    up=st.file_uploader("Upload signed / organization-issued offer letter (PDF)",type=["pdf"],key=f"offer_upload_{app['id']}")
    if up and st.button("Save uploaded offer letter",key=f"save_uploaded_{app['id']}"):
        fname=f"application_{app['id']}_{Path(up.name).name}"
        target=UPLOAD_DIR/fname
        target.write_bytes(up.getbuffer())
        with get_conn() as c:
            c.execute("INSERT INTO offer_letters(application_id,filename,file_path,uploaded_by,letter_type) VALUES(?,?,?,?,?)",
                      (app["id"],up.name,str(target),user["username"],"Uploaded"))
        audit(user["username"],"OFFER_LETTER_UPLOADED",f"Application {app['id']}")
        st.success("Offer letter uploaded and made available to the student.")
        st.rerun()

    st.markdown("**Generate institution-format approval letter**")
    st.warning(DRAFT_NOTICE)
    with st.expander("Preview draft terms and conditions"):
        for i,term in enumerate(DEFAULT_TERMS,1): st.write(f"{i}. {term}")
    if st.button("Generate PDF offer / approval letter",key=f"generate_letter_{app['id']}"):
        student={"full_name":app["full_name"],"student_id":app["student_id"],"department":app["department"]}
        internship={"title":app["title"],"company":app["company"],"department":app["internship_department"],
                    "duration":app["duration"],"mode":app["mode"],"total_hours":app["total_hours"]}
        target=OFFER_DIR/f"Internship_Approval_{app['student_id']}_{app['id']}.pdf"
        generate_offer_letter(target,student,internship,app["id"])
        with get_conn() as c:
            c.execute("INSERT INTO offer_letters(application_id,filename,file_path,uploaded_by,letter_type) VALUES(?,?,?,?,?)",
                      (app["id"],target.name,str(target),user["username"],"Generated draft"))
        audit(user["username"],"OFFER_LETTER_GENERATED",f"Application {app['id']}")
        st.success("PDF generated and attached to the student's portal.")
        st.rerun()

def reviewer_dashboard(user):
    role=user["role"]
    st.markdown(f'<div class="portal-hero"><h1>{role} workspace</h1><p>Application review, student monitoring and internship records.</p></div>',unsafe_allow_html=True)
    pending_filter="a.hod_status='Pending'" if role=="HOD" else "a.hod_status='Approved' AND a.head_status='Pending'"
    apps=rows(f"""SELECT a.id AS application_id,a.*,s.full_name,s.department,s.cgpa,s.backlogs,s.credits,s.skills,
                         i.title,i.company,i.required_skills,i.min_cgpa,i.max_backlogs,i.min_credits,i.duration,i.mode,i.total_hours,
                         i.department AS internship_department
                  FROM applications a JOIN students s ON s.student_id=a.student_id
                  JOIN internships i ON i.id=a.internship_id WHERE {pending_filter} ORDER BY a.created_at""")
    st.subheader("Applications awaiting your decision")
    if not apps: st.info("No applications are waiting for your review.")
    for raw in apps:
        app=dict(raw)
        eligibility=assess_eligibility({"cgpa":app["cgpa"],"backlogs":app["backlogs"],"credits":app["credits"],"skills":app["skills"]},
                                       {"min_cgpa":app["min_cgpa"],"max_backlogs":app["max_backlogs"],"min_credits":app["min_credits"],"required_skills":app["required_skills"]})
        with st.container(border=True):
            st.markdown(f"### Application #{app['application_id']} · {app['title']}")
            st.write(f"**Student:** {app['full_name']} ({app['student_id']}) · **Company:** {app['company']}")
            a,b,c=st.columns(3)
            a.metric("CGPA",app["cgpa"])
            b.metric("Backlogs",app["backlogs"])
            c.metric("Credits",app["credits"])
            st.write("**Skills:**",app["skills"])
            st.write("**Required skills:**",app["required_skills"])
            for label,passed in eligibility["checks"].items():
                st.write(("✅ " if passed else "❌ ")+label)
            st.write(f"Skill match: {eligibility['skill_match']}%")
            col1,col2=st.columns(2)
            if col1.button("Approve",key=f"approve_{role}_{app['application_id']}",type="primary"):
                try:
                    review_application(app["application_id"],role,"Approved",user["username"])
                    st.success("Approval recorded.")
                    st.rerun()
                except Exception as exc: st.error(str(exc))
            if col2.button("Reject",key=f"reject_{role}_{app['application_id']}"):
                try:
                    review_application(app["application_id"],role,"Rejected",user["username"])
                    st.warning("Application rejected.")
                    st.rerun()
                except Exception as exc: st.error(str(exc))

    st.divider()
    st.subheader("Student internship monitoring")
    monitored=rows("""SELECT a.id AS application_id,a.status,a.hod_status,a.head_status,
                             s.full_name,s.student_id,s.department,s.cgpa,s.backlogs,s.credits,s.skills,
                             i.title,i.company,i.total_hours,i.min_cgpa,i.max_backlogs,i.min_credits,i.required_skills
                      FROM applications a JOIN students s ON s.student_id=a.student_id
                      JOIN internships i ON i.id=a.internship_id
                      ORDER BY s.full_name""")
    if not monitored: st.info("Student application progress will appear here.")
    for raw in monitored:
        app=dict(raw)
        with st.expander(f"{app['full_name']} · {app['title']} · {app['status']}"):
            st.write(f"Student ID: {app['student_id']} · {app['department']} · CGPA {app['cgpa']}")
            st.write(f"HOD: {app['hod_status']} · Internship Head: {app['head_status']}")
            logs=rows("SELECT * FROM progress_logs WHERE application_id=? ORDER BY log_date DESC",(app["application_id"],))
            done=sum(float(x["hours"]) for x in logs)
            total=float(app["total_hours"] or 120)
            x,y,z=st.columns(3)
            x.metric("Total hours",f"{total:g}")
            y.metric("Completed",f"{done:g}")
            z.metric("Remaining",f"{max(total-done,0):g}")
            st.progress(min(done/total,1) if total else 0)
            for log in logs:
                st.markdown(f"**{log['log_date']} · {log['hours']:g} hours**")
                st.write(log["task_summary"])
                if log["learning"]: st.caption(log["learning"])
            if app["status"]=="Approved":
                full_app=get_application(app["application_id"])
                offer_letter_tools(full_app,user)
            if role=="Internship Head":
                st.markdown("**Internship marks / assessment**")
                current=rows("SELECT * FROM internship_marks WHERE application_id=?",(app["application_id"],))
                with st.form(f"marks_{app['application_id']}"):
                    marks=st.number_input("Marks obtained",0.0,1000.0,float(current[0]["marks"]) if current else 0.0,.5)
                    max_marks=st.number_input("Maximum marks",1.0,1000.0,float(current[0]["max_marks"]) if current else 100.0,.5)
                    grade=st.text_input("Grade",current[0]["grade"] if current else "")
                    remarks=st.text_area("Assessment remarks",current[0]["remarks"] if current else "")
                    save_marks=st.form_submit_button("Save marks")
                marks_file=st.file_uploader("Upload marksheet / evaluation sheet",type=["pdf","csv","xlsx"],key=f"marks_file_{app['application_id']}")
                if save_marks:
                    if marks>max_marks: st.error("Marks cannot exceed maximum marks.")
                    else:
                        old_path=current[0]["marksheet_path"] if current else ""
                        with get_conn() as c:
                            c.execute("""INSERT INTO internship_marks(application_id,marks,max_marks,grade,remarks,marksheet_path,updated_by)
                                         VALUES(?,?,?,?,?,?,?)
                                         ON CONFLICT(application_id) DO UPDATE SET
                                         marks=excluded.marks,max_marks=excluded.max_marks,grade=excluded.grade,
                                         remarks=excluded.remarks,updated_by=excluded.updated_by,updated_at=CURRENT_TIMESTAMP""",
                                      (app["application_id"],marks,max_marks,grade,remarks,old_path,user["username"]))
                        audit(user["username"],"INTERNSHIP_MARKS_UPDATED",f"Application {app['application_id']}: {marks}/{max_marks}")
                        st.success("Marks saved.")
                        st.rerun()
                if marks_file and st.button("Upload marksheet",key=f"upload_marks_{app['application_id']}"):
                    target=MARKS_DIR/f"marks_{app['student_id']}_{app['application_id']}_{Path(marks_file.name).name}"
                    target.write_bytes(marks_file.getbuffer())
                    with get_conn() as c:
                        existing=c.execute("SELECT * FROM internship_marks WHERE application_id=?",(app["application_id"],)).fetchone()
                        if existing:
                            c.execute("UPDATE internship_marks SET marksheet_path=?,updated_by=?,updated_at=CURRENT_TIMESTAMP WHERE application_id=?",
                                      (str(target),user["username"],app["application_id"]))
                        else:
                            c.execute("INSERT INTO internship_marks(application_id,marks,max_marks,marksheet_path,updated_by) VALUES(?,?,?,?,?)",
                                      (app["application_id"],0,100,str(target),user["username"]))
                    audit(user["username"],"MARKSHEET_UPLOADED",f"Application {app['application_id']}")
                    st.success("Marksheet uploaded.")
                    st.rerun()

    if role=="HOD":
        st.divider()
        st.subheader("HOD assistant")
        st.caption("Ask about pending applications, eligibility and internship progress.")
        if "review_chat" not in st.session_state: st.session_state.review_chat=[]
        for msg in st.session_state.review_chat:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        prompt=st.chat_input("Ask the HOD assistant...")
        if prompt:
            st.session_state.review_chat.append({"role":"user","content":prompt})
            with st.chat_message("assistant"):
                # Internal assistant entry point; no framework/debug details exposed.
                answer=answer_student_question(prompt,"STU001")
                st.markdown(answer)
            st.session_state.review_chat.append({"role":"assistant","content":answer})

def main():
    if "user" not in st.session_state:
        login()
        return
    user=st.session_state.user
    with st.sidebar:
        st.markdown("## INTERNSHIP HUB")
        st.caption("APPLICATION & TRACKING")
        st.write(f"**{user['full_name']}**")
        st.caption(user["role"])
        st.divider()
        if st.button("Log out",use_container_width=True):
            audit(user["username"],"LOGOUT","Logged out")
            for key in ("user","student_chat","review_chat"): st.session_state.pop(key,None)
            st.rerun()
    if user["role"]=="Student":
        student_dashboard(user)
    elif user["role"] in ("HOD","Internship Head"):
        reviewer_dashboard(user)
    elif user["role"]=="Admin":
        admin_dashboard(user)
    else:
        st.error("Unknown role.")

if __name__=="__main__":
    main()
