
import json
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

MEMORY_FILE = Path(__file__).resolve().parents[1] / "data" / "memory.json"


def load_memories():
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not MEMORY_FILE.exists():
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file).get("memories", [])


def save_memory(
    user_id: str,
    content: str,
    category: str = "general",
    tags: list[str] | None = None
):
    if not user_id.strip() or not content.strip():
        raise ValueError("User ID and memory content are required.")

    memories = load_memories()

    memory = {
        "memory_id": str(uuid4()),
        "user_id": user_id,
        "content": content,
        "category": category,
        "tags": tags or [],
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    memories.append(memory)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump({"memories": memories}, file, indent=4)

    return memory


def get_user_memories(user_id: str):
    return [
        memory for memory in load_memories()
        if memory["user_id"] == user_id
    ]


def delete_memory(memory_id: str):
    memories = load_memories()

    updated = [
        memory for memory in memories
        if memory["memory_id"] != memory_id
    ]

    if len(updated) == len(memories):
        return False

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump({"memories": updated}, file, indent=4)

    return True
