from app import app
from flask import jsonify, request 
import sqlite3
import pandas as pd
@app.route('/api/analise', methods=['GET'])
def get_analysis():
    try:
        uf_filter = request.args.get('uf')
        ano_filter = request.args.get('ano', type=int)
        
        base_query = "SELECT categoria_padronizada, SUM(valor) as total_gasto FROM despesas"
        where_conditions = ["categoria_padronizada != ?"]
        params = ["Outros"]
        
        if uf_filter:
            where_conditions.append("estado = ?") 
            params.append(uf_filter.upper())
        
        if ano_filter:
            where_conditions.append("ano = ?")
            params.append(ano_filter)
            
        base_query += " WHERE " + " AND ".join(where_conditions)
        final_query = base_query + " GROUP BY categoria_padronizada ORDER BY total_gasto DESC LIMIT 2"
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(final_query, conn, params=tuple(params))
        conn.close()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        print(f"Ocorreu um erro na rota /api/analise: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/estatisticas/total', methods=['GET'])
def get_total_investimento():
    try:
        uf_filter = request.args.get('uf')
        ano_filter = request.args.get('ano', type=int)
        
        base_query = "SELECT SUM(valor) as valor_total FROM despesas"
        where_conditions, params = [], []
        
        if uf_filter:
            where_conditions.append("estado = ?")
            params.append(uf_filter.upper())
        
        if ano_filter:
            where_conditions.append("ano = ?")
            params.append(ano_filter)
            
        if where_conditions:
            base_query += " WHERE " + " AND ".join(where_conditions)

        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(base_query, conn, params=tuple(params))
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
        uf_filter = request.args.get('uf')
        ano_filter = request.args.get('ano', type=int)
        
        base_query = "SELECT categoria_padronizada, SUM(valor) as total_gasto FROM despesas"
        where_conditions = ["categoria_padronizada != ?"]
        params = ["Outros"]

        if uf_filter:
            where_conditions.append("estado = ?")
            params.append(uf_filter.upper())
        
        if ano_filter:
            where_conditions.append("ano = ?")
            params.append(ano_filter)
            
        base_query += " WHERE " + " AND ".join(where_conditions)
        final_query = base_query + " GROUP BY categoria_padronizada ORDER BY total_gasto DESC"
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        
        
        full_df = pd.read_sql_query(final_query, conn, params=tuple(params))
        conn.close()

        
        offset = (page - 1) * per_page
        paginated_df = full_df.iloc[offset : offset + per_page]

        
        total_items = len(full_df)
        
        
        return jsonify({
            'total_registros': total_items,
            'pagina_atual': page,
            'dados': paginated_df.to_dict(orient='records')
        })

    except Exception as e:
        print(f"Ocorreu um erro na rota /api/ranking: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/dados', methods=['GET'])
def get_dados_paginados():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        uf_filter = request.args.get('uf')
        ano_filter = request.args.get('ano', type=int)
        offset = (page - 1) * per_page

        base_query = "SELECT * FROM despesas"
        where_conditions, params = [], []

        if uf_filter:
            where_conditions.append("estado = ?")
            params.append(uf_filter.upper())
        
        if ano_filter:
            where_conditions.append("ano = ?")
            params.append(ano_filter)
            
        if where_conditions:
            base_query += " WHERE " + " AND ".join(where_conditions)
        
        count_query = base_query.replace("SELECT *", "SELECT COUNT(*)")
        final_query = base_query + f" ORDER BY valor DESC LIMIT {per_page} OFFSET {offset}"

        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(final_query, conn, params=tuple(params))
        total_rows = pd.read_sql_query(count_query, conn, params=tuple(params)).iloc[0,0]
        conn.close()
        
        return jsonify({
            'total_registros': int(total_rows),
            'pagina_atual': page,
            'dados': df.to_dict(orient='records')
        })
    except Exception as e:
        print(f"Ocorreu um erro na rota /api/dados: {e}")
        return jsonify({"error": str(e)}), 500