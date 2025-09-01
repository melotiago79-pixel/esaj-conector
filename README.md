# e-SAJ Connector (Template para Render)

Este é um template mínimo de FastAPI para publicar no Render e obter uma URL estável.

## Endpoints
- `GET /health` -> `{"status":"ok"}`
- `GET /consulta?processo=CNJ` -> retorna JSON mínimo com `ok`, `numero` e campos opcionais.

## Deploy no Render (resumo)
1. Faça fork/clone ou envie estes arquivos para um repositório no GitHub.
2. No Render: New -> Web Service -> selecione o repo.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Salve. A URL ficará como `https://SEU-NOME.onrender.com`.

## OpenAPI para o GPT
Use `openapi.yaml` no seu GPT e troque o `servers.url` para a sua URL.
