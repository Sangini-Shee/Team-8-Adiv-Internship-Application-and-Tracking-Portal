
import app.memory_store as memory_store
import app.retrieval as retrieval
from app.agent import remember_information, recall_information


def test_save_memory(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"
    monkeypatch.setattr(memory_store, "MEMORY_FILE", test_file)

    result = remember_information(
        "STU001",
        "Interested in Python and machine learning",
        "skills",
        ["Python", "ML"]
    )

    assert result["user_id"] == "STU001"
    assert result["category"] == "skills"


def test_get_user_memories(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"
    monkeypatch.setattr(memory_store, "MEMORY_FILE", test_file)

    memory_store.save_memory("STU001", "Knows Python")
    memory_store.save_memory("STU002", "Knows Java")

    memories = memory_store.get_user_memories("STU001")

    assert len(memories) == 1
    assert memories[0]["content"] == "Knows Python"


def test_search_memories(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"
    monkeypatch.setattr(memory_store, "MEMORY_FILE", test_file)
    monkeypatch.setattr(
        retrieval, "load_memories", memory_store.load_memories
    )

    memory_store.save_memory(
        "STU001",
        "Interested in Python programming",
        "skills",
        ["Python"]
    )

    results = recall_information("STU001", "Python")

    assert len(results) >= 1
    assert "Python" in results[0]["content"]


def test_delete_memory(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"
    monkeypatch.setattr(memory_store, "MEMORY_FILE", test_file)

    memory = memory_store.save_memory("STU001", "Temporary memory")

    # Support either identifier field used by the memory store.
    memory_id = memory.get("id") or memory.get("memory_id")
    assert memory_id is not None

    assert memory_store.delete_memory(memory_id) is True
    assert memory_store.get_user_memories("STU001") == []


def test_user_memory_isolation(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"
    monkeypatch.setattr(memory_store, "MEMORY_FILE", test_file)

    memory_store.save_memory("STU001", "Python skills")
    memory_store.save_memory("STU002", "Java skills")

    assert len(memory_store.get_user_memories("STU001")) == 1
    assert len(memory_store.get_user_memories("STU002")) == 1
