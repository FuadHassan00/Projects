import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langchain.messages import AnyMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict, Annotated
from src.tools.awards_search_tool import search_awards_flights
from src.tools.search_cash_flights import search_cash_flights
from src.tools.cents_per_points import compare_cash_vs_points
from prompts.flight_agent_prompt import FLIGHT_AGENT_INSTRUCTIONS


# Load .env
load_dotenv(".env", override=True)

# Retrieve API key
api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0, 
        max_tokens=None,
        timeout=None,
        max_retries=2,
        top_p = 1)

class FlightState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


tools = [search_awards_flights, search_cash_flights, compare_cash_vs_points]

llm_with_tools = llm.bind_tools(tools)

def llm_agent(state: FlightState):
    messages = [
        SystemMessage(content=FLIGHT_AGENT_INSTRUCTIONS),*state["messages"]]
    
    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


def wf_builder(checkpointer):
    builder = StateGraph(FlightState)

    # Register nodes
    builder.add_node("agent", llm_agent)
    builder.add_node("tools", ToolNode(tools))

    # Define workflow
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    # Compile workflow
    wf = builder.compile(checkpointer=checkpointer)

    return wf


