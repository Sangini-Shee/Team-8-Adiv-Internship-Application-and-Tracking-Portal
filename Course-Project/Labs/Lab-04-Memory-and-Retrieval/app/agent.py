from app.memory_store import save_memory, get_user_memories
from app.retrieval import search_memories


def remember_information(user_id: str, content: str, category: str = "general", tags=None):
    return save_memory(
        user_id=user_id,
        content=content,
        category=category,
        tags=tags or []
    )


def recall_information(user_id: str, query: str):
    return search_memories(user_id, query)


def get_memory_summary(user_id: str):
    memories = get_user_memories(user_id)

    return {
        "user_id": user_id,
        "total_memories": len(memories),
        "memories": memories
    }