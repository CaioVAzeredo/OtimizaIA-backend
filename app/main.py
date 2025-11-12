from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="OtimizaIA - Analisador de Prompts")

class PromptRequest(BaseModel):
    texto: str

@app.post("/analise")
async def analisar_prompt(request: PromptRequest):
    prompt_usuario = request.texto

    # 🔹 Prompt aprimorado para garantir retorno JSON
    mensagem = f"""
    Você é um analisador de texto. Analise o prompt abaixo e responda SOMENTE em JSON puro,
    sem texto explicativo, comentários ou formatações extras.
    O JSON deve conter exatamente este formato:

    {{
      "partes_desnecessarias": [ "..." ],
      "prompt_otimizado": "..."
    }}

    Prompt: "{prompt_usuario}"
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    resposta = model.generate_content(mensagem)

    texto = resposta.text.strip()

    # 🔹 Corrige respostas que vêm com markdown ou texto extra
    texto_limpo = texto.replace("```json", "").replace("```", "").strip()

    try:
        dados = json.loads(texto_limpo)
    except Exception:
        dados = {
            "erro": "Não foi possível interpretar a resposta do modelo.",
            "resposta_original": texto
        }

    # 🔹 Cálculo de consumo (ajuste leve)
    consumo_agua_ml = len(prompt_usuario) * 0.5 / 100
    consumo_energia_wh = len(prompt_usuario) * 0.05 / 100

    return {
        "prompt_original": prompt_usuario,
        "analise": dados,
        "consumo_estimado": {
            "agua_ml": round(consumo_agua_ml, 2),
            "energia_wh": round(consumo_energia_wh, 2)
        }
    }
