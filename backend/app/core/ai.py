import time
import json
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)
MODEL = "llama-3.1-8b-instant"


def _call_groq(messages: list, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.1,
            )
            return response.choices[0].message.content
        except Exception as e:
            if "rate_limit" in str(e) and attempt < retries - 1:
                wait = 10 * (attempt + 1)
                print(f"Rate limit atingido. Aguardando {wait}s...")
                time.sleep(wait)
            else:
                raise


def classify_mention(text: str) -> dict:
    prompt = f"""Analise o seguinte texto e classifique:

Texto: "{text}"

Responda APENAS em JSON neste formato exato:
{{
  "sentiment": "positive" | "neutral" | "negative",
  "type": "complaint" | "praise" | "question" | "crisis",
  "score": <número de 0 a 100 representando a reputação>,
  "summary": "<resumo em 1 frase>"
}}"""

    content = _call_groq([{"role": "user", "content": prompt}])
    return json.loads(content)


def generate_response(text: str, brand_tone: str = "profissional e cordial") -> str:
    prompt = f"""Você é um assistente de atendimento ao cliente.

Tom da marca: {brand_tone}

Menção recebida: "{text}"

Escreva uma resposta curta, empática e no tom indicado. Máximo 3 frases."""

    return _call_groq([{"role": "user", "content": prompt}])
