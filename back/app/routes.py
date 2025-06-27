# Arquivo: back/app/routes.py (VERSÃO FINAL E TOTALMENTE REATORADA)

from app import app
from flask import jsonify, request 
import sqlite3
import pandas as pd

# ==============================================================================
# FUNÇÃO AJUDANTE (HELPER) PARA CONSTRUIR A CLÁUSULA WHERE
# Centraliza toda a lógica de filtros para todas as rotas.
# ==============================================================================
def construir_clausula_where(filtros):
    """
    Constrói a string da cláusula WHERE e a lista de parâmetros com base nos filtros.
    Filtros é um dicionário, ex: {'uf': 'SP', 'ano': 2024}
    """
    where_conditions = []
    params = []

    # Mapeia os filtros da URL para as colunas reais do banco de dados
    mapa_filtros = {
        'uf': 'estado',
        'ano': 'ano',
        'categoria': 'categoria_padronizada'
    }

    for chave, valor in filtros.items():
        if valor: # Apenas adiciona o filtro se ele tiver um valor
            nome_coluna = mapa_filtros.get(chave)
            if nome_coluna:
                where_conditions.append(f"{nome_coluna} = ?")
                # Converte para maiúsculas se for string (para UFs), senão usa o valor como está (para anos)
                params.append(valor.upper() if isinstance(valor, str) else valor)

    if not where_conditions:
        return "", []

    return " WHERE " + " AND ".join(where_conditions), params


# ==============================================================================
# NOSSAS ROTAS, AGORA TODAS USANDO O HELPER
# ==============================================================================

# ROTA 1: Para a análise do "Top 2" na tela nacional
@app.route('/api/analise', methods=['GET'])
def get_analysis():
    try:
        filtros = {'uf': request.args.get('uf'), 'ano': request.args.get('ano', type=int)}
        string_where, params = construir_clausula_where(filtros)
        
        # Constrói a cláusula WHERE completa, incluindo o filtro "Outros"
        if not string_where:
            final_where = " WHERE area_de_atuacao != ?"
            final_params = ["Outros"]
        else:
            final_where = string_where + " AND area_de_atuacao != ?"
            final_params = params + ["Outros"]

        query = f"""
            SELECT area_de_atuacao, SUM(valor_gasto) as total_gasto
            FROM Despesas_Estados
            {final_where}
            GROUP BY area_de_atuacao ORDER BY total_gasto DESC LIMIT 2
        """
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn, params=tuple(final_params))
        conn.close()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)})

# ROTA 2: Para o cálculo do VALOR TOTAL investido
@app.route('/api/estatisticas/total', methods=['GET'])
def get_total_investimento():
    try:
        filtros = {'uf': request.args.get('uf'), 'ano': request.args.get('ano', type=int)}
        string_where, params = construir_clausula_where(filtros)
        
        query = f"SELECT SUM(valor_gasto) as valor_total FROM Despesas_Estados {string_where}"

        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn, params=tuple(params))
        conn.close()
        total_value = df['valor_total'].iloc[0]
        return jsonify({"valor_total": float(total_value or 0)})
    except Exception as e:
        return jsonify({"error": str(e)})

# ROTA 3: Para alimentar o RANKING ESTADUAL (paginado)
@app.route('/api/ranking', methods=['GET'])
def get_ranking_data():
    try:
        filtros = {'uf': request.args.get('uf'), 'ano': request.args.get('ano', type=int)}
        string_where, params = construir_clausula_where(filtros)
        
        if not string_where:
            final_where = " WHERE area_de_atuacao != ?"
            final_params = ["Outros"]
        else:
            final_where = string_where + " AND area_de_atuacao != ?"
            final_params = params + ["Outros"]
        
        base_query = f"SELECT area_de_atuacao, SUM(valor_gasto) as total_gasto FROM Despesas_Estados {final_where} GROUP BY area_de_atuacao"
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        
        count_query = f"SELECT COUNT(*) FROM ({base_query})"
        total_items = pd.read_sql_query(count_query, conn, params=tuple(final_params)).iloc[0,0]

        paginated_query = base_query + f" ORDER BY total_gasto DESC LIMIT {request.args.get('per_page', 10, type=int)} OFFSET {(request.args.get('page', 1, type=int) - 1) * request.args.get('per_page', 10, type=int)}"
        df = pd.read_sql_query(paginated_query, conn, params=tuple(final_params))
        conn.close()
        
        return jsonify({
            'total_registros': int(total_items),
            'pagina_atual': request.args.get('page', 1, type=int),
            'dados': df.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({"error": str(e)})

# ROTA 4: Para o GRÁFICO DE BARRAS COMPARATIVO
@app.route('/api/comparativo-nacional', methods=['GET'])
def get_comparativo_nacional():
    try:
        filtros = {'categoria': request.args.get('categoria')}
        string_where, params = construir_clausula_where(filtros)

        if not string_where: # Precisa de uma categoria para funcionar
            return jsonify([])

        query = f"""
            SELECT uf, SUM(valor_gasto) AS total_investido
            FROM Despesas_Estados
            {string_where}
            GROUP BY uf ORDER BY total_investido DESC
        """
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)})

# ROTA 5: Para o RANKING NACIONAL (Top 5 estados)
@app.route('/api/ranking-nacional', methods=['GET'])
def get_ranking_nacional():
    try:
        query = """
            SELECT uf AS estado, SUM(valor_gasto) AS total_investido
            FROM Despesas_Estados
            GROUP BY uf ORDER BY total_investido DESC LIMIT 5
        """
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)})

# ROTA 6: Para listar despesas individuais com paginação
@app.route('/api/dados', methods=['GET'])
def get_dados_paginados():
    try:
        filtros = {'uf': request.args.get('uf'),'ano': request.args.get('ano', type=int)}
        string_where, params = construir_clausula_where(filtros)

        base_query = f"SELECT * FROM Despesas_Estados {string_where}"
        count_query = base_query.replace("SELECT *", "SELECT COUNT(*)")
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        total_rows = pd.read_sql_query(count_query, conn, params=tuple(params)).iloc[0,0]
        
        paginated_query = base_query + f" ORDER BY valor_gasto DESC LIMIT {request.args.get('per_page', 100, type=int)} OFFSET {(request.args.get('page', 1, type=int) - 1) * request.args.get('per_page', 100, type=int)}"
        df = pd.read_sql_query(paginated_query, conn, params=tuple(params))
        conn.close()
        
        return jsonify({
            'total_registros': int(total_rows),
            'pagina_atual': request.args.get('page', 1, type=int),
            'dados': df.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({"error": str(e)})