# Pipeline ETL de Dados de Filmes

Este projeto implementa um pipeline ETL (Extract, Transform, Load) que extrai dados de filmes a partir da [OMDb API](https://www.omdbapi.com/), transforma e normaliza esses dados e, finalmente, os carrega em um banco de dados SQLite. O pipeline foi desenvolvido com foco em modularização, integridade dos dados e otimização através de processamento concorrente.

## Funcionalidades

- **Extração:**  
  Consulta a OMDb API para obter informações dos filmes. O módulo `src/extract.py` realiza a requisição HTTP e trata erros de comunicação e validação.

- **Transformação:**  
  O módulo `src/transform.py` processa os dados brutos, realizando as seguintes operações:
  - Normalização do título e nome do diretor.
  - Conversão da data de lançamento para o formato ISO 8601.
  - Cálculo do tempo decorrido (dias, meses e anos) desde o lançamento.
  - Separação dos gêneros em uma lista.
  - Extração do `imdbID`, que é usado como identificador único para evitar duplicidades.

- **Carga:**  
  O módulo `src/load.py` cria e gerencia as seguintes tabelas no SQLite:
  - **Filmes:** Armazena dados do filme (incluindo `imdb_id`, Título, Ano de Lançamento, datas, Diretor e Sinopse).
  - **Generos:** Armazena os gêneros dos filmes (com restrição `UNIQUE`).
  - **Filme_Genero:** Tabela associativa que relaciona filmes aos seus gêneros.
  
  Para evitar duplicidades, é utilizada a estratégia `INSERT OR IGNORE` combinada com restrições `UNIQUE` (baseadas no `imdbID` para filmes).

- **Otimização com Concorrência:**  
  O arquivo `main.py` utiliza o módulo `concurrent.futures` com 4 *workers* para paralelizar as etapas de extração e transformação, otimizando o tempo de execução.

## Estrutura do Projeto
```
.
├── db/                 # Pasta para o banco de dados SQLite (arquivo: filmes.db)
├── logs/               # Pasta para os logs do processo ETL (arquivo: etl.log)
├── src/
│   ├── extract.py      # Módulo de extração de dados da OMDb API
│   ├── transform.py    # Módulo de transformação dos dados extraídos
│   └── load.py         # Módulo de criação das tabelas e inserção dos dados
├── main.py             # Arquivo principal que orquestra o pipeline ETL
└── requirements.txt    # Lista de dependências do projeto
```

## Pré-Requisitos

- Python 3.13 
- Chave de API gratuita da [OMDb API](https://www.omdbapi.com/apikey.aspx)

## Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

**Observação:**
Se estiver utilizando Python 3, o módulo `concurrent.futures` já faz parte da biblioteca padrão. Se estiver utilizando Python 2 (não recomendado), adicione a dependência `futures` conforme especificado no `requirements.txt`.

## Configuração

- **API Key:**  
No arquivo `main.py`, substitua o valor da variável `API_KEY` pela sua chave de acesso da OMDb API.

- **Pastas:**  
O script verifica e cria automaticamente as pastas `db` e `logs` caso elas não existam. O banco de dados será criado em `db/filmes.db` e os logs serão gravados em `logs/etl.log`.

## Execução

Para rodar o pipeline ETL, execute:
```bash
python main.py
```
O pipeline extrai os dados de uma lista de filmes definida em `main.py`, processa-os e os insere no banco de dados. Caso o script seja executado novamente, os filmes já existentes (identificados pelo `imdbID`) não serão duplicados.

## Contribuições

Contribuições são bem-vindas! Se você deseja melhorar o projeto, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a MIT License.

