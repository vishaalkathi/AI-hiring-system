import ollama

response = ollama.chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": "List the technical skills in: Python, FastAPI, PostgreSQL and Docker."
        }
    ]
)

print(response["message"]["content"])