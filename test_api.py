from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "A 60-year-old patient has chest pain and breathlessness. Which OPD department should they go to at a government hospital?"}],
    temperature=0.3
)

print(response.choices[0].message.content)