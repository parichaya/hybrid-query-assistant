"""
Query Router Module

This module implements the routing logic for a hybrid multi-agent system
that handles both structured and unstructured data queries.

Responsibilities:
- Analyze incoming user queries
- Route queries to SQL agent, RAG agent, or both
- Orchestrate execution across agents
- Use LLM-based synthesis to generate a final coherent response

Design:
- Deterministic routing (fast and reliable)
- Deterministic SQL execution
- Semantic retrieval via RAG
- Final response synthesis via local LLM (Ollama)

Author  : Parichaya Chatterji
        : chatterjiparichay@gmail.com
"""

from rag_agent import RAGAgent
from sql_agent import SQLAgent
import subprocess
import re


# ---------------------------
# ROUTER
# ---------------------------
class QueryRouter:
    def __init__(self):
        self.rag = RAGAgent()
        self.sql = SQLAgent()

        print("[Router] Initializing RAG index...")
        self.rag.build_index()
        print("[Router] Ready.")

    # ---------------------------
    # ROUTING LOGIC
    # ---------------------------
    def route(self, query):
        q = query.lower()

        if any(word in q for word in ["sales", "price", "stock"]):
            if any(word in q for word in ["feature", "review", "detail", "explain"]):
                return "both"
            return "sql"

        return "rag"

    # ---------------------------
    # HANDLE QUERY
    # ---------------------------
    def handle_query(self, query):
        route = self.route(query)

        route_label = {
            "sql": "SQL",
            "rag": "RAG",
            "both": "BOTH (SQL+RAG) with LLM Synthesis",
        }[route]

        print(f"\n[ROUTER] Route selected: {route_label}")

        if route == "sql":
            return self.sql.query(query)

        elif route == "rag":
            return self.rag.query(query)

        elif route == "both":
            sql_result = self.sql.query(query)
            rag_result = self.rag.query(query)

            return self.synthesize(query, sql_result, rag_result)

    # ---------------------------
    # LLM SYNTHESIS (FINAL FIXED)
    # ---------------------------
    def synthesize(self, query, sql_res, rag_res):
        # Extract numeric value from SQL result
        match = re.search(r"\d+", sql_res)
        numeric_value = match.group(0) if match else "UNKNOWN"

        prompt = f"""
You are an intelligent assistant.

You MUST include the exact numerical value provided below in your answer.

Query:
{query}

IMPORTANT FACT (MUST USE):
Sales = {numeric_value}

Additional Context:
{rag_res}

Instructions:
- ALWAYS include the exact number: {numeric_value}
- Do NOT say "not provided"
- Do NOT ignore the number
- Integrate it naturally into the answer
- Be concise (3–5 sentences)

Final Answer:
"""

        result = subprocess.run(
            ["ollama", "run", "phi3"],
            input=prompt,
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return result.stdout.strip()


# ---------------------------
# CLI TEST
# ---------------------------
if __name__ == "__main__":
    router = QueryRouter()

    while True:
        user_query = input("\nEnter query (or 'exit'): ")

        if user_query.lower() == "exit":
            break

        result = router.handle_query(user_query)

        print("\n=== FINAL ANSWER ===")
        print(result)