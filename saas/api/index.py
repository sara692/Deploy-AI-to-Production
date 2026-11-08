import os
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

@app.get("/api")
def idea():
    prompt = [{"role": "user", "content": "Come up with a new business idea for AI Agents"}]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=prompt,
    )
    return PlainTextResponse(response.choices[0].message.content)