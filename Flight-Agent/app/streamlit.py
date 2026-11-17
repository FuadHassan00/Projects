"""Streamlit app for the Flight Agent."""

import sys
import json
from pathlib import Path
from uuid import uuid4

import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

# Project configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.agents.flight_agent import wf_builder


# Page configuration
st.set_page_config(
    page_title="Flight Agent",
    layout="wide"
)

st.title("Flight Search Agent")
st.caption("Search for cash and award flights using AI")


# Initialize LangGraph
@st.cache_resource
def initialize_agent():
    checkpointer = InMemorySaver()
    return wf_builder(checkpointer=checkpointer)


wf = initialize_agent()


# Initialize session state
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
with st.sidebar:
    st.header("Flight Agent")

    st.write("Search options:")
    st.write("Cash flights")
    st.write("Award flights")

    debug_mode = st.checkbox(
        "Debug Mode",
        value=True
    )

    if st.button("New Conversation"):
        st.session_state.thread_id = str(uuid4())
        st.session_state.messages = []
        st.rerun()


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        text = message["content"]
        formatted_text = text.replace("$", r"\$")
        st.markdown(formatted_text)


# Chat input
if prompt := st.chat_input("Where would you like to fly?"):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching flights..."):

            try:
                config = {
                    "configurable": {
                        "thread_id": st.session_state.thread_id
                    }
                }

                result = wf.invoke(
                    {
                        "messages": [
                            HumanMessage(content=prompt)
                        ]
                    },
                    config=config
                )

                # Extract final response
                response = result["messages"][-1].text()
                response_formatted = response.replace("$", r"\$")
                st.markdown(response_formatted)

                # Save response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

                # Debug tool execution
                if debug_mode:

                    with st.expander("LangGraph Debug Information"):

                        for i, message in enumerate(result["messages"]):

                            st.write(f"### Message {i + 1}")
                            st.write("Type:", message.type)

                            if message.type == "ai":

                                if message.tool_calls:
                                    st.write("Tool Calls:")
                                    st.json(message.tool_calls)

                                else:
                                    st.write("AI Response:")
                                    st.write(message.text())

                            elif message.type == "tool":

                                st.write("Tool Name:", message.name)

                                st.write("Tool Status:", message.status)

                                st.write("Tool Result:")
                                st.code(str(message.content)[:3000])

                            st.divider()

            except Exception as e:
                st.error(f"Flight search failed: {e}")

                if debug_mode:
                    st.exception(e)