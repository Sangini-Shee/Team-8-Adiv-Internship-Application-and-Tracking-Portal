
import asyncio

from agents.profile_agent import run_profile_agent
from agents.skill_agent import run_skill_agent
from agents.opportunity_agent import run_opportunity_agent


async def run_parallel_swarm(student_id):
    """
    Execute three specialized agents concurrently
    and combine their outputs.
    """

    print("\nStarting Parallel Agent Swarm...")
    print("Launching 3 agents concurrently...\n")

    profile_task = run_profile_agent(student_id)
    skill_task = run_skill_agent(student_id)
    opportunity_task = run_opportunity_agent()

    profile_result, skill_result, opportunity_result = (
        await asyncio.gather(
            profile_task,
            skill_task,
            opportunity_task,
            return_exceptions=True
        )
    )

    results = {
        "profile_analysis": profile_result,
        "skill_analysis": skill_result,
        "opportunity_analysis": opportunity_result
    }

    errors = [
        f"{name}: {result}"
        for name, result in results.items()
        if isinstance(result, Exception)
    ]

    if errors:
        return {
            "status": "error",
            "student_id": student_id,
            "errors": errors,
            "agent_results": results
        }

    failed_agents = [
        name for name, result in results.items()
        if result.get("status") == "error"
    ]

    return {
        "status": "completed" if not failed_agents else "partial",
        "student_id": student_id,
        "agents_executed": 3,
        "execution_mode": "parallel",
        "failed_agents": failed_agents,
        "agent_results": results
    }


def run_swarm(student_id):
    """Synchronous entry point for the parallel swarm."""
    return asyncio.run(run_parallel_swarm(student_id))
