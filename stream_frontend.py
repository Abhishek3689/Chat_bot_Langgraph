from simple_chat import chatbot
from langchain_core.messages import HumanMessage
from langgraph.graph.message import BaseMessage,add_messages
import streamlit as st

st.title("chat with AI")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input =  st.chat_input("Ask Question")
if user_input:
    with st.chat_message('user'):
        st.text(user_input)
        st.session_state['chat_history'].append({'role':'user','content':user_input})
    with st.chat_message('assistant'):
        # ai_message = st.write_stream(
        #     message_chunk.content for message_chunk, metadata in chatbot.stream(
        #         {'messages': [HumanMessage(content=user_input)]},
            
        #         stream_mode= 'messages'
        #     )
        # )
        # st.session_state.chat_history.append({'role':'assistant','content':ai_message})

        ai_msg=[]
        for message_chunk,metadata in chatbot.stream({'messages':[HumanMessage(content=user_input)]}, stream_mode="messages"):
            ai_msg.append( message_chunk.content)
        st.session_state.chat_history.append({'role':'assistant','content':' '.join(ai_msg)})   
        st.write_stream(ai_msg)
        

