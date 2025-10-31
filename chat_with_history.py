# from simple_chat import chatbot
from persistence_chat import chatbot
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from typing import TypedDict,Annotated,List
import streamlit as st
import uuid


# class Chat_response(TypedDict):
#     messages:Annotated[List[BaseMessage],add_messages]

def generate_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_id()
    st.session_state.thread_id=thread_id
    add_thread(thread_id)
    st.session_state['Chat_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['thread_chats']:
        st.session_state['thread_chats'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values.get('messages',[])



st.header("Chat with AI with Multiple Conversation")

if 'thread_chats' not in st.session_state:
    st.session_state['thread_chats']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_id()

if 'Chat_history' not in st.session_state:
    st.session_state.Chat_history=[]

add_thread(st.session_state['thread_id'])



selected_chat=None
with st.sidebar:
    new_chat=st.button("New Chat")
    if new_chat:
        reset_chat()
    st.header("My Conversations ")  
    for thread in st.session_state['thread_chats']:
        
        if st.button(str(thread)):
            st.session_state['thread_id']=thread
            messages=load_conversation(thread)

            temp_messages=[]
            for msg in messages:
                if isinstance(msg,HumanMessage):
                    role='user'
                else:
                    role='assistant'
                temp_messages.append({'role':role,'content':msg.content})

            st.session_state.Chat_history=temp_messages

    # for thread in st.session_state.thread_chats:
    #     st.write(thread)
    # for thread in st.session_state.thread_chats:
    #     if st.button(thread):
    #         st.session_state['thread_id']=thread
    


for message in st.session_state.Chat_history:
    with st.chat_message(message['role']):
        st.text(message['content'])




user_input=st.chat_input("Ask Query :")

if user_input:
    with st.chat_message("User"):
        st.text(user_input)
        st.session_state.Chat_history.append({'role':'user','content':user_input})
    config={'configurable':{'thread_id':st.session_state['thread_id']}}
    initial_state={'messages':[HumanMessage(content=user_input)]}    
    ai_msg=[]
    for msg_chunk,metadata in chatbot.stream(initial_state,config=config,stream_mode='messages'):
        ai_msg.append(msg_chunk.content)
    with st.chat_message('assistant'):
        st.write_stream(ai_msg)
        st.session_state.Chat_history.append({'role':'assistant','content':' '.join(ai_msg)})
