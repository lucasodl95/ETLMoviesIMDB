import sqlite3
import logging

def criar_tabelas(conn):
    """
    Cria as tabelas necessárias no banco de dados:
      - Filmes
      - Generos
      - Filme_Genero (tabela de associação)
      
    Parâmetro:
      - conn: Conexão com o banco de dados.
    """
    try:
        cursor = conn.cursor()
        # Tabela de Filmes com restrição UNIQUE no campo imdb_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Filmes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imdb_id TEXT UNIQUE,
                titulo TEXT,
                ano_lancamento TEXT,
                iso_release_date TEXT,
                dias_desde_lancamento INTEGER,
                meses_desde_lancamento INTEGER,
                anos_desde_lancamento INTEGER,
                diretor TEXT,
                sinopse TEXT
            )
        ''')
        # Tabela de Gêneros com restrição UNIQUE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Generos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_genero TEXT UNIQUE
            )
        ''')
        # Tabela de associação Filme_Genero
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Filme_Genero (
                filme_id INTEGER,
                genero_id INTEGER,
                FOREIGN KEY(filme_id) REFERENCES Filmes(id),
                FOREIGN KEY(genero_id) REFERENCES Generos(id),
                UNIQUE(filme_id, genero_id)
            )
        ''')
        conn.commit()
        logging.info("Tabelas criadas com sucesso no banco de dados.")
    except Exception as e:
        logging.exception("Erro ao criar as tabelas no banco de dados.")

def carregar_dados_no_banco(conn, dados_filme):
    """
    Insere os dados transformados no banco de dados, garantindo a integridade referencial.
    
    Parâmetros:
      - conn: Conexão com o banco de dados.
      - dados_filme: Dicionário com os dados do filme transformados.
    """
    try:
        cursor = conn.cursor()
        
        # Insere o filme utilizando INSERT OR IGNORE para evitar duplicidades
        cursor.execute('''
            INSERT OR IGNORE INTO Filmes (
                imdb_id, titulo, ano_lancamento, iso_release_date, dias_desde_lancamento,
                meses_desde_lancamento, anos_desde_lancamento, diretor, sinopse
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dados_filme["imdb_id"],
            dados_filme["titulo"],
            dados_filme["ano_lancamento"],
            dados_filme["iso_release_date"],
            dados_filme["dias_desde_lancamento"],
            dados_filme["meses_desde_lancamento"],
            dados_filme["anos_desde_lancamento"],
            dados_filme["diretor"],
            dados_filme["sinopse"]
        ))
        
        # Recupera o id do filme (seja recém inserido ou já existente)
        cursor.execute("SELECT id FROM Filmes WHERE imdb_id = ?", (dados_filme["imdb_id"],))
        filme_row = cursor.fetchone()
        if filme_row:
            filme_id = filme_row[0]
            logging.info(f"Filme '{dados_filme['titulo']}' com imdb_id {dados_filme['imdb_id']} possui o ID {filme_id}.")
        else:
            logging.error("Não foi possível recuperar o ID do filme.")
            conn.rollback()
            return

        # Inserção dos gêneros e da associação com o filme
        for genero in dados_filme["generos"]:
            # Verifica se o gênero já existe na tabela Generos
            cursor.execute("SELECT id FROM Generos WHERE nome_genero = ?", (genero,))
            resultado = cursor.fetchone()
            if resultado:
                genero_id = resultado[0]
            else:
                cursor.execute("INSERT OR IGNORE INTO Generos (nome_genero) VALUES (?)", (genero,))
                genero_id = cursor.lastrowid
            
            # Insere a associação na tabela Filme_Genero utilizando INSERT OR IGNORE
            cursor.execute("INSERT OR IGNORE INTO Filme_Genero (filme_id, genero_id) VALUES (?, ?)", (filme_id, genero_id))
        
        conn.commit()
        logging.info("Dados carregados com sucesso no banco de dados.")
    except Exception as e:
        logging.exception("Erro ao carregar os dados no banco de dados.")
        conn.rollback()
