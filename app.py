import streamlit as st
import os
import uuid

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_classic.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate

#  Page Config  Theme CSS

st.set_page_config(page_title="SQL Insight AI", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    /* 1. Global App & Bottom Bar Background */
    .stApp, div[data-testid="stBottom"] { 
        background-color: #0E1117 !important; 
    }

    /* 2. User Input Box: Black text on Light Grey background */
    .stChatInput textarea {
        color: #000000 !important; /* Black text for contrast */
        background-color: #E0E0E0 !important; /* Light grey box */
        border-radius: 10px !important;
    }

    /* 3. Chat Window Outputs: Forced White Text */
    .stChatMessage p, .stChatMessage span, .stMarkdown {
        color: #FFFFFF !important; /* White text for answers */
    }

    /* 4. SQL Code Blocks: Dark background, no white glare */
    code { 
        color: #FF7B72 !important; 
        background-color: #161B22 !important; 
    }
    
    pre {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
    }

    /* 5. Sidebar & Header: Uniform Dark */
    [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
    header[data-testid="stHeader"] { background-color: #0E1117 !important; }
    div[data-testid="stDecoration"] { background-image: none !important; background-color: #0E1117 !important; }

    /* Titles */
    h1, h2, h3 { color: #58A6FF !important; }
    </style>
    """, unsafe_allow_html=True)


# Setup & Session State for Persistent Chats

load_dotenv()


if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    default_id = str(uuid.uuid4())
    st.session_state.all_chats[default_id] = {"name": "New Chat", "messages": []}
    st.session_state.current_chat_id = default_id

# ---------------------------
# 3. Sidebar - Navigation
# ---------------------------
with st.sidebar:
    st.title("📊 SQL Assistant")
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = {"name": "New Chat", "messages": []}
        st.session_state.current_chat_id = new_id
        st.rerun()

    st.markdown("---")
    st.subheader("📜 History")
    for chat_id, chat_data in st.session_state.all_chats.items():
        label = f"💬 {chat_data['name']}" if chat_id == st.session_state.current_chat_id else chat_data['name']
        if st.button(label, key=chat_id):
            st.session_state.current_chat_id = chat_id
            st.rerun()


#  LLM Connection

llm = ChatOpenAI(openai_api_key=GROQ_API_KEY, 
                 model="openai/gpt-oss-20b", 
                 base_url="https://api.groq.com/openai/v1", 
                 temperature=0)

#  Database Connection
db = SQLDatabase.from_uri(f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
 

#  SQL Generation Chain

custom_prompt = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template="""You are a MySQL expert. Return ONLY the SQL code. 
    Wrap column names with spaces in backticks.
    Schema: {table_info}
    Question: {input}
    /* Max: {top_k} */"""
)
chain = create_sql_query_chain(llm, db, prompt=custom_prompt)

#  Main Chat Display

current_chat = st.session_state.all_chats[st.session_state.current_chat_id]
st.title(current_chat["name"])

for msg in current_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


#    Chat Logic

question = st.chat_input("Ask your database a question...")

if question:
    # Setting  chat name based on first question
    if not current_chat["messages"]:
        current_chat["name"] = question[:30] + ("..." if len(question) > 30 else "")

    current_chat["messages"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    try:
        with st.spinner("🤖 Processing..."):
            # 1. Generate SQL
            raw_sql = chain.invoke({"question": question})
            clean_sql = raw_sql.replace("```sql", "").replace("```", "").strip().split(';')[0]
            
            # 2. Execute
            db_res = db.run(clean_sql)
            
            # 3. Final Summary
            summary_prompt = f"Question: {question}\nData: {db_res}\nExplain this result simply to the user:"
            final_ans = llm.invoke(summary_prompt).content
            
            full_response = f"**Answer:**\n{final_ans}\n\n---\n**SQL Query:**\n```sql\n{clean_sql}\n```"
            
            current_chat["messages"].append({"role": "assistant", "content": full_response})
            with st.chat_message("assistant"):
                st.markdown(full_response)
                
    except Exception as e:
        st.error(f"Error: {e}")