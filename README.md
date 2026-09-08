# Quotes Scraper API

Web scraper de [quotes.toscrape.com](https://quotes.toscrape.com) com uma API em FastAPI
para consultar as frases coletadas.

## Como funciona

- `coletar_frases()` percorre todas as páginas do site e extrai texto e autor de cada frase.
- Os dados são salvos em `frases.json` e mantidos em memória.
- A API expõe endpoints para listar as frases e filtrar por autor.

## Requisitos

- Python 3.10+

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Executar

```bash
uvicorn index:app --reload
```

A coleta acontece automaticamente ao iniciar a aplicação.

## Endpoints

| Método | Rota                         | Descrição                              |
|--------|------------------------------|----------------------------------------|
| GET    | `/frases`                    | Lista todas as frases coletadas        |
| GET    | `/frases/autor/{nome_autor}` | Filtra frases por autor (busca parcial)|

Documentação interativa em `http://127.0.0.1:8000/docs`.

## Exemplo

```bash
curl http://127.0.0.1:8000/frases
curl http://127.0.0.1:8000/frases/autor/einstein
```
