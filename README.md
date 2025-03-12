# 📝 RAG-Based Natural Query to SQL Converter

This project is a **Retrieval-Augmented Generation (RAG)** powered web application that converts natural language queries into **SQL queries** using **ChromaDB** and **Ollama (Llama 3.1)**. It provides a **Streamlit UI** to upload CSV/Excel files and interact with an AI model to generate and execute SQL queries in real time.

## 🚀 Features
- Upload **CSV/Excel** files and store them in an **SQLite database**.
- Convert **natural language queries into SQL** using Llama 3.1.
- **Retrieve past queries** using **ChromaDB** to improve query generation.
- **Validate SQL queries** to prevent AI hallucinations.
- Execute queries and **display results** in a structured format.

## 🏗️ Installation & Setup
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/repo-name.git
cd repo-name
```

### **2️⃣ Create Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the Application**
```bash
streamlit run app.py
```

## 🛠️ Project Structure
```
repo-name/
│── app.py               # Main Streamlit app
│── requirements.txt      # Dependencies
│── README.md            # Project documentation
│── .gitignore           # Git ignore file
└── data/                # Sample dataset folder
```

## 📜 Usage Guide
1. **Upload a CSV/Excel file**
2. **Enter a natural language query** (e.g., "Show total sales for January")
3. **Generate SQL query** using AI
4. **Validate & execute** the query
5. **View results** and refine queries if needed

## 💡 Future Improvements
- Add support for **multiple databases** (PostgreSQL, MySQL, etc.)
- Improve **SQL query validation**
- Add **user authentication** for query history
