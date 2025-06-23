# Arquivo: back/verificar_db.py (VERSÃO PARA VER COLUNAS)
import sqlite3
import os

# O nome da sua tabela que descobrimos que é 'despesas'
NOME_DA_TABELA = 'despesas'

db_path = os.path.join('database', 'despesas_brasil.db')

print(f"Analisando as colunas da tabela '{NOME_DA_TABELA}' em: {os.path.abspath(db_path)}\n")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Esta consulta especial pede ao SQLite para descrever as colunas da tabela
    cursor.execute(f"PRAGMA table_info({NOME_DA_TABELA});")

    columns = cursor.fetchall()
    conn.close()

    if not columns:
        print(f"ERRO: A tabela '{NOME_DA_TABELA}' parece estar vazia ou não foi encontrada.")
    else:
        print("Sucesso! Estas são as colunas encontradas:")
        print("---------------------------------------")
        for col in columns:
            # O nome da coluna é o segundo item da lista (índice 1)
            print(f"- Nome da coluna: {col[1]}, Tipo: {col[2]}")
        print("---------------------------------------")

except Exception as e:
    print(f"\nFALHA AO CONECTAR: {e}")