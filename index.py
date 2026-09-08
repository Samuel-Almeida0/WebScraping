import json
import logging
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://quotes.toscrape.com"


def coletar_frases():
    """Percorre todas as páginas do site e coleta texto + autor de cada frase."""
    frases = []
    pagina_num = 1

    while True:
        url = f"{BASE_URL}/page/{pagina_num}/"
        logger.info(f"Coletando página {pagina_num}...")

        try:
            resposta = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as erro:
            logger.error(f"Erro de conexão na página {pagina_num}: {erro}")
            break

        if resposta.status_code != 200:
            logger.info(f"Página {pagina_num} não encontrada (status {resposta.status_code}). Encerrando.")
            break

        soup = BeautifulSoup(resposta.text, "html.parser")
        blocos_frases = soup.find_all("div", class_="quote")

        if not blocos_frases:
            logger.info("Nenhuma frase encontrada nesta página. Fim da paginação.")
            break

        for bloco in blocos_frases:
            texto = bloco.find("span", class_="text").text
            autor = bloco.find("small", class_="author").text
            frases.append({"texto": texto, "autor": autor})

        pagina_num += 1

    logger.info(f"Coleta finalizada: {len(frases)} frases encontradas.")
    return frases


def salvar_json(frases, caminho="frases.json"):
    """Salva os dados coletados em um arquivo JSON."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(frases, arquivo, ensure_ascii=False, indent=2)
    logger.info(f"Dados salvos em {caminho}")


# --- Coleta os dados uma vez, ao iniciar a aplicação ---
frases_coletadas = coletar_frases()
salvar_json(frases_coletadas)

# --- API ---
app = FastAPI(title="Quotes Scraper API")


@app.get("/frases")
def listar_frases():
    """Retorna todas as frases coletadas."""
    return frases_coletadas


@app.get("/frases/autor/{nome_autor}")
def frases_por_autor(nome_autor: str):
    """Retorna todas as frases de um autor específico."""
    resultado = [
        f for f in frases_coletadas
        if nome_autor.lower() in f["autor"].lower()
    ]

    if not resultado:
        raise HTTPException(status_code=404, detail=f"Nenhuma frase encontrada para o autor '{nome_autor}'")

    return resultado


# Para rodar: uvicorn scraper_api:app --reload