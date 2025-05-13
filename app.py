import streamlit as st
import tempfile
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_ollama import ChatOllama

st.set_page_config(page_title="🧠 SQL Query Assistant", layout="centered")
st.title("🧠 Natural Language to SQL")

st.markdown("Yüklediğiniz `.db` dosyası üzerinde doğal dilde SQL sorguları oluşturun.")

# Kullanıcıdan .db dosyasını al
uploaded_file = st.file_uploader("Bir SQLite .db dosyası yükleyin", type=["db"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        tmp.write(uploaded_file.read())
        db_path = tmp.name

    # SQLDatabase bağla
    db_uri = f"sqlite:///{db_path}"
    db = SQLDatabase.from_uri(db_uri)

    # LLM modeli
    llm = ChatOllama(model="llama2:latest", temperature=0.0)
    chain = create_sql_query_chain(llm, db)

    # Kullanıcıdan soru al
    question = st.text_input("❓ Ne sormak istersiniz?", placeholder="Get the average age of active users.")

    if question:
        with st.spinner("🔎 Sorgu oluşturuluyor..."):
            try:
                result = chain.invoke({"question": question})
                st.success("✅ SQL sorgusu oluşturuldu ve çalıştırıldı.")
                st.code(result, language="sql")
            except Exception as e:
                st.error(f"❌ Hata: {e}")
else:
    st.warning("Lütfen önce bir .db dosyası yükleyin.")
