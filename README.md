
# Team 8 – Internship Application and Tracking Portal

## Project Overview

The Internship Application and Tracking Portal is an AI-powered platform designed to simplify and streamline the internship application and approval process for students and college administrators.

The system helps students discover internship opportunities, check eligibility based on academic performance and skills, submit applications, and track internship progress.

It also supports administrative workflows involving HODs and Internship Coordinators, including application review, approval, and offer-letter management.

The project incorporates Agentic AI concepts, including LangChain, LangGraph, Swarms, and Model Context Protocol (MCP), to support intelligent workflows and automated assistance.

## Team Details

| Field | Details |
|---|---|
| Team | Team 8 |
| Division | A |
| Project | Internship Application and Tracking Portal |

### Team Members

| Sl. No. | Name | USN |
|---|---|---|
| 1 | Sangini Shee | To be added |
| 2 | K Sindhu | To be added |
| 3 | Chirag Hanamaratti | To be added |
| 4 | Kshitij Heblikar | To be added |

## Repository Structure

```text
Team-8-Adiv-Internship-Application-and-Tracking-Portal/
│
├── Course-Project/
│   ├── Labs/
│   │   ├── Lab-01-Agent-vs-Chatbot/
│   │   ├── Lab-02-Tool-Using-Agent/
│   │   ├── Lab-03/
│   │   ├── Lab-04/
│   │   ├── Lab-05/
│   │   ├── Lab-06/
│   │   ├── Lab-07/
│   │   ├── Lab-08/
│   │   ├── Lab-09/
│   │   ├── Lab-10/
│   │   ├── Lab-11/
│   │   ├── Lab-12/
│   │   ├── Lab-13/
│   │   └── Lab-14/
│   │
│   ├── Architecture/
│   ├── Problem-Statement/
│   ├── report/
│   └── Screenshots/
│
├── .gitignore
└── README.md
```

## Course Labs – 14 Experiments

The repository contains the practical implementations completed as part of the Agentic AI course.

| Lab | Topic | Status |
|---|---|---|
| Lab 1 | Agent vs Chatbot | Completed |
| Lab 2 | Tool-Using Agent | Completed |
| Lab 3 | To be documented | Pending verification |
| Lab 4 | To be documented | Pending verification |
| Lab 5 | To be documented | Pending verification |
| Lab 6 | To be documented | Pending verification |
| Lab 7 | To be documented | Pending verification |
| Lab 8 | To be documented | Pending verification |
| Lab 9 | To be documented | Pending verification |
| Lab 10 | To be documented | Pending verification |
| Lab 11 | To be documented | Pending verification |
| Lab 12 | To be documented | Pending verification |
| Lab 13 | To be documented | Pending verification |
| Lab 14 | To be documented | Pending verification |

## Course Project

### Internship Application and Tracking Portal

**Problem Statement**

To build an AI-powered Internship Application and Tracking Portal that streamlines internship discovery, eligibility assessment, application approval, and internship progress monitoring through intelligent agents and automated workflows.

### Key Objectives

- Provide role-based access for Students, Admin, HOD, and Internship Coordinators.
- Recommend internship opportunities based on students' academic profiles and skills.
- Evaluate eligibility using CGPA, backlogs, academic credits, and required skills.
- Implement an approval workflow involving the HOD and Internship Head.
- Enable administrators to upload and manage internship offer letters.
- Allow students to update their internship progress regularly.
- Provide centralized internship application and status tracking.

### Proposed Technologies

- Python
- LangChain
- LangGraph
- Swarms
- Model Context Protocol (MCP)
- Streamlit
- SQLite
- Large Language Models

### Main Modules

1. User Authentication and Role Management
2. Student Profile Management
3. Internship Opportunity Management
4. AI-Based Internship Recommendations
5. Eligibility Assessment
6. Internship Application Management
7. HOD Approval Workflow
8. Internship Head Approval Workflow
9. Offer Letter Management
10. Internship Progress Tracking
11. AI Agent Orchestration
12. Notification and Status Management
13. Administrative Dashboard
14. Reporting and Monitoring

## Implemented Lab Highlights

### Lab 1 – Agent vs Chatbot

Implemented an AI agent demonstrating the Clarify, Plan, and Revise workflow using the Gemini API. Includes a Streamlit interface and automated tests.

### Lab 2 – Tool-Using Agent

Implemented a Gemini-powered tool-using agent with three Python tools:

- `read_student_profile`
- `read_opportunity`
- `check_eligibility`

Includes structured JSON data, Pydantic validation, CLI execution, Streamlit interface, local fallback execution, and automated tests.

Latest recorded test result: 12 tests passed.

## How to Run

Navigate to the required lab directory and follow its README instructions.

For example, Lab 2:

```bash
cd Course-Project/Labs/Lab-02-Tool-Using-Agent
pip install -r requirements.txt
streamlit run streamlit_app.py
```

For automated tests:

```bash
python -m pytest tests -v
```

Configure required API credentials in the root `.env` file. Never upload API keys or other secrets to GitHub.

## Important Note

Student profiles, academic details, internship opportunities, and eligibility records currently used in the Lab 2 demonstration are synthetic data. They are not official institutional records or approved internship opportunities.

## Repository

GitHub: https://github.com/Sangini-Shee/Team-8-Adiv-Internship-Application-and-Tracking-Portal

---

**Team 8 | Division A**
