
# ============================================================
# LAB 1 - AGENT VS CHATBOT
# Streamlit Internship Opportunity Planner
# File: streamlit_app.py
# ============================================================

import json
from datetime import datetime
from pathlib import Path

import streamlit as st

from app.agent import (
    clarify_request,
    create_plan,
    revise_plan,
    save_plan
)


# ------------------------------------------------------------
# PATHS AND CONFIGURATION
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
JSON_FILE = OUTPUT_DIR / "application_plans.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Internship Opportunity Planner",
    page_icon="🎓",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #4F46E5;
    }

    .subtitle {
        color: #777777;
        font-size: 1rem;
    }

    .stage {
        padding: 14px;
        border-radius: 10px;
        background-color: rgba(120, 120, 120, 0.08);
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

DEFAULTS = {
    "student_request": "",
    "clarification_questions": "",
    "clarification_answers": "",
    "plan": "",
    "revision_count": 0,
    "saved_message": ""
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ------------------------------------------------------------
# JSON STORAGE
# ------------------------------------------------------------

def save_plan_to_json(
    request: str,
    answers: str,
    plan: str
):
    """
    Stores the internship planning record in JSON format.
    """

    if JSON_FILE.exists():
        try:
            with open(
                JSON_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                records = json.load(file)

        except (json.JSONDecodeError, OSError):
            records = []

    else:
        records = []

    if not isinstance(records, list):
        records = []

    record = {
        "record_id": len(records) + 1,
        "created_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "student_request": request,
        "clarification_answers": answers,
        "application_plan": plan,
        "status": "Draft"
    }

    records.append(record)

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )


# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

st.markdown(
    '<div class="main-title">'
    'Internship Application & Tracking Portal'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Lab 1 | Agent vs Chatbot | Gemini-powered Coordinator'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:

    st.title("Coordinator")

    st.write(
        "Your AI assistant helps prepare and organize "
        "internship applications."
    )

    st.divider()

    st.subheader("Agent Workflow")

    stages = [
        "1. Clarification",
        "2. Plan Generation",
        "3. Plan Revision",
        "4. Save Application"
    ]

    for stage in stages:
        st.markdown(
            f'<div class="stage">{stage}</div>',
            unsafe_allow_html=True
        )

    st.divider()

    st.caption("Powered by Google Gemini API")


# ------------------------------------------------------------
# STAGE 1: CLARIFICATION
# ------------------------------------------------------------

st.header("1. Describe Your Internship Goal")

st.write(
    "Tell the Coordinator what kind of internship "
    "you are looking for."
)

student_request = st.text_area(
    "Your internship requirements",
    key="student_request",
    height=130,
    placeholder=(
        "Example: I am a final-year Computer Science "
        "student looking for an AI or Machine Learning "
        "internship. I know Python and have completed "
        "academic projects."
    )
)

if st.button(
    "Analyze Request",
    type="primary",
    use_container_width=True
):

    if not student_request.strip():

        st.warning("Please describe your internship goal.")

    else:

        try:
            with st.spinner(
                "Coordinator is analyzing your request..."
            ):

                questions = clarify_request(
                    student_request
                )

            st.session_state.clarification_questions = questions
            st.session_state.clarification_answers = ""
            st.session_state.plan = ""
            st.session_state.revision_count = 0
            st.session_state.saved_message = ""

            st.success(
                "Request analyzed. Please answer the "
                "clarification questions."
            )

        except Exception as error:

            st.error(f"Agent error: {error}")


# ------------------------------------------------------------
# DISPLAY CLARIFICATION QUESTIONS
# ------------------------------------------------------------

if st.session_state.clarification_questions:

    st.divider()

    st.header("2. Clarification Questions")

    st.markdown(
        st.session_state.clarification_questions
    )

    answers = st.text_area(
        "Your answers",
        key="clarification_answers",
        height=160,
        placeholder=(
            "Provide your answers to the questions above."
        )
    )

    if st.button(
        "Generate Internship Plan",
        type="primary",
        use_container_width=True
    ):

        if not answers.strip():

            st.warning(
                "Please provide your clarification answers."
            )

        else:

            try:
                with st.spinner(
                    "Coordinator is preparing your plan..."
                ):

                    generated_plan = create_plan(
                        st.session_state.student_request,
                        answers
                    )

                st.session_state.plan = generated_plan
                st.session_state.revision_count = 0
                st.session_state.saved_message = ""

                st.success(
                    "Internship application outline generated!"
                )

            except Exception as error:

                st.error(f"Planning error: {error}")


# ------------------------------------------------------------
# STAGE 3: PLAN REVISION
# ------------------------------------------------------------

if st.session_state.plan:

    st.divider()

    st.header("3. Internship Application Plan")

    st.info(
        "Review and edit this outline. You can also "
        "ask the Coordinator to revise it."
    )

    editor_key = (
        f"plan_editor_{st.session_state.revision_count}"
    )

    editable_plan = st.text_area(
        "Editable application outline",
        value=st.session_state.plan,
        key=editor_key,
        height=450
    )

    st.subheader("Request a Revision")

    feedback = st.text_area(
        "What would you like to change?",
        key="revision_feedback",
        height=100,
        placeholder=(
            "Example: Add a two-week preparation schedule "
            "and include interview preparation."
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Revise Plan",
            type="primary",
            use_container_width=True
        ):

            if not feedback.strip():

                st.warning(
                    "Please enter your revision instructions."
                )

            else:

                try:
                    with st.spinner(
                        "Coordinator is revising your plan..."
                    ):

                        revised_plan = revise_plan(
                            existing_plan=editable_plan,
                            feedback=feedback
                        )

                    st.session_state.plan = revised_plan
                    st.session_state.revision_count += 1
                    st.session_state.saved_message = ""

                    st.rerun()

                except Exception as error:

                    st.error(f"Revision error: {error}")

    with col2:

        if st.button(
            "Save Application Plan",
            use_container_width=True
        ):

            try:

                # Save editable Markdown document
                markdown_path = save_plan(editable_plan)

                # Save structured JSON record
                save_plan_to_json(
                    request=st.session_state.student_request,
                    answers=st.session_state.clarification_answers,
                    plan=editable_plan
                )

                st.session_state.saved_message = (
                    f"Application plan saved successfully. "
                    f"Markdown: {markdown_path}"
                )

                st.success(
                    "Application plan saved successfully!"
                )

                st.write(
                    "JSON record: outputs/application_plans.json"
                )

            except Exception as error:

                st.error(f"Save error: {error}")


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "Agentic AI | Team 8 | Division A | Lab 1"
)

st.caption(
    "Clarify → Plan → Revise → Save"
)
