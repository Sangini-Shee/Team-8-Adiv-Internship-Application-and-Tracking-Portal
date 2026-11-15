
import streamlit as st

from app.agent import (
    remember_information,
    recall_information,
    get_memory_summary
)

st.set_page_config(
    page_title="Memory and Retrieval Agent",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Memory and Retrieval Agent")
st.caption("Lab 04 – Persistent Memory and Context-Based Retrieval")

user_id = st.sidebar.text_input("Student ID", value="STU001").strip()

if not user_id:
    st.warning("Please enter a Student ID.")
    st.stop()

tab1, tab2, tab3 = st.tabs([
    "Save Memory",
    "Search Memory",
    "Memory Dashboard"
])

with tab1:
    st.subheader("Store New Information")

    content = st.text_area(
        "Information to remember",
        placeholder="Example: I am interested in Python and machine learning."
    )

    category = st.selectbox(
        "Category",
        ["general", "skills", "preferences", "education", "career", "projects"]
    )

    tags_input = st.text_input(
        "Tags (comma separated)",
        placeholder="Python, Machine Learning"
    )

    if st.button("Save Memory", type="primary"):
        if not content.strip():
            st.error("Please enter information to remember.")
        else:
            tags = [
                tag.strip()
                for tag in tags_input.split(",")
                if tag.strip()
            ]

            result = remember_information(
                user_id,
                content.strip(),
                category,
                tags
            )

            st.success("Memory saved successfully!")
            st.json(result)

with tab2:
    st.subheader("Retrieve Relevant Memories")

    query = st.text_input(
        "What would you like to recall?",
        placeholder="Example: Python skills"
    )

    if st.button("Search Memory"):
        if not query.strip():
            st.warning("Enter a search query.")
        else:
            results = recall_information(user_id, query.strip())

            if results:
                st.success(f"Found {len(results)} matching memories.")

                for memory in results:
                    with st.expander(memory["content"]):
                        st.write("Category:", memory["category"])
                        st.write("Tags:", ", ".join(memory.get("tags", [])))
                        st.write("Created:", memory.get("created_at", ""))
            else:
                st.info("No matching memories found.")

with tab3:
    st.subheader("Your Memory Dashboard")

    summary = get_memory_summary(user_id)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Stored Memories", summary["total_memories"])

    with col2:
        st.metric("Student ID", user_id)

    st.divider()

    if summary["memories"]:
        for memory in summary["memories"]:
            with st.expander(memory["content"]):
                st.write("Category:", memory["category"])
                st.write("Tags:", ", ".join(memory.get("tags", [])))
                st.write("Created:", memory.get("created_at", ""))
    else:
        st.info("No memories have been stored yet.")
