# Hybrid Query Assistant

A locally running, multi-agent AI system that answers user queries by combining **structured (SQL)** and **unstructured (RAG)** data sources.

---

## 🚀 Overview

This project implements a **hybrid retrieval architecture**:

- Structured data → queried via SQLite (deterministic SQL agent)
- Unstructured data → retrieved using RAG (Retrieval-Augmented Generation)
- Final responses → optionally synthesized using a local LLM (Ollama)

The system intelligently routes queries to the appropriate agent and combines results when needed.

---

## 🧠 What is RAG?

**RAG (Retrieval-Augmented Generation)** is a technique where:

- relevant documents are retrieved first  
- then passed to a language model to generate grounded answers  

This improves factual accuracy by anchoring responses in real data.

---

## 🏗️ Architecture

```
User Query
   ↓
Query Router
   ↓
 ┌───────────────┬───────────────┐
 │               │               │
SQL Agent     RAG Agent      BOTH
 │               │               │
 └───────→ LLM Synthesis ←───────┘
                 ↓
           Final Answer
```

---

## ⚙️ Components

### 1. SQL Agent (Structured Data)

- Uses SQLite (`products.db`)
- Handles queries like:
  - product sales
  - pricing
  - inventory

**Design Decision:**

> Initially experimented with LLM-based SQL generation, but due to latency and reliability issues with local models, implemented a deterministic query layer for structured data while keeping LLMs for unstructured retrieval and synthesis.

---

### 2. RAG Agent (Unstructured Data)

- Processes text files from `data/docs/`
- Uses:
  - SentenceTransformers (embeddings)
  - FAISS (vector search)
  - Ollama (local LLM)

Handles queries like:

- product features  
- company info  
- policies  

---

### 3. Query Router

- Lightweight rule-based routing  
- Determines:
  - SQL → structured queries  
  - RAG → semantic queries  
  - BOTH → hybrid queries  

---

### 4. LLM Synthesis

- Combines structured + unstructured outputs  
- Ensures:
  - coherent answers  
  - natural language output  
  - preservation of key numerical values  

---

## 🧰 Tech Stack

**Core Technologies:**
- Python 3.11  
- SQLite (structured data)  
- FAISS (vector search)  
- SentenceTransformers (embeddings)  

**LLM Runtime:**
- Ollama (local inference)  
- Model used: `phi3`  

**Why `phi3`:**
- lightweight and fast on CPU  
- suitable for local inference (no GPU required)  
- good balance between speed and response quality  

---

## 📦 Key Dependencies

(Full list in `requirements.txt`)

- sentence-transformers  
- faiss-cpu  
- langchain  
- langchain-community  
- langchain-text-splitters  

---

## 🗄️ Data

### Structured Data (SQLite)

Database: `data/products.db`

- **products**: id, name, category, price, sales, rating  
- **inventory**: id, product_id (FK → products.id), region, stock  

Sample Data:

| name                | category | price | sales | rating |
|---------------------|----------|-------|-------|--------|
| Nova X Smartphone   | Phone    | 999   | 1500  | 4.5    |
| Orbit Lite Phone    | Phone    | 399   | 1100  | 4.0    |


---

### Unstructured Data

Located in: `data/docs/`

Includes:

- product descriptions  
- FAQs  
- company overview  
- policies (shipping, returns)  

These documents are chunked, embedded, and indexed for semantic retrieval.

---

## ▶️ How to Run

```bash
python main.py
```

Then enter queries such as:

```
What are the sales of Nova X Smartphone?
What are the features of Nova X Smartphone?
What are the sales of Nova X Smartphone and what are its features?
```

---

## 🧪 Example

**Input:**

```
What are the sales of Nova X Smartphone and what are its features?
```

**Output (example):**

```
The Nova X Smartphone has recorded sales of 1500 units and features a 6.5-inch display, 5G connectivity, and a 48MP camera...
```

---

## 🔍 Design Highlights

- Fully local (no external APIs)  
- Deterministic + probabilistic hybrid system  
- Modular architecture (agents + router)  
- Fast and reliable structured queries  
- Context-grounded unstructured responses  

---

## ⚠️ Notes & Future Improvements

### Model Monitoring & Updates

- Track response quality (accuracy, hallucination rate)  
- Evaluate latency (especially RAG + synthesis)  
- Swap models easily via Ollama (e.g., `phi3` → larger models if needed)  
- Periodically re-embed documents if data changes  

### Potential Enhancements

- Smarter intent classification (ML-based routing)  
- Better prompt tuning for synthesis  
- Streaming responses  
- UI layer (web interface)  

---

## 📌 Summary

This project demonstrates how to combine:

- deterministic data systems (SQL)  
- semantic retrieval (RAG)  
- local LLM reasoning  

into a **practical, hybrid AI assistant**.

---

## 👤 Author

Parichaya Chatterji  

📧 chatterjiparichay@gmail.com