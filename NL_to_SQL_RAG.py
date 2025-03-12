import streamlit as st
import pandas as pd
import sqlite3
import ollama
import chromadb
import re

# Initialize ChromaDB for RAG storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="query_embeddings")

# Function to extract SQL query from LLM response
def extract_sql_query(response_text):
    match = re.findall(r"```sql\n(.*?)\n```", response_text, re.DOTALL)
    sql_query = match[0] if match else response_text
    sql_query = re.sub(r'FROM\s+["`\[]?[\w-]+["`\]]?', 'FROM QueryTable', sql_query, flags=re.IGNORECASE)
    return sql_query.strip()

# Function to validate SQL query columns
def validate_sql(sql_query, df_columns):
    for col in re.findall(r'SELECT (.*?) FROM', sql_query, re.IGNORECASE):
        if col.strip() not in df_columns and col.strip() != "*":
            return False, f"Invalid column: {col}"
    return True, "Valid SQL"

# Streamlit UI
st.title("📝 RAG-Based Natural Query to SQL Converter")
st.write("Convert natural language queries into SQL using Retrieval-Augmented Generation (RAG) with ChromaDB.")

# File Upload
uploaded_file = st.file_uploader("📂 Upload an Excel/CSV file", type=["xlsx", "csv"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
    
    # Store table in SQLite
    conn = sqlite3.connect(":memory:")
    df.to_sql("QueryTable", conn, if_exists="replace", index=False)
    
    schema_info = ", ".join([f"{col} ({str(df[col].dtype)})" for col in df.columns])
    st.subheader("📊 Sample Data Preview")
    st.write(df.head())
    
    # User Input for Natural Query
    natural_query = st.text_input("🔍 Enter your natural language query:")
    
    if st.button("Generate SQL Query"):
        if natural_query:
            # Retrieve similar past queries from ChromaDB (Improved Retrieval)
            results = collection.query(query_texts=[natural_query], n_results=5)
            similar_queries = "\n".join(results["documents"][0]) if results["documents"] else ""
            
            # Construct RAG-based prompt with strict rules (Better Prompting)
            prompt = f"""
            You are an SQL expert. Generate an accurate SQL query using ONLY the following schema:
            
            Table: QueryTable
            Columns: {schema_info}
            
            User Query: "{natural_query}"
            
            Here are similar past queries for reference:
            {similar_queries}
            
            Rules:
            1. Do not hallucinate columns, functions, or tables.
            2. Use ONLY the given schema.
            3. Wrap the SQL query inside triple backticks.
            
            Return only the SQL query.
            """
            
            response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
            raw_sql_output = response["message"]["content"]
            sql_query = extract_sql_query(raw_sql_output)
            
            # Display SQL Query
            st.subheader("🛠 Generated SQL Query")
            st.code(sql_query, language="sql")
            
            # Validate SQL before execution (Prevent Hallucination)
            is_valid, msg = validate_sql(sql_query, df.columns)
            if not is_valid:
                st.error(f"❌ {msg}")
            else:
                # Execute the query safely
                st.subheader("🔎 Query Results")
                try:
                    result_df = pd.read_sql_query(sql_query, conn)
                    st.dataframe(result_df)
                    
                    # Store the new query in ChromaDB for future retrieval
                    collection.add(documents=[natural_query], metadatas=[{"query": natural_query}], ids=[str(len(collection.get()["documents"]))])
                except Exception as e:
                    st.error(f"❌ SQL Execution Error: {e}")
    
    conn.close()
