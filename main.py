import os
import sqlite3
import logging
import concurrent.futures
from dotenv import load_dotenv
from src.extract import extrair_dados_filme
from src.transform import transformar_dados_filme
from src.load import criar_tabelas, carregar_dados_no_banco

# Carrega as variáveis definidas no arquivo .env
load_dotenv()

# --- Configuração do Logging ---
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/etl.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Substitua 'YOUR_API_KEY' pela sua chave de acesso da OMDb API.
API_KEY = os.getenv("API_KEY")

# Lista de filmes a serem processados
TITULOS_FILMES = [
    "The Matrix", "Inception", "Interstellar", "Fight Club", 
    "Titanic", "Avatar", "Gladiator", "The Godfather", "Pulp Fiction","Batman Begins", "Superman"
]

def processar_filme(titulo):
    """
    Realiza a extração e transformação para um dado filme.
    Retorna os dados transformados ou None, caso haja erro.
    """
    logging.info(f"Iniciando o processamento para o filme: {titulo}")
    
    # Extração
    dados_brutos = extrair_dados_filme(titulo, API_KEY)
    if not dados_brutos:
        logging.error(f"Não foi possível extrair os dados para '{titulo}'.")
        return None
    
    # Transformação
    dados_transformados = transformar_dados_filme(dados_brutos)
    if not dados_transformados:
        logging.error(f"Erro na transformação dos dados para '{titulo}'.")
        return None

    return dados_transformados

def main():
    # Garante que a pasta 'db' exista
    db_folder = "db"
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    # Conexão com o banco de dados SQLite, agora na pasta 'db'
    db_path = os.path.join(db_folder, "filmes.db")
    conn = sqlite3.connect(db_path)
    criar_tabelas(conn)
    
    # Utiliza ThreadPoolExecutor com 4 workers para processar extração e transformação
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        resultados = list(executor.map(processar_filme, TITULOS_FILMES))
    
    # Realiza a carga dos dados de forma sequencial (para evitar conflitos com o SQLite)
    for dados in resultados:
        if dados is not None:
            carregar_dados_no_banco(conn, dados)
    
    conn.close()
    logging.info("Processo ETL concluído com sucesso.")

if __name__ == "__main__":
    main()
