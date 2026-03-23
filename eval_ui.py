import streamlit as st

st.set_page_config(page_title="Tenice - Asisten Chatbot ITENAS", layout="wide")

# Define Pages
chat_page = st.Page("pages/chat.py", title="Chat Interaktif", icon="💬", default=True)
eval_page = st.Page("pages/eval.py", title="Evaluasi Dataset", icon="📁")
data_page = st.Page("pages/data.py", title="Kelola Data Knowledge Base", icon="🗄️")

# Render Navigation
pg = st.navigation({
    "Menu Utama": [chat_page, eval_page, data_page]
})

pg.run()

