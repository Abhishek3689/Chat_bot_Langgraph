import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END
# from langgraph.graph.messages import add_message
from langchain_core.messages import HumanMessage,AIMessage
from langchain_groq import ChatGroq
# from langgraph.checkpointer.memory import InMemoryCheckpointer
from typing import Annotated,TypedDict,List
from langgraph.graph.message import BaseMessage,add_messages



load_dotenv()

llm=ChatGroq(model='llama-3.1-8b-instant')

class Chat_message(TypedDict):
    messages: Annotated[List[BaseMessage],add_messages]

def llm_chat(state:Chat_message)->Chat_message:
    response=llm.invoke(state['messages'])
    return {'messages':[response]}    

# def graph
graph= StateGraph(Chat_message)

## add nodes
graph.add_node( "llm_chat",llm_chat)

## add edges
graph.add_edge(START,"llm_chat")
graph.add_edge("llm_chat",END)

## compile
chatbot=graph.compile()
                      
if __name__=="__main__":
    initial_state={'messages':[HumanMessage(content="what is the capital of India?")]}
    result=chatbot.invoke(initial_state)
    print("Chatbot response:", result['messages'][-1].content)