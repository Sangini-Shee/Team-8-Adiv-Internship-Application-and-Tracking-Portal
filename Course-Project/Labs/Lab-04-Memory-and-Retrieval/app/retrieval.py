
from app.memory_store import load_memories


def search_memories(
    user_id: str,
    query: str
):
    memories = load_memories()

    keywords = set(query.lower().split())

    results = []

    for memory in memories:

        if memory["user_id"] != user_id:
            continue

        searchable_text = (
            memory["content"] + " " +
            memory["category"] + " " +
            " ".join(memory["tags"])
        ).lower()

        matched_words = keywords.intersection(
            set(searchable_text.split())
        )

        if matched_words:
            results.append({
                **memory,
                "match_count": len(matched_words)
            })

    return sorted(
        results,
        key=lambda item: item["match_count"],
        reverse=True
    )
