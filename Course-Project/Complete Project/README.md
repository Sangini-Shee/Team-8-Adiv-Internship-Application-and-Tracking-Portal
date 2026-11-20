# Course Project – Internship Application and Tracking Portal

## Roles and permissions

### Student
- Four seeded student accounts for the project team.
- View profile, CGPA, backlogs, credits and skills.
- Browse internship offers and eligibility results.
- Submit applications.
- Track HOD and Internship Head decisions.
- Download generated or uploaded offer letters.
- Submit daily work, hours and learning updates after approval.
- View total, completed and remaining hours, marks and marksheet.
- Ask questions through one integrated assistant.

### Admin
- Publish additional internship offers with eligibility requirements and hour targets.
- View all student profiles and applications.
- Add student profiles.

### HOD
- Review student profiles and eligibility.
- Approve or reject applications.
- Monitor all student internship progress.
- Upload an externally issued offer letter or generate an institution-format draft.
- Ask questions through an internal assistant.

### Internship Head
- Review applications after HOD approval.
- Approve or reject applications.
- Monitor internship progress.
- Enter marks, grade and remarks.
- Upload marksheets / evaluation sheets.
- Upload offer letters or generate institution-format drafts.

## Approval flow
Student applies -> HOD review -> Internship Head review -> application approved ->
offer letter available -> student submits daily progress -> reviewers monitor progress.

## Offer letter
The portal can generate a PDF approval/offer letter with student and internship details,
terms, and typed signature blocks labelled HOD and Internship Head. The included terms
are clearly marked as draft examples. Replace them with the college's officially approved
internship rules before using the letter as an official institutional document.

## Frameworks
LangChain, LangGraph, MCP and Swarms are implemented in backend modules. The portal
shows students one assistant interface only. No source code, tool traces, prompts or
framework debugging details are displayed in the UI. LLM-backed LangChain/Swarms execution
requires a supported provider key; local fallback remains available.

## Demo accounts
| Role | Username | Password |
|---|---|---|
| Sangini Shee | sangini | student123 |
| Sindhu Kesiraju | sindhu | student123 |
| Chirag Hanamaratti | chirag | student123 |
| Kshitij Heblikar | kshitij | student123 |
| HOD | hod | hod123 |
| Internship Head | internshiphead | head123 |
| Admin | admin | admin123 |

All student records and sample internship offers are demo data. Change demo passwords
and replace draft terms before any real deployment.

## Run
Activate the repository `.venv`, open CMD inside this `Course-Project` folder, then:

```cmd
pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```cmd
python -m pytest -v
```
