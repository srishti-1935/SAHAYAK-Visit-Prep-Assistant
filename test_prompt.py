from dotenv import load_dotenv
import os

load_dotenv()

from groq import Groq
import json
from prompt import build_prompt

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = build_prompt(
    symptoms="chest pain and breathlessness",
    hospital="Rajiv Gandhi Government General Hospital, Chennai",
    age=60,
    language="Tamil",
    has_scheme="Ayushman Bharat"
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3
)

raw = response.choices[0].message.content
clean = raw.replace("```json", "").replace("```", "").strip()

result = json.loads(clean)
print(json.dumps(result, indent=2, ensure_ascii=False))