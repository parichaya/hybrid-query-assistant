"""
RAG Agent Module

This module implements a Retrieval-Augmented Generation (RAG) pipeline
over unstructured text documents.

Responsibilities:
- Load and preprocess documents from the local data directory
- Split documents into chunks for semantic retrieval
- Generate vector embeddings using SentenceTransformers
- Store and query embeddings using FAISS
- Retrieve relevant context for a given user query
- Use a local LLM (via Ollama) to generate answers grounded in retrieved context

This module is designed to act as the "unstructured data agent"
within a larger multi-agent system.

Author  : Parichaya Chatterji
        : chatterjiparichay@gmail.com
"""

from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import subprocess


# ---------------------------
# CONFIG
# ---------------------------
DOCS_PATH = Path("data/docs")
EMBED_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "phi3"


# ---------------------------
# DOCUMENT LOADING
# ---------------------------
def load_documents():
    documents = []
    for file_path in DOCS_PATH.glob("*.txt"):
        loader = TextLoader(str(file_path))
        documents.extend(loader.load())
    return documents


# ---------------------------
# CHUNKING
# ---------------------------
def split_documents(documents):
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    return [doc.page_content for doc in chunks]


# ---------------------------
# RAG AGENT
# ---------------------------
class RAGAgent:
    def __init__(self):
        self.embedder = SentenceTransformer(EMBED_MODEL)
        self.index = None
        self.texts = []

    def build_index(self):
        documents = load_documents()
        self.texts = split_documents(documents)

        embeddings = self.embedder.encode(self.texts)
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

        print(f"[RAG] Indexed {len(self.texts)} chunks from {DOCS_PATH}")

    def retrieve(self, query, k=3):
        query_embedding = self.embedder.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), k)

        results = [self.texts[i] for i in indices[0]]

        return list(dict.fromkeys(results))

    def generate_answer(self, query, context):
        prompt = f"""
You are an expert assistant.

Use ONLY the provided context to answer.

Context:
{context}

Question:
{query}

Answer clearly in 3-4 sentences:
"""

        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"Ollama error: {result.stderr}")

        return result.stdout.strip()

    def query(self, query):
        if self.index is None:
            raise ValueError("Index not built. Call build_index() first.")

        retrieved_docs = self.retrieve(query)

        #context = "\n\n".join(retrieved_docs[:2])
        #More context while reducing hallucination risk:
        context = "\n\n".join(retrieved_docs[:3])

        return self.generate_answer(query, context)


# ---------------------------
# QUICK TEST
# ---------------------------
if __name__ == "__main__":
    rag = RAGAgent()
    rag.build_index()

    test_query = "What are the features of Nova X Smartphone?"
    print("\nQuery:", test_query)

    answer = rag.query(test_query)
    print("\nAnswer:\n", answer)