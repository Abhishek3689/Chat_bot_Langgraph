from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage,HumanMessage,BaseMessage
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict,Annotated,List
import sqlite3
from langchain.agents import create_agent
from utilities import web_search,calculator,Weather_data
from langgraph.prebuilt import ToolNode,tools_condition

load_dotenv()

# load Model
llm=ChatGroq(model='llama-3.1-8b-instant')

# make connection with sqlite
conn=sqlite3.connect(database="chat_database.db",check_same_thread=False)

checkpointer=SqliteSaver(conn=conn)

# tools binding
tools=[web_search, Weather_data,calculator]
llm_with_tools=llm.bind_tools(tools)

# agent=create_agent(
#     model=llm,
#     tools=[web_search, Weather_data,calculator],
#     system_prompt="You are a helpful assistant which has the ability to understand the user query understand intent \
#     and basis that give result and if necessary use tools to use."
# )

class Chat_response(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]

def Chat_LLM(state:Chat_response):
    """ You are a helpful assistant which has the ability to understand the user query understand intent \
    and basis that give result and if necessary use tools to use."""
    response=llm_with_tools.invoke(state['messages'])
    return {'messages':[response]}

tool_node=ToolNode(tools)

graph=StateGraph(Chat_response)

graph.add_node("Chat_LLM",Chat_LLM)
graph.add_node("tools",tool_node)

graph.add_edge(START,"Chat_LLM")
graph.add_conditional_edges("Chat_LLM",tools_condition)
graph.add_edge("tools","Chat_LLM")
# graph.add_edge("Chat_LLM",END)

chatbot=graph.compile(checkpointer=checkpointer)


def get_all_threads():
    set_threads=set()
    for checkpoints in checkpointer.list(None):
        set_threads.add(checkpoints.config['configurable']['thread_id'])
    return list(set_threads)


