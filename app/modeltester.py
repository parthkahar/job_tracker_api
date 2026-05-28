import ollama

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {"role": "user", "content": "say hello"}
    ]
)

print(response['message']['content'])