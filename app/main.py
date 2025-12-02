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

# Configuração do CORS (Permitindo conexão com seu Front-end React)
origins = ["*"] # Em produção, troque "*" pela URL do seu front (ex: http://localhost:5173)

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
    
    # --- CONSTANTES AJUSTADAS (Estimativas Realistas para Inferência) ---
    # Água: Estudos indicam aprox. 1 garrafa (500ml) para 20-50 turnos de conversa.
    # Estimativa conservadora: ~0.04 ml por token processado.
    fator_agua = 0.04
    
    # Energia: Inferência é muito eficiente. Estima-se entre 0.003 e 0.005 Wh por token.
    # Vamos usar 0.004 Wh (4 miliwatt-hora) como média.
    fator_energia = 0.004

    agua_ml = tokens * fator_agua
    energia_wh = tokens * fator_energia
    
    # Aumentei a precisão do arredondamento para não zerar valores pequenos
    return round(agua_ml, 3), round(energia_wh, 5), tokens

@app.post("/analise")
async def analisar_prompt(request: PromptRequest):
    prompt_usuario = request.texto

    # Prompt do sistema aprimorado para garantir JSON
    mensagem = f"""
    Você é um analisador de texto especialista em Engenharia de Prompt e Green Software. 
    Analise o prompt do usuário abaixo.
    
    Objetivo: 
    1. Identificar palavras desnecessárias, polidez excessiva ou redundâncias.
    2. Reescrever o prompt para ser direto e eficiente (menos tokens), mantendo a intenção original.
    
    Responda ESTRITAMENTE neste formato JSON:
    {{
      "partes_desnecessarias": ["exemplo1", "exemplo2"],
      "prompt_otimizado": "texto reescrito aqui"
    }}

    Prompt Original: "{prompt_usuario}"
    """

    try:
        # Verifique se o modelo 'gemini-2.5-flash' está disponível na sua conta.
        # Caso contrário, use 'gemini-1.5-flash'.
        model = genai.GenerativeModel("gemini-2.5-flash") 
        
        # generation_config força o retorno em JSON (disponível nos modelos flash mais recentes)
        resposta = model.generate_content(
            mensagem,
            generation_config={"response_mime_type": "application/json"}
        )
        
        texto_resposta = resposta.text.strip()
        
        # Parsing do JSON
        dados = json.loads(texto_resposta)
        partes_desnecessarias = dados.get("partes_desnecessarias", [])
        prompt_otimizado = dados.get("prompt_otimizado", "")
        
    except Exception as e:
        # Fallback em caso de erro na API ou no parse
        print(f"Erro na API ou Parse: {e}")
        partes_desnecessarias = ["Erro na análise inteligente: "]
        prompt_otimizado = prompt_usuario # Retorna o original para não quebrar
        
        # Opcional: Logar o erro completo para debug
        dados = {
            "erro": str(e),
            "resposta_bruta": texto_resposta if 'texto_resposta' in locals() else "Sem resposta"
        }

    # Cálculos Comparativos
    agua_antes, energia_antes, tokens_antes = calcular_consumo(prompt_usuario)
    agua_depois, energia_depois, tokens_depois = calcular_consumo(prompt_otimizado)

    economia_agua = round(agua_antes - agua_depois, 3)
    economia_energia = round(energia_antes - energia_depois, 5)
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