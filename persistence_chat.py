from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage,HumanMessage,BaseMessage
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict,Annotated,List


load_dotenv()

llm=ChatGroq(model='llama-3.1-8b-instant')

checkpointer=InMemorySaver()

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