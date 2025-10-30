from persistence_chat import chatbot
from langchain_core.messages import HumanMessage
import streamlit as st

st.header("Chat with LLM with Persistence")
config={'configurable':{'thread_id':'thread1'}}

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.text(message['content'])
        
user_input=st.chat_input("Ask Query")

if user_input:
    with st.chat_message('user'):
        initial_state={'messages':[HumanMessage(content=user_input)]}
        st.text(user_input)
        st.session_state.chat_history.append({'role':'user','content':user_input})

    with st.chat_message('assistant'):
        ai_msg=[]
        for msg_chunk,metadata in chatbot.stream(initial_state,config=config,stream_mode='messages'):
            ai_msg.append(msg_chunk.content)
        st.write_stream(ai_msg)
        st.session_state.chat_history.append({'role':'assistant','content':' '.join(ai_msg)})
