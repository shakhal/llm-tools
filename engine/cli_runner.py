class CliRunner:
    def __init__(self, client, engine, prompt):
        self.client = client
        self.prompt = prompt
        self.engine = engine

    # Main conversation loop
    def run(self):
        functions_desc = [ f["function"]["description"] for f in self.client.tools_schema]
        print("I am a chatbot able to do run some functions.", "Functions:\n\t",  "\n\t".join(functions_desc))
        print()

        messages = [{"role":'system', "content": self.prompt}]

        while True:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Assistant: Goodbye!")
                break
            if user_input.strip() == "":
                continue
            messages.append({"role": "user", "content": user_input})
            response = self.engine.chat_with_model(messages)
            print(f"Assistant: {response}")
            messages.append({"role": "assistant", "content": response})

