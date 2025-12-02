🌱 API para análise e otimização sustentável de prompts de IA

Este backend foi desenvolvido em FastAPI e utiliza o modelo Gemini 2.5 Flash para analisar prompts, identificar partes desnecessárias, otimizar o texto e calcular o consumo ambiental estimado em água e energia baseado na quantidade de tokens.

Ele também possui um sistema de métricas, contabilizando:

Tokens antes e depois

Água gasta (ml)

Energia gasta (Wh)

Economia total após otimização

🚀 Tecnologias Utilizadas

Python 3.10+

FastAPI

Uvicorn

Google Generative AI (Gemini API)

Transformers (GPT2 Tokenizer)

python-dotenv

CORS Middleware

📁 Estrutura do Projeto
OtimizaIA-backend/
│
├── .env
├── requirements.txt
└── main.py


O arquivo main.py contém todo o backend funcional.

🔑 Variáveis de Ambiente

Crie um arquivo .env na raiz do projeto:

GEMINI_API_KEY=COLOQUE_SUA_CHAVE_AQUI

🧱 Instalação
1️⃣ Criar ambiente virtual

Windows (PowerShell)

python -m venv venv
venv\Scripts\activate


Linux/Mac

python3 -m venv venv
source venv/bin/activate

2️⃣ Instalar dependências

Se tiver requirements.txt:

pip install -r requirements.txt


Ou instale manualmente:

pip install fastapi uvicorn
pip install python-dotenv
pip install google-generativeai
pip install transformers

▶ Rodando o servidor
uvicorn main:app --reload


A API ficará disponível em:

http://127.0.0.1:8000

📘 Documentação interativa:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

🔍 Endpoints
🔹 POST /analise

Analisa o texto enviado e retorna:

Prompt otimizado

Partes desnecessárias

Tokens antes/depois

Consumo de água e energia

Economia total

📤 Exemplo de requisição:
{
  "texto": "Olá, por favor, será que você poderia me explicar gentilmente o que é um átomo?"
}

📥 Exemplo de resposta:
{
  "analise": {
    "prompt_original": "Olá, por favor...",
    "prompt_otimizado": "Explique o que é um átomo.",
    "partes_desnecessarias": ["Olá", "por favor", "gentilmente"]
  },
  "metricas": {
    "tokens": {
      "antes": 40,
      "depois": 12,
      "economia": 28
    },
    "consumo_agua_ml": {
      "antes": 1.6,
      "depois": 0.48,
      "economia": 1.12
    },
    "consumo_energia_wh": {
      "antes": 0.16,
      "depois": 0.048,
      "economia": 0.112
    }
  }
}

🧠 Como o backend funciona internamente
🔹 1. Conta tokens usando GPT2Tokenizer

Isso simula o tamanho real do prompt.

🔹 2. Calcula consumo ambiental

Com base nos tokens:

Água: 0.04 ml por token

Energia: 0.004 Wh por token

🔹 3. Envia o texto ao Gemini

Com instruções rígidas para retornar JSON formatado.

🔹 4. Trata falhas da API

Se o Gemini retornar formato inválido ou falhar, o backend:

Não quebra

Retorna o prompt original

Informa erro na análise inteligente

📦 Atualizar dependências

Após instalar novas libs:

pip freeze > requirements.txt

🛑 Encerrar servidor
CTRL + C


E para sair do ambiente virtual:

deactivate