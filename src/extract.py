import requests
import logging

def extrair_dados_filme(titulo_filme, api_key):
    """
    Extrai os dados do filme a partir da OMDb API.

    Parâmetros:
      - titulo_filme: Nome do filme a ser consultado.
      - api_key: Chave de acesso da OMDb API.

    Retorna:
      - Um dicionário com os dados do filme ou None em caso de erro.
    """
    try:
        url = "http://www.omdbapi.com/"
        params = {"t": titulo_filme, "apikey": api_key}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Verifica se houve erro HTTP
        data = response.json()
        if data.get("Response") == "False":
            logging.error(f"Erro na API ao buscar '{titulo_filme}': {data.get('Error')}")
            return None
        logging.info(f"Dados extraídos para o filme: {titulo_filme}")
        return data
    except Exception as e:
        logging.exception("Erro ao extrair dados do filme.")
        return None
