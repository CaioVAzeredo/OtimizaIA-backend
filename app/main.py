from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# 🔹 Carrega chave do Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="OtimizaIA - Comparador de Consumo de Prompts")

class PromptRequest(BaseModel):
    texto: str

@app.post("/analise")
async def analisar_prompt(request: PromptRequest):
    prompt_usuario = request.texto

    # 🔹 Prompt para o Gemini (solicitando análise JSON)
    mensagem = f"""
    Você é um analisador de texto. Analise o prompt abaixo e responda SOMENTE em JSON puro,
    sem explicações extras.
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
    texto_limpo = texto.replace("```json", "").replace("```", "").strip()

    try:
        dados = json.loads(texto_limpo)
        partes_desnecessarias = dados.get("partes_desnecessarias", [])
        prompt_otimizado = dados.get("prompt_otimizado", "")
    except Exception:
        partes_desnecessarias = []
        prompt_otimizado = ""
        dados = {
            "erro": "Não foi possível interpretar a resposta do modelo.",
            "resposta_original": texto
        }

    # =============================
    # 🔹 Cálculo de consumo realista
    # 1000 caracteres ≈ 500 ml e 0.5 Wh
    # =============================
    def calcular_consumo(texto: str):
        agua_ml = (len(texto) / 1000) * 500
        energia_wh = (len(texto) / 1000) * 0.5
        return round(agua_ml, 2), round(energia_wh, 4)

    agua_antes, energia_antes = calcular_consumo(prompt_usuario)
    agua_depois, energia_depois = calcular_consumo(prompt_otimizado)

    economia_agua = round(agua_antes - agua_depois, 2)
    economia_energia = round(energia_antes - energia_depois, 4)

    # =============================
    # 🔹 Resposta final da API
    # =============================
    return {
        "prompt_original": prompt_usuario,
        "prompt_otimizado": prompt_otimizado,
        "partes_desnecessarias": partes_desnecessarias,
        "consumo": {
            "antes": {
                "agua_ml": agua_antes,
                "energia_wh": energia_antes
            },
            "depois": {
                "agua_ml": agua_depois,
                "energia_wh": energia_depois
            },
            "economia": {
                "agua_ml": economia_agua,
                "energia_wh": economia_energia
            }
        }
    }
