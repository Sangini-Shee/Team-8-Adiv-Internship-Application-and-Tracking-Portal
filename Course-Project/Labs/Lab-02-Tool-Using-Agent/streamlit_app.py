
import streamlit as st

from app.agent import run_agent


st.set_page_config(
    page_title="Internship Assistant",
    page_icon="🎓",
    layout="wide"
)

# Header
st.title("🎓 AI Internship Application Assistant")

st.markdown(
    """
    Your intelligent internship assistant.
    
    Explore student profiles, internship opportunities,
    and eligibility using an AI-powered tool-using agent.
    """
)

# Sidebar
with st.sidebar:
    st.header("About the Assistant")

    st.write(
        "This assistant uses Gemini function calling "
        "to interact with Python tools and retrieve "
        "internship information."
    )

    st.divider()

    st.subheader("Available Features")

    st.write("👤 Student Profile")
    st.write("💼 Internship Opportunities")
    st.write("✅ Eligibility Checking")

    st.divider()

    st.caption(
        "Student and internship records are synthetic "
        "demonstration data."
    )

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
user_query = st.chat_input(
    "Ask about student profiles, internships or eligibility..."
)

if user_query:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Processing your request..."):

            response = run_agent(user_query)

        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
