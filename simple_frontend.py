import streamlit as st
from simple_chat import chatbot
from langchain_core.messages import HumanMessage,BaseMessage


st.header("Simple Chatbot with LangGraph and Groq LLM")
if 'chat_message' not in st.session_state:
    st.session_state.chat_message=[]

for message in st.session_state.chat_message:
    with st.chat_message(message['role']):
        st.text(message['content'])
user_question=st.chat_input("Ask Question")
# st.header("Ask any question and get a response!")
if user_question:
    with st.chat_message("user"):
            st.write(user_question)
            st.session_state.chat_message.append({'role':'user','content':user_question})
    with st.chat_message("assistant"):
        initial_state={'messages':[HumanMessage(content=user_question)]}
        result=chatbot.invoke(initial_state)
        response=result['messages'][-1].content
        st.session_state.chat_message.append({'role':'assistant','content':response})
        st.write(response)
