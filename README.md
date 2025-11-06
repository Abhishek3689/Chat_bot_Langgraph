## 💬 LANGGRAPH Chatbot – Persistent Multi-Conversation AI+ Intelligent Agents
### 🧠 A memory-based AI chatbot powered by LangGraph, Streamlit, SQLite, and Agents
<img width="1350" height="567" alt="image" src="https://github.com/user-attachments/assets/4b29c89d-ab43-472e-9f23-93d20ee01c8c" />
🚀 Overview

**LANGGRAPH Chatbot is an interactive conversational AI web app built using Streamlit, designed to simulate real-world chat memory.**
- Unlike regular chatbots that forget old messages, this one stores and recalls past conversations — even after you close and reopen the app!**

All chat history is securely stored in a SQLite database, allowing:

🗂️ Multiple independent chat sessions

🤖 Integrated Agent System – The chatbot now leverages LangGraph Agents, allowing dynamic reasoning and tool usage:

- Web search or knowledge retrieval
- Weather Data
- Calculator or data-based reasoning
- Context-aware query handling

💾 Persistent memory across sessions and restarts

⚡ Smooth user experience with a Streamlit UI

Whether you return after hours or days, your previous chats remain right where you left them.

### 🧩 Key Features

- ✅ Streamlit-based UI – simple, interactive, and fast
- ✅ Persistent chat memory – powered by SQLite
- ✅ Multiple conversations – continue from any thread
- ✅ Configurable user interface – view and select past chats
- ✅ Extendable backend – can integrate with LLMs (e.g., OpenAI, Hugging Face)

### Steps To use

- cd your-repo
- clone the repo
```
git clone https://github.com/Abhishek3689/Chat_bot_Langgraph.git
```
- create virtual env
 ```
python -m venv venv
```
- activate environment
```
source venv/bin/activate
```
or On Windows: venv\Scripts\activate
- install dependencies
```
pip install -r requirements.txt
```
- Run
```
python datasase_frontend.py
```
