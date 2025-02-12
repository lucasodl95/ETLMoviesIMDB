import datetime
from dateutil.relativedelta import relativedelta
import logging

def transformar_dados_filme(dados_brutos):
    """
    Transforma os dados extraídos para atender aos requisitos:
      - Normaliza os nomes (capitalização adequada);
      - Converte a data de lançamento para o formato ISO 8601;
      - Separa múltiplos gêneros em uma lista;
      - Calcula quantos dias, meses e anos se passaram desde o lançamento;
      - Extrai o identificador único imdbID da API.
      
    Parâmetros:
      - dados_brutos: Dicionário com os dados do filme conforme obtidos da API.
      
    Retorna:
      - Um dicionário com os dados transformados.
    """
    try:
        # Extrai o imdbID retornado pela API
        imdb_id = dados_brutos.get("imdbID", None)
        
        # Normalização dos nomes: título e diretor com capitalização adequada
        titulo = dados_brutos.get("Title", "").title()
        diretor = dados_brutos.get("Director", "").title()
        ano_lancamento = dados_brutos.get("Year", "")
        
        # Conversão da data de lançamento para o formato ISO 8601
        released_str = dados_brutos.get("Released", "")
        try:
            data_lancamento = datetime.datetime.strptime(released_str, "%d %b %Y").date()
            iso_release_date = data_lancamento.isoformat()
        except Exception:
            logging.error(f"Erro ao converter a data '{released_str}'.")
            data_lancamento = None
            iso_release_date = None

        # Cálculo do tempo decorrido desde o lançamento
        dias_desde_lancamento = meses_desde_lancamento = anos_desde_lancamento = None
        if data_lancamento:
            hoje = datetime.date.today()
            delta = relativedelta(hoje, data_lancamento)
            dias_desde_lancamento = (hoje - data_lancamento).days
            meses_desde_lancamento = delta.years * 12 + delta.months
            anos_desde_lancamento = delta.years

        # Extração e normalização da sinopse (Plot)
        sinopse = dados_brutos.get("Plot", "")

        # Separação dos gêneros (o campo "Genre" vem como uma string separada por vírgulas)
        generos_str = dados_brutos.get("Genre", "")
        generos = [genero.strip().title() for genero in generos_str.split(",") if genero.strip()]
        
        dados_transformados = {
            "imdb_id": imdb_id,  # Identificador único do filme
            "titulo": titulo,
            "ano_lancamento": ano_lancamento,
            "iso_release_date": iso_release_date,
            "dias_desde_lancamento": dias_desde_lancamento,
            "meses_desde_lancamento": meses_desde_lancamento,
            "anos_desde_lancamento": anos_desde_lancamento,
            "diretor": diretor,
            "sinopse": sinopse,
            "generos": generos
        }
        
        logging.info(f"Dados transformados para o filme: {titulo}")
        return dados_transformados

    except Exception as e:
        logging.exception("Erro na transformação dos dados do filme.")
        return None
