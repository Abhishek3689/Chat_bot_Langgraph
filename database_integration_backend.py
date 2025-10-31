from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage,HumanMessage,BaseMessage
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict,Annotated,List
import sqlite3


load_dotenv()

llm=ChatGroq(model='llama-3.1-8b-instant')

conn=sqlite3.connect(database="chat_database.db",check_same_thread=False)


checkpointer=SqliteSaver(conn=conn)

class Chat_response(TypedDict):
    messages:Annotated[List[BaseMessage],add_messages]

def Chat_LLM(state:Chat_response):
    response=llm.invoke(state['messages'])
    return {'messages':[response]}

graph=StateGraph(Chat_response)

graph.add_node("Chat_LLM",Chat_LLM)

graph.add_edge(START,"Chat_LLM")
graph.add_edge("Chat_LLM",END)

chatbot=graph.compile(checkpointer=checkpointer)

# config={'configurable':{'thread_id':'thread1'}}
# initial_state={'messages':[HumanMessage(content='do you know my name')]}

# response=chatbot.invoke(initial_state,config=config)

# print(response['messages'][-1])

def get_all_threads():
    set_threads=set()
    for checkpoints in checkpointer.list(None):
        set_threads.add(checkpoints.config['configurable']['thread_id'])
    return list(set_threads)

# print(get_all_threads())
