"""Optional Swarms orchestration adapter.

Swarms agents require a configured model/provider. If no provider key is
available, the portal uses its deterministic specialist-agent pipeline.
"""
import os


def build_swarms_workflow():
    """Build a Swarms SequentialWorkflow when a provider key is configured."""
    keys = ("OPENAI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY")
    if not any(os.getenv(key) for key in keys):
        raise RuntimeError(
            "No LLM provider key configured. Use the local specialist-agent workflow."
        )

    from swarms import Agent, SequentialWorkflow

    model_name = os.getenv("SWARMS_MODEL", "gpt-4o")
    academic = Agent(
        agent_name="AcademicEligibilityAgent",
        system_prompt=(
            "Review the supplied structured academic eligibility result. "
            "Explain CGPA, backlog and credit checks. Do not change the result."
        ),
        model_name=model_name,
        max_loops=1,
    )
    skills = Agent(
        agent_name="SkillsMatchingAgent",
        system_prompt=(
            "Review supplied required, matched and missing skills. "
            "Explain the skill gap without inventing qualifications."
        ),
        model_name=model_name,
        max_loops=1,
    )
    career = Agent(
        agent_name="CareerGuidanceAgent",
        system_prompt=(
            "Summarize the supplied eligibility and skill analysis into "
            "career guidance. Never approve or reject an application."
        ),
        model_name=model_name,
        max_loops=1,
    )
    return SequentialWorkflow(
        name="InternshipPortalSpecialistWorkflow",
        description="Sequential academic, skills and career review.",
        agents=[academic, skills, career],
    )


def run_swarms_workflow(task: str) -> str:
    workflow = build_swarms_workflow()
    return str(workflow.run(task))
