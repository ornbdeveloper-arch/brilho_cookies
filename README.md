# Brilho Cookies

Aplicacao para gestao de cookies, clientes, vendas e fidelidade. O frontend continua em HTML/CSS/JS puro, e os dados agora ficam persistidos no Supabase via backend FastAPI.

## Requisitos

- Python 3.11 ou superior
- Conta e projeto no Supabase

## Criar as tabelas no Supabase

1. Abra o painel do seu projeto no Supabase.
2. Acesse `SQL Editor`.
3. Cole e execute o conteudo de `backend/schema.sql`.

Esse script cria as tabelas:

- `cookies`
- `customers`
- `sales`

## Configurar variaveis de ambiente

Crie um arquivo `.env` dentro da pasta `backend`:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-do-supabase
```

Use a `service_role key` quando o backend ficar apenas no servidor/local da loja. Nao coloque essa chave diretamente no frontend.

## Instalar dependencias

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

No macOS/Linux, ative o ambiente com:

```bash
source .venv/bin/activate
```

## Rodar a API

```bash
cd backend
uvicorn main:app --reload
```

A API fica em `http://localhost:8000`.

## Deploy no Render

O arquivo `runtime.txt` fixa o Python em `3.12.7` para evitar builds com Python muito novo, como `3.14`, que podem tentar compilar dependencias nativas.

Configure o serviço como Web Service:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

No painel do Render, adicione:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-do-supabase
```

## Abrir o frontend

Na raiz do projeto, abra o `index.html` no navegador ou sirva a pasta:

```bash
python -m http.server 8080
```

Acesse `http://localhost:8080`.

Por padrao, o frontend chama `http://localhost:8000`. Se precisar usar outro endereco, defina antes de carregar `js/storage.js`:

```html
<script>
  window.BRILHO_API_URL = "http://localhost:8001";
</script>
```

## Endpoints principais

- `GET /` - resumo do dashboard
- `GET /cookies/`, `POST /cookies/`, `PUT /cookies/{id}`, `DELETE /cookies/{id}`
- `GET /clientes/`, `POST /clientes/`, `PUT /clientes/{id}`, `DELETE /clientes/{id}`
- `GET /vendas/`, `POST /vendas/`, `PATCH /vendas/{id}/pagar`, `PATCH /vendas/{id}/pendente`, `DELETE /vendas/{id}`
- `GET /fidelidade/` - ranking de fidelidade

## Estrutura

```text
brilho_cookies/
├── index.html
├── cookies.html
├── clientes.html
├── vendas.html
├── fidelidade.html
├── css/
├── js/
│   ├── storage.js
│   ├── ui.js
│   └── layout.js
└── backend/
    ├── main.py
    ├── database.py
    ├── schema.sql
    ├── requirements.txt
    └── routers/
```
