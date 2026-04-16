
# 🚀 Text-to-SQL RAG Bot

A powerful dark-themed Natural Language to SQL interface that lets you chat with your MySQL database using plain English.

Ask questions, generate SQL automatically, execute queries, and get summarized insights — all in a seamless conversational experience.



## ✨ Overview

**Text-to-SQL RAG Bot** bridges the gap between business users and databases by eliminating the need to write complex SQL queries manually.

It combines **LLMs + Retrieval-Augmented Generation (RAG)** to:

- Understand natural language queries  
- Generate optimized SQL  
- Execute queries on your database  
- Return clean, summarized results  



## 🔥 Key Features

### 💬 Natural Language Querying

Ask questions like:

> "Show top 5 customers by revenue"  
> "What is the average order value this month?"

…and get instant results.


### ⚡ Intelligent SQL Generation

- Powered by **LangChain + Groq (GPT-OSS-20B)**  
- Converts natural language → optimized SQL queries  
- Handles joins, aggregations, filters, and edge cases  



### 🧠 RAG-Enhanced Context Awareness

- Uses schema-aware prompting  
- Improves accuracy by grounding responses in database structure  



### 🗂️ Persistent Chat Sessions

- Multiple chat sessions with unique IDs  
- Auto-generated titles for easy navigation  
- Context retained across conversations  



### 🌙 Modern Dark UI

- Clean, edge-to-edge dark theme  
- Built with **Streamlit** for simplicity + performance  
- Optimized for readability of query outputs  



### 🔐 Security First

- `.env` support for API key protection  
- `.gitignore` enforced to prevent leaks  
- Safe query execution practices  



## 🛠️ Tech Stack

| Layer              | Technology                     |
|-------------------|------------------------------|
| Frontend          | Streamlit                    |
| Orchestration     | LangChain                   |
| LLM               | Groq (OpenAI-compatible API)|
| Database          | MySQL                       |
| Env Management    | python-dotenv               |



Frontend	Streamlit
Orchestration	LangChain
LLM	Groq (OpenAI-compatible API)
Database	MySQL
