
import streamlit as st

from app.skill_registry import list_skills
from app.skills import (
    opportunity_discovery,
    eligibility_verification,
    application_preparation
)

from app.schemas import (
    OpportunityDiscoveryInput,
    EligibilityVerificationInput,
    ApplicationPreparationInput
)


st.set_page_config(
    page_title="Internship Skill Center",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Internship Skill Center")
st.write(
    "Reusable AI skills for internship discovery, "
    "eligibility verification and application preparation."
)

skills = list_skills()

# Sidebar
with st.sidebar:
    st.header("Available Skills")

    selected_skill = st.radio(
        "Choose a skill",
        options=list(skills.keys()),
        format_func=lambda key: skills[key]["name"]
    )

    st.divider()
    st.caption("Lab 3 – Skill Creation")
    st.caption("All records are synthetic demonstration data.")


# Main content
skill_info = skills[selected_skill]

st.subheader(skill_info["name"])
st.write(skill_info["description"])
st.caption(f"Category: {skill_info['category']}")

st.divider()

student_id = st.text_input(
    "Student ID",
    value="STU001"
)

if selected_skill == "opportunity_discovery":

    st.markdown("### Opportunity Discovery")

    domain = st.selectbox(
        "Preferred Domain",
        ["Any", "Artificial Intelligence", "Software Engineering"]
    )

    work_mode = st.selectbox(
        "Preferred Work Mode",
        ["Any", "Remote", "Hybrid", "On-site"]
    )

    if st.button("Discover Opportunities", type="primary"):

        try:
            result = opportunity_discovery(
                OpportunityDiscoveryInput(
                    student_id=student_id.strip(),
                    preferred_domain=domain,
                    preferred_work_mode=work_mode
                )
            )

            st.success(
                f"Found {result.total_found} matching opportunities."
            )

            st.json(result.model_dump())

        except Exception as error:
            st.error(str(error))


elif selected_skill == "eligibility_verification":

    st.markdown("### Eligibility Verification")

    opportunity_id = st.text_input(
        "Opportunity ID",
        value="INT001"
    )

    if st.button("Verify Eligibility", type="primary"):

        try:
            result = eligibility_verification(
                EligibilityVerificationInput(
                    student_id=student_id.strip(),
                    opportunity_id=opportunity_id.strip()
                )
            )

            st.subheader("Verification Result")
            st.write(f"**Status:** {result.status}")

            if result.status == "eligible":
                st.success("Eligibility criteria passed.")
            elif result.status == "ineligible":
                st.error("The student does not meet the criteria.")
            else:
                st.warning(
                    "Official verification is required. "
                    "The student cannot proceed based on demo data."
                )

            st.json(result.model_dump())

        except Exception as error:
            st.error(str(error))


elif selected_skill == "application_preparation":

    st.markdown("### Application Preparation")

    opportunity_id = st.text_input(
        "Opportunity ID",
        value="INT001"
    )

    resume_available = st.checkbox(
        "Resume is available"
    )

    cover_letter_available = st.checkbox(
        "Cover letter is available"
    )

    if st.button("Prepare Application", type="primary"):

        try:
            result = application_preparation(
                ApplicationPreparationInput(
                    student_id=student_id.strip(),
                    opportunity_id=opportunity_id.strip(),
                    resume_available=resume_available,
                    cover_letter_available=cover_letter_available
                )
            )

            st.subheader("Application Readiness")

            st.write(
                f"**Status:** {result.readiness_status}"
            )

            st.info(result.message)

            st.markdown("### Remaining Checklist")

            if result.checklist:
                for item in result.checklist:
                    st.write(f"☐ {item}")
            else:
                st.success("All preparation checklist items are complete.")

            st.json(result.model_dump())

        except Exception as error:
            st.error(str(error))


st.divider()

st.caption(
    "Lab 3 demonstrates reusable, schema-typed skills "
    "that can be integrated into the Internship Application Portal."
)
