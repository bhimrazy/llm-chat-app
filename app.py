import streamlit as st
from openai import OpenAI

# define model
MODEL = "phi3:3.8b-instruct" # ollama pull phi3:3.8b-instruct
SYSTEM_MESSAGE = {"role": "system", "content": "You are a helpful assistant."}
client = OpenAI(
    base_url="http://localhost:11434/v1/",  # ollama endpoint
    api_key="ollama",
)

st.title("Chat with an AI Assistant.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask anything?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        messages = [SYSTEM_MESSAGE, *st.session_state.messages]
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
