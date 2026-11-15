
from app.agent import (
    remember_information,
    recall_information,
    get_memory_summary
)


def main():
    print("\n===== MEMORY AND RETRIEVAL AGENT =====")

    user_id = input("Enter Student ID: ").strip()

    while True:
        print("\n1. Save Memory")
        print("2. Search Memory")
        print("3. View All Memories")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            content = input("Enter information to remember: ").strip()
            category = input("Enter category: ").strip() or "general"
            tags = input("Enter tags (comma separated): ").split(",")

            result = remember_information(
                user_id,
                content,
                category,
                [tag.strip() for tag in tags if tag.strip()]
            )
            print("\nMemory saved successfully!")
            print(result)

        elif choice == "2":
            query = input("What do you want to recall? ").strip()
            results = recall_information(user_id, query)

            if results:
                print("\nMatching memories:")
                for memory in results:
                    print("-", memory["content"])
            else:
                print("\nNo matching memories found.")

        elif choice == "3":
            summary = get_memory_summary(user_id)
            print("\nTotal memories:", summary["total_memories"])

            for memory in summary["memories"]:
                print("-", memory["content"], "|", memory["category"])

        elif choice == "4":
            print("Exiting Memory Agent.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
