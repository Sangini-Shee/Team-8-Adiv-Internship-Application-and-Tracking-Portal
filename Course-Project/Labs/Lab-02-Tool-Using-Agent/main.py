
from app.agent import run_agent


def main():
    print("=" * 60)
    print("       AI INTERNSHIP APPLICATION ASSISTANT")
    print("=" * 60)

    print("\nWelcome to the Internship Portal!")
    print("You can ask me to:")
    print("1. View your student profile")
    print("2. View internship opportunities")
    print("3. Check internship eligibility")
    print("\nType 'exit' to close the application.")

    while True:
        print("\n" + "-" * 60)

        query = input("You: ").strip()

        if query.lower() in ["exit", "quit", "bye"]:
            print("\nThank you for using the Internship Assistant!")
            break

        if not query:
            print("Please enter a question.")
            continue

        print("\nAssistant: Processing your request...")

        response = run_agent(query)

        print("\nAssistant:")
        print(response)


if __name__ == "__main__":
    main()
