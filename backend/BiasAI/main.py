from BiasAI.claude import client

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[{"role": "user", "content": "you hate bias in unversity AI tools"}],
)
print(message.content)
