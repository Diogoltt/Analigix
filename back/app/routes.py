from app import app
from flask import jsonify, request 
import sqlite3
import pandas as pd
import os

def construir_clausula_where(filtros):
    where_conditions = []
    params = []


    mapa_filtros = {
        'uf': 'estado',
        'categoria': 'categoria_padronizada'
    }

    for chave, valor in filtros.items():
        if chave != 'ano' and valor:
            nome_coluna = mapa_filtros.get(chave)
            if nome_coluna:
                where_conditions.append(f"{nome_coluna} = ?")
                params.append(valor.upper() if chave == 'uf' else valor)

    ano_filter = filtros.get('ano')
    if ano_filter:
        where_conditions.append("strftime('%Y', data) = ?")
        params.append(str(ano_filter))
        
    if not where_conditions:
        return "", []

    return " WHERE " + " AND ".join(where_conditions), params



@app.route('/api/analise', methods=['GET'])
def get_analysis():
    try:
        filtros = {'uf': request.args.get('uf'), 'ano': request.args.get('ano')}
        string_where, params = construir_clausula_where(filtros)
        
        final_params = ["Outros"] + params
        final_where = " WHERE categoria_padronizada != ?"
        if string_where:
            final_where += " AND " + string_where.replace("WHERE", "").strip()

        query = f"SELECT categoria_padronizada, SUM(valor) as total_gasto FROM despesas{final_where} GROUP BY categoria_padronizada ORDER BY total_gasto DESC LIMIT 2"
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn, params=tuple(final_params))
        conn.close()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        print(f"Ocorreu um erro na rota /api/analise: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/estatisticas/total', methods=['GET'])
def get_total_investimento():
    try:
        filtros = {'uf': request.args.get('uf'), 'ano': request.args.get('ano')}
        string_where, params = construir_clausula_where(filtros)
        
        query = f"SELECT SUM(valor) as valor_total FROM despesas{string_where}"
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn, params=tuple(params))
        conn.close()
        total_value = df['valor_total'].iloc[0]
        return jsonify({"valor_total": float(total_value or 0)})
    except Exception as e:
        print(f"Ocorreu um erro na rota /api/estatisticas/total: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ranking', methods=['GET'])
def get_ranking_data():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        filtros = {'uf': request.args.get('uf'), 'ano': request.args.get('ano')}
        string_where, params = construir_clausula_where(filtros)

        final_params = ["Outros"] + params
        final_where = " WHERE categoria_padronizada != ?"
        if string_where:
            final_where += " AND " + string_where.replace("WHERE", "").strip()
        
        base_query = f"SELECT categoria_padronizada, SUM(valor) as total_gasto FROM despesas{final_where} GROUP BY categoria_padronizada"
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        
        count_query = f"SELECT COUNT(*) FROM ({base_query})"
        total_items = pd.read_sql_query(count_query, conn, params=tuple(final_params)).iloc[0,0]

        paginated_query = base_query + f" ORDER BY total_gasto DESC LIMIT {per_page} OFFSET {(page - 1) * per_page}"
        df = pd.read_sql_query(paginated_query, conn, params=tuple(final_params))
        conn.close()
        
        return jsonify({'total_registros': int(total_items), 'pagina_atual': page, 'dados': df.to_dict(orient='records')})
    except Exception as e:
        print(f"Ocorreu um erro na rota /api/ranking: {e}")
        return jsonify({"error": str(e)})

@app.route('/api/comparativo-geral', methods=['GET'])
def get_comparativo_geral():
    try:
        filtros = {'categoria': request.args.get('categoria'), 'ano': request.args.get('ano')}
        string_where, params = construir_clausula_where(filtros)

        query = f"SELECT estado, SUM(valor) AS total_investido FROM despesas{string_where} GROUP BY estado ORDER BY total_investido DESC"
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        print(f"Ocorreu um erro na rota /api/comparativo-geral: {e}")
        return jsonify({"error": str(e)})

@app.route('/api/ranking-nacional', methods=['GET'])
def get_ranking_nacional():
    try:
        filtros = {'ano': request.args.get('ano')}
        string_where, params = construir_clausula_where(filtros)

    
        query = f"SELECT estado, SUM(valor) AS total_investido FROM despesas{string_where} GROUP BY estado ORDER BY total_investido DESC LIMIT 5"
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
    
        return jsonify(df.to_dict(orient='records'))

    except Exception as e:
        print(f"Ocorreu um erro na rota /api/ranking-nacional: {e}")
        return jsonify({"error": str(e)})


@app.route('/api/dados', methods=['GET'])
def get_dados_paginados():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        filtros = {'uf': request.args.get('uf'),'ano': request.args.get('ano')}
        string_where, params = construir_clausula_where(filtros)

        base_query = f"SELECT * FROM despesas{string_where}"
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        
        count_query = base_query.replace("SELECT *", "SELECT COUNT(*)")
        total_rows = pd.read_sql_query(count_query, conn, params=tuple(params)).iloc[0,0]
        
        final_query = base_query + f" ORDER BY valor DESC LIMIT {per_page} OFFSET {(page - 1) * per_page}"
        df = pd.read_sql_query(final_query, conn, params=tuple(params))
        conn.close()
        
        return jsonify({
            'total_registros': int(total_rows), 'pagina_atual': page, 'dados': df.to_dict(orient='records')
        })
    except Exception as e:
        print(f"Ocorreu um erro na rota /api/dados: {e}")
        return jsonify({"error": str(e)})
    
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Obter dados do formulário
        estado = request.form.get('estado')
        ano = request.form.get('ano')
        arquivo = request.files.get('file')

        # Validar se todos os campos foram preenchidos
        if not estado or not ano:
            return jsonify({'erro': 'Estado e ano são obrigatórios.'}), 400

        if not arquivo:
            return jsonify({'erro': 'Nenhum arquivo enviado.'}), 400

        # Verificar se é um arquivo CSV
        if not arquivo.filename.lower().endswith('.csv'):
            return jsonify({'erro': 'Apenas arquivos CSV são aceitos.'}), 400

        # Definir o caminho da pasta csvs
        basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        upload_folder = os.path.join(basedir, 'csvs')
        
        # Criar a pasta se não existir
        os.makedirs(upload_folder, exist_ok=True)

        # Criar o nome do arquivo no formato SIGLAESTADO_ANO.csv
        nome_arquivo = f"{estado.upper()}_{ano}.csv"
        caminho_arquivo = os.path.join(upload_folder, nome_arquivo)

        # Salvar o arquivo
        arquivo.save(caminho_arquivo)

        return jsonify({
            'mensagem': 'Arquivo enviado com sucesso!',
            'arquivo': nome_arquivo,
            'caminho': caminho_arquivo
        }), 200

    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500