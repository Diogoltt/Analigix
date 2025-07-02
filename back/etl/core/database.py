"""
Gerenciador do banco de dados SQLite.
"""

import sqlite3
import os


def verificar_banco(nome_banco, nome_tabela):
    """
    Verifica se o banco existe e cria a tabela se necessário.
    """
    try:
        # Criar pasta se não existir
        database_dir = os.path.dirname(nome_banco)
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)
            print(f"📁 Pasta criada: {database_dir}")
        
        conn = sqlite3.connect(nome_banco)
        cursor = conn.cursor()
        
        # Verificar se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nome_tabela,))
        if not cursor.fetchone():
            print(f"⚠️  Tabela '{nome_tabela}' não existe. Criando automaticamente...")
            
            # Criar tabela
            sql_criar_tabela = """
            CREATE TABLE IF NOT EXISTS despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estado TEXT NOT NULL,
                data DATE,
                orgao TEXT,
                categoria_padronizada TEXT,
                valor REAL
            )
            """
            cursor.execute(sql_criar_tabela)
            conn.commit()
            print(f"✅ Tabela '{nome_tabela}' criada com sucesso!")
            
        # Mostrar estatísticas do banco
        cursor.execute(f"SELECT COUNT(*) FROM {nome_tabela}")
        total_registros = cursor.fetchone()[0]
        print(f"📊 Banco atual possui {total_registros} registros.")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao verificar/criar o banco: {e}")
        return False


def salvar_dados(dados_processados, nome_banco, nome_tabela):
    """
    Salva os dados processados no banco SQLite.
    """
    if not dados_processados:
        return 0
    
    try:
        import pandas as pd
        df_final = pd.DataFrame(dados_processados)
        
        conn = sqlite3.connect(nome_banco)
        df_final.to_sql(nome_tabela, conn, if_exists='append', index=False)
        conn.commit()
        conn.close()
        
        return len(df_final)
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")
        return 0
