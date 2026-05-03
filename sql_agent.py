"""
SQL Agent Module

This module provides deterministic access to structured data stored in a SQLite database.

Responsibilities:
- Interpret user queries related to structured data (e.g., sales, product info)
- Extract relevant entities such as product names
- Execute safe, parameterized SQL queries against the database
- Return clean, human-readable results

Design Decisions:
- Uses deterministic logic instead of LLM-based SQL generation to ensure reliability and speed
- Avoids SQL injection via parameterized queries
- Keeps logic simple and extensible for additional query types (e.g., pricing, inventory)

Role in System:
- Acts as the "structured data agent" in a hybrid multi-agent architecture
- Complements the RAG agent (which handles unstructured data)

Author  : Parichaya Chatterji
        : chatterjiparichay@gmail.com
"""

import sqlite3
from pathlib import Path


# ---------------------------
# CONFIG
# ---------------------------
DB_PATH = Path("data/products.db")


# ---------------------------
# SQL AGENT
# ---------------------------
class SQLAgent:
    def __init__(self):
        if not DB_PATH.exists():
            raise FileNotFoundError(f"Database not found at {DB_PATH}")

        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

    # ---------------------------
    # MAIN QUERY HANDLER
    # ---------------------------
    def query(self, question):
        question_lower = question.lower()

        # ---------------------------
        # SALES QUERY
        # ---------------------------
        if "sales" in question_lower:
            product = self.extract_product_name(question)

            if not product:
                return "Could not identify product."

            return self.get_sales(product)

        return "Query not supported yet."

    # ---------------------------
    # EXTRACT PRODUCT NAME
    # ---------------------------
    def extract_product_name(self, question):
        products = [
            "Acme Pro Laptop",
            "Zenith Ultra Laptop",
            "Nova X Smartphone",
            "Orbit Lite Phone",
            "Vertex Pro Phone"
        ]

        for p in products:
            if p.lower() in question.lower():
                return p

        return None

    # ---------------------------
    # EXECUTE SALES QUERY
    # ---------------------------
    def get_sales(self, product_name):
        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT sales FROM products WHERE name = ?",
            (product_name,)
        )

        row = cursor.fetchone()

        if not row:
            return "No results found."

        return f"sales: {row['sales']}"


# ---------------------------
# TEST
# ---------------------------
if __name__ == "__main__":
    agent = SQLAgent()

    q = "What are the sales of Nova X Smartphone?"
    print("\nQuestion:", q)

    result = agent.query(q)

    print("\nResult:\n", result)