import httpx
import openai

openai.api_key = "sk-proj-5TPvRJvtvJVrOJ1Fd5SAT3BlbkFJszRuxiLZrvXI1DUtN1Q1"

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Translate the following English text to French: 'Hello, how are you?'",
    temperature=0.5,
    max_tokens=60
)

client = openai(
    api_key=“…”,
    http_client=httpx.Client(
        proxies=“…”),
)
print(response.choices[0].text.strip())
