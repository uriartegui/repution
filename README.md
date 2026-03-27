# Repution

Monitoramento inteligente de reputação de marca com IA.

## O que é

Repution coleta menções da sua empresa no Reclame Aqui, classifica automaticamente com IA e sugere respostas — tudo em um dashboard centralizado.

## Funcionalidades

- Coleta automática de reclamações (Reclame Aqui)
- Classificação com IA: sentimento, tipo e score de reputação
- Sugestão de resposta automática
- Alertas e dashboard em tempo real
- Coleta agendada a cada hora
- Deduplicação automática

## Stack

- **Backend:** Python + FastAPI + PostgreSQL + SQLAlchemy + Alembic
- **IA:** Groq (LLaMA 3)
- **Scraping:** Playwright
- **Frontend:** Next.js + Tailwind CSS

## Como rodar

### Pré-requisitos

- Python 3.12+
- Node.js 18+
- PostgreSQL

### Backend

```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
playwright install chromium
```

Crie o arquivo `.env` baseado no `.env.example`:

```bash
cp .env.example .env
```

Rode as migrations e suba o servidor:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse: `http://localhost:3000`

API docs: `http://localhost:8000/docs`

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | URL de conexão PostgreSQL |
| `GROQ_API_KEY` | Chave da API do Groq |
| `SECRET_KEY` | Chave secreta da aplicação |

## Licença

MIT
