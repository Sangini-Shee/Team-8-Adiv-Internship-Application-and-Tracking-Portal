# Lab 04 – Memory and Retrieval

## 1. Overview
This lab demonstrates how an AI agent can store, retrieve, and manage persistent user-specific information. It uses a JSON-based memory store and keyword-based retrieval to provide relevant context when responding to user queries.

## 2. Objectives
- Implement persistent memory storage.
- Retrieve memories using relevant keywords.
- Maintain separate memories for different users.
- Support saving, searching, viewing, and deleting memories.
- Integrate memory functionality into an interactive application.

## 3. Technologies Used
- Python 3.12
- Streamlit
- JSON
- Pytest

## 4. Project Structure
```text
Lab-04-Memory-and-Retrieval/
├── app/
│   ├── __init__.py
│   ├── memory_store.py
│   ├── retrieval.py
│   └── agent.py
├── data/
│   └── memory.json
├── tests/
│   ├── conftest.py
│   └── test_memory.py
├── outputs/
├── main.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## 5. Implementation

### Memory Storage
Stores user information in a persistent JSON file with a unique identifier, user ID, category, tags, and timestamp.

### Memory Retrieval
Searches stored information using keywords and tags to identify relevant memories.

### Memory Agent
Provides functions to save information, recall relevant memories, and display a user's memory summary.

### User Interface
The Streamlit application provides three sections:
- Save Memory
- Search Memory
- Memory Dashboard

## 6. Testing
Run the automated tests:

```bash
python -m pytest -v
```

**Test coverage includes:**
- Saving memories
- Retrieving user-specific memories
- Searching stored memories
- Deleting memories
- Isolating memories between users

All 5 tests passed during verification.

## 7. Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the command-line application:

```bash
python main.py
```

Run the Streamlit application:

```bash
streamlit run streamlit_app.py
```

## 8. Outcome
Successfully implemented a persistent memory and retrieval system that stores user-specific information, searches relevant memories, and presents the results through a Streamlit interface.

## 9. Limitations
The current implementation uses local JSON storage and keyword-based retrieval. It does not yet use vector embeddings or a production database.
