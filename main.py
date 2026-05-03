"""
Main Entry Point

This module serves as the entry point for the Hybrid Query Assistant.

Responsibilities:
- Initialize the Query Router
- Provide a simple command-line interface (CLI)
- Accept user queries and display responses

Usage:
    python main.py

Author  : Parichaya Chatterji
        : chatterjiparichay@gmail.com
"""

from router import QueryRouter


def main():
    print("=== Hybrid Query Assistant ===")
    print("Type your query below (type 'exit' to quit)\n")

    router = QueryRouter()

    while True:
        try:
            user_query = input("\n> ")

            if user_query.strip().lower() == "exit":
                print("Exiting...")
                break

            if not user_query.strip():
                continue

            result = router.handle_query(user_query)

            print("\n=== RESPONSE ===")
            print(result)

        except KeyboardInterrupt:
            print("\nExiting...")
            break

        except Exception as e:
            print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    main()
