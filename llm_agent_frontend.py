from llm_agent_backend import chatbot,get_all_threads
from langchain_core.messages import HumanMessage,AIMessage
import streamlit as st
import uuid


# """********************************Basic Utility Function********************************"""

## Generate unique thread id
def generate_id():
    thread_id=uuid.uuid4()
    return thread_id

## function to start a new chat
def reset_chat():
    thread_id=generate_id()
    st.session_state['thread_id']=thread_id
    add_thread(thread_id)
    st.session_state['chat_history']=[]

## function to add thread id to Chat threads session
def add_thread(thread_id):
    if thread_id not in st.session_state['Chat_threads']:
        st.session_state['Chat_threads'].append(thread_id)

## function to load conversation based on specific thread id
def load_conversation(thread_id):
    config={'configurable':{'thread_id':thread_id}}
    state=chatbot.get_state(config=config).values.get('messages',[])
    return state

# """******************************** Streamlit setup ********************************"""

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

if 'Chat_threads' not in st.session_state:
    st.session_state['Chat_threads']=get_all_threads()

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_id()

 
# """********************************Frontend code********************************"""   

st.title("LangGraph Chatbot – Persistent Multi-Conversation Memory")


add_thread(st.session_state['thread_id'])


with st.sidebar:
    st.header("Click for Conversation")
    if st.button("New Chat"):
        reset_chat()
    st.subheader("My Conversations")
    col1, col2 = st.columns([1, 4])
    with col2:
        conversations = st.session_state['Chat_threads']
        for i, thread in enumerate(conversations[::-1]):
            with st.expander(f"Conversation {i+1}"):
                if st.button(f"Open {thread}"):
                    st.session_state['thread_id'] = thread
                    messages = load_conversation(thread)
                    temp_messages = []
                    for msg in messages:
                        if isinstance(msg, HumanMessage):
                            role = 'user'
                        else:
                            role = 'assistant'
                        temp_messages.append({'role': role, 'content': msg.content})
                    st.session_state['chat_history'] = temp_messages

## *********************************Getting messages stored in session ****************************        
for message in st.session_state['chat_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

## *********************************user and Assistant Interation****************************
user_input=st.chat_input("Ask Query: ")
if user_input:
    ## user query

    with st.chat_message("user"):
        st.text(user_input)
        st.session_state['chat_history'].append({'role':'user','content':user_input})

    config={'configurable':{'thread_id':st.session_state['thread_id']}}
    initial_state={'messages':[HumanMessage(content=user_input)]}
    ## AI Response
    ai_msg=[]
    with st.chat_message("assistant"):
        def ai_stream():
            for msg_chunks,metadata in chatbot.stream(initial_state,config=config,stream_mode='messages'):
                if isinstance(msg_chunks,AIMessage):
                    yield msg_chunks.content
                
        ai_msg=st.write_stream(ai_stream()) 
        st.session_state['chat_history'].append({'role':'assistant','content':' '.join(ai_msg)})

