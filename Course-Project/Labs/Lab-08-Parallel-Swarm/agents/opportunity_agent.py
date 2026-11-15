
import json
import asyncio
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "Labs" / "Lab-02-Tool-Using-Agent" / "data"


def load_opportunities():
    """Load internship opportunities from Lab 2."""
    file_path = DATA_DIR / "opportunities.json"

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict):
        return data.get("opportunities", [])

    return data


def analyze_opportunities():
    """Analyse available internships and their requirements."""

    opportunities = load_opportunities()
    results = []

    for opportunity in opportunities:
        required_skills = opportunity.get(
            "required_skills",
            opportunity.get("skills", [])
        )

        min_cgpa = opportunity.get(
            "min_cgpa",
            opportunity.get("minimum_cgpa", 0)
        )

        results.append({
            "internship_id": opportunity.get(
    "internship_id",
    opportunity.get("opportunity_id", opportunity.get("id"))
),
            "title": opportunity.get("title", "Unknown"),
            "company": opportunity.get("company", "Unknown"),
            "domain": opportunity.get("domain", "Not specified"),
            "required_skills": required_skills,
            "minimum_cgpa": min_cgpa,
            "work_mode": opportunity.get("work_mode", "Not specified"),
            "duration": opportunity.get(
    "duration",
    opportunity.get("duration_months", "Not specified")
),
            "availability": (
                "Demo listing - verification required"
                if opportunity.get("is_verified") is False
                or opportunity.get("approval_status") == "demo_only"
                else "Check approval status"
            )
        })

    return {
        "agent": "Opportunity Analyst Agent",
        "status": "success",
        "total_opportunities": len(results),
        "opportunities": results
    }


async def run_opportunity_agent():
    """Run opportunity analysis asynchronously."""
    return await asyncio.to_thread(analyze_opportunities)
