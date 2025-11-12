# 🚀 OtimizaIA Backend

Este é o backend do projeto **OtimizaIA**, desenvolvido em **Python + FastAPI**.  
O objetivo do sistema é analisar prompts de IA e estimar o consumo de **água e energia** gerado por partes desnecessárias do texto.

---

## 🧱 Requisitos

Antes de começar, instale:

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/) *(opcional, se quiser clonar o repositório)*

---

## ⚙️ 1. Clonar o projeto

```bash
git clone https://github.com/seu-usuario/OtimizaIA-backend.git
cd OtimizaIA-backend

(Se você já tiver o projeto localmente, apenas entre na pasta.)
🐍 2. Criar ambiente virtual

Crie um ambiente virtual Python dentro da pasta do projeto:

python -m venv venv

Ative o ambiente virtual:
👉 Windows (PowerShell)

venv\Scripts\activate

👉 Linux / macOS

source venv/bin/activate

Quando ativado, você verá algo como:

(venv) PS C:\...\OtimizaIA-backend>

📦 3. Instalar dependências

Instale as bibliotecas necessárias:

pip install dotenv

pip install google-generativeai

pip install fastapi uvicorn

Se existir o arquivo requirements.txt, você também pode usar:

pip install -r requirements.txt

🧠 4. Estrutura básica do projeto

OtimizaIA-backend/
│
├── venv/               # ambiente virtual (não editar)
└── app/
    └── main.py         # ponto de entrada da aplicação

🚀 5. Rodar o servidor

Com o ambiente virtual ativo, execute:

uvicorn app.main:app --reload

Você verá algo como:

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

🌐 6. Acessar a API

Abra no navegador:

    Página inicial → http://127.0.0.1:8000

Documentação interativa (Swagger UI) → http://127.0.0.1:8000/docs

Documentação alternativa (ReDoc) → http://127.0.0.1:8000/redoc
🧩 7. Encerrar o servidor

Pressione CTRL + C no terminal para parar o servidor.
Para sair do ambiente virtual, use:

deactivate

💡 Dica

Se você quiser adicionar novas dependências no projeto (ex: SQLAlchemy, Pydantic etc.), instale com pip install nome_da_lib e atualize o arquivo requirements.txt:

pip freeze > requirements.txt