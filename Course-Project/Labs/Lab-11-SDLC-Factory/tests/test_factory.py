
import pytest

from agents.requirement_agent import analyze_requirements
from agents.design_agent import generate_design
from agents.code_agent import generate_code_skeleton, save_generated_code
from agents.testing_agent import generate_test_plan
from agents.documentation_agent import generate_documentation
from factory.orchestrator import run_sdlc_factory


@pytest.fixture
def sample_description():
    return (
        "The system allows students to register and login. "
        "Students can search and apply for internships. "
        "The system must be secure and reliable."
    )


@pytest.fixture
def sample_requirements(sample_description):
    return analyze_requirements(sample_description)


@pytest.fixture
def sample_design(sample_requirements):
    return generate_design(sample_requirements)


@pytest.fixture
def sample_code(sample_design):
    return generate_code_skeleton(
        "Internship Portal",
        sample_design
    )


def test_requirement_analysis(sample_requirements):
    assert sample_requirements["status"] == "completed"
    assert len(sample_requirements["functional_requirements"]) > 0


def test_non_functional_requirements(sample_requirements):
    assert len(sample_requirements["non_functional_requirements"]) > 0


def test_empty_requirements():
    with pytest.raises(ValueError):
        analyze_requirements("")


def test_design_generation(sample_design):
    assert sample_design["status"] == "completed"
    assert sample_design["architecture"] == "Layered Architecture"


def test_design_components(sample_design):
    assert len(sample_design["components"]) == 4


def test_code_generation(sample_code):
    assert sample_code["status"] == "completed"
    assert sample_code["file_count"] == 4
    assert "main.py" in sample_code["generated_files"]


def test_empty_project_name(sample_design):
    with pytest.raises(ValueError):
        generate_code_skeleton("", sample_design)


def test_code_file_saving(sample_code, tmp_path):
    path = save_generated_code(sample_code, tmp_path)

    from pathlib import Path
    project_path = Path(path)

    assert project_path.exists()
    assert (project_path / "main.py").exists()


def test_testing_agent(sample_requirements, sample_code):
    result = generate_test_plan(sample_requirements, sample_code)

    assert result["status"] == "completed"
    assert result["total_test_cases"] >= 4


def test_documentation_generation(
    sample_requirements,
    sample_design,
    sample_code
):
    testing = generate_test_plan(sample_requirements, sample_code)

    result = generate_documentation(
        "Internship Portal",
        sample_requirements,
        sample_design,
        sample_code,
        testing
    )

    assert result["status"] == "completed"
    assert "# Internship Portal" in result["documentation"]
    assert "Testing Plan" in result["documentation"]


def test_complete_sdlc_workflow(tmp_path, monkeypatch):
    import factory.orchestrator as orchestrator

    monkeypatch.setattr(
        orchestrator,
        "__file__",
        str(tmp_path / "factory" / "orchestrator.py")
    )

    result = run_sdlc_factory(
        "Internship Portal",
        "Students can register and search internships. "
        "The system must be secure."
    )

    assert result["status"] == "completed"
    assert result["agents_executed"] == 5
    assert result["testing_plan"]["total_test_cases"] >= 4


def test_invalid_project_name():
    with pytest.raises(ValueError):
        run_sdlc_factory("", "A valid project description.")
