from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from transformers import GPT2TokenizerFast
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Carregando Tokenizer...")
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
print("Tokenizer carregado.")

app = FastAPI(title="OtimizaIA - Comparador de Consumo de Prompts")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

class PromptRequest(BaseModel):
    texto: str

def contar_tokens(texto: str) -> int:
    if not texto:
        return 0
    return len(tokenizer.encode(texto))

def calcular_consumo(texto: str):

    tokens = contar_tokens(texto)
    
    agua_ml = tokens * 0.3217
    energia_wh = tokens * 0.34
    
    return round(agua_ml, 2), round(energia_wh, 4), tokens

@app.post("/analise")
async def analisar_prompt(request: PromptRequest):
    prompt_usuario = request.texto

    mensagem = f"""
    Você é um analisador de texto especialista em Engenharia de Prompt. 
    Analise o prompt abaixo e responda SOMENTE em JSON puro.
    
    Objetivo: Remova verbosidade, saudações desnecessárias e torne o prompt direto e eficiente para uma LLM, 
    mas mantenha a intenção original intacta.
    
    O JSON deve conter exatamente este formato:
    {{
      "partes_desnecessarias": [ "lista de trechos removidos..." ],
      "prompt_otimizado": "texto otimizado aqui..."
    }}

    Prompt Original: "{prompt_usuario}"
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        resposta = model.generate_content(mensagem)
        
        texto_resposta = resposta.text.strip()
        
        texto_limpo = texto_resposta.replace("```json", "").replace("```", "").strip()
        
        dados = json.loads(texto_limpo)
        partes_desnecessarias = dados.get("partes_desnecessarias", [])
        prompt_otimizado = dados.get("prompt_otimizado", "")
        
    except Exception as e:
        
        partes_desnecessarias = []
        prompt_otimizado = prompt_usuario
        dados = {
            "erro": f"Erro ao processar: {str(e)}",
            "resposta_original": texto_resposta if 'texto_resposta' in locals() else ""
        }

    agua_antes, energia_antes, tokens_antes = calcular_consumo(prompt_usuario)
    agua_depois, energia_depois, tokens_depois = calcular_consumo(prompt_otimizado)

    
    economia_agua = round(agua_antes - agua_depois, 2)
    economia_energia = round(energia_antes - energia_depois, 4)
    economia_tokens = tokens_antes - tokens_depois

    return {
        "analise": {
            "prompt_original": prompt_usuario,
            "prompt_otimizado": prompt_otimizado,
            "partes_desnecessarias": partes_desnecessarias
        },
        "metricas": {
            "tokens": {
                "antes": tokens_antes,
                "depois": tokens_depois,
                "economia": economia_tokens
            },
            "consumo_agua_ml": {
                "antes": agua_antes,
                "depois": agua_depois,
                "economia": economia_agua
            },
            "consumo_energia_wh": {
                "antes": energia_antes,
                "depois": energia_depois,
                "economia": economia_energia
            }
        }
    }
