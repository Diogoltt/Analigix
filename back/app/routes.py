from app import app
from flask import jsonify, request 
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

# Carregar variáveis de ambiente
load_dotenv()

# Configurar cliente OpenAI
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

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

# Em back/app/routes.py

@app.route('/api/detalhes-categoria', methods=['GET'])
def get_detalhes_categoria():
    """
    Para uma dada categoria e UF, retorna a lista de despesas AGRUPADA por órgão,
    com os valores SOMADOS.
    """
    try:
        # Pega os filtros da URL
        uf_filter = request.args.get('uf')
        categoria_filter = request.args.get('categoria')
        ano_filter = request.args.get('ano') # Pega o ano como string

        # Validação: uf e categoria são obrigatórios para esta consulta
        if not uf_filter or not categoria_filter:
            return jsonify({"error": "UF e Categoria são parâmetros obrigatórios."}), 400

        # Usa o helper para construir a cláusula WHERE
        filtros = {
            'uf': uf_filter,
            'ano': ano_filter,
            'categoria': categoria_filter
        }
        string_where, params = construir_clausula_where(filtros)

        # ===================================================================
        # A MUDANÇA ESTÁ AQUI: A nova query com GROUP BY e SUM
        # ===================================================================
        query = f"""
            SELECT
                orgao,
                SUM(valor) AS total_por_orgao
            FROM
                despesas
            {string_where}
            GROUP BY
                orgao
            ORDER BY
                total_por_orgao DESC
        """
        
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn, params=tuple(params))
        conn.close()
        
        # A API agora envia uma lista já sumarizada e sem duplicatas
        return jsonify(df.to_dict(orient='records'))

    except Exception as e:
        print(f"Ocorreu um erro na rota /api/detalhes-categoria: {e}")
        return jsonify({"error": str(e)}), 500
    
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

        # Validar ano
        try:
            ano_int = int(ano)
            if ano_int < 2020 or ano_int > 2025:
                return jsonify({'erro': 'Ano deve estar entre 2020 e 2025.'}), 400
        except ValueError:
            return jsonify({'erro': 'Ano deve ser um número válido.'}), 400

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

        # Processar o arquivo automaticamente com ETL
        try:
            import sys
            etl_path = os.path.join(basedir, 'etl')
            if etl_path not in sys.path:
                sys.path.append(etl_path)
            
            from etl.run_etl import processar_novo_arquivo
            
            print(f"🚀 Iniciando processamento ETL para {estado.upper()}_{ano}.csv")
            sucesso_etl = processar_novo_arquivo(estado.upper(), ano_int)
            
            if sucesso_etl:
                # Deletar o arquivo CSV após processamento bem-sucedido
                try:
                    os.remove(caminho_arquivo)
                    print(f"🗑️ Arquivo {nome_arquivo} deletado após processamento bem-sucedido")
                    arquivo_deletado = True
                except Exception as delete_error:
                    print(f"⚠️ Erro ao deletar arquivo {nome_arquivo}: {delete_error}")
                    arquivo_deletado = False
                
                return jsonify({
                    'mensagem': 'Arquivo enviado, processado com sucesso e removido!',
                    'arquivo': nome_arquivo,
                    'etl_processado': True,
                    'arquivo_deletado': arquivo_deletado
                }), 200
            else:
                return jsonify({
                    'mensagem': 'Arquivo enviado, mas houve erro no processamento ETL.',
                    'arquivo': nome_arquivo,
                    'caminho': caminho_arquivo,
                    'etl_processado': False,
                    'aviso': 'Os dados podem não estar disponíveis no dashboard. Arquivo mantido para depuração.'
                }), 200
                
        except Exception as etl_error:
            print(f"❌ Erro no processamento ETL: {etl_error}")
            return jsonify({
                'mensagem': 'Arquivo enviado, mas houve erro no processamento ETL.',
                'arquivo': nome_arquivo,
                'caminho': caminho_arquivo,
                'etl_processado': False,
                'erro_etl': str(etl_error),
                'aviso': 'Os dados podem não estar disponíveis no dashboard.'
            }), 200

    except Exception as e:
        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/api/insight-comparacao', methods=['GET'])
def get_insight_comparacao():
    try:
        uf_a = request.args.get('ufA')
        uf_b = request.args.get('ufB')
        ano = request.args.get('ano', 2024)
        categorias = request.args.get('categorias', '').split(',') if request.args.get('categorias') else []
        
        if not uf_a or not uf_b:
            return jsonify({'erro': 'UFs são obrigatórias'}), 400
            
        db_path = app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        
        # Se categorias específicas foram fornecidas, filtrar por elas
        categoria_filter = ""
        if categorias and categorias[0]:  # Verifica se há categorias e não está vazio
            categoria_placeholders = ','.join(['?' for _ in categorias])
            categoria_filter = f" AND categoria_padronizada IN ({categoria_placeholders})"
        
        # Query para buscar dados dos dois estados
        query = f"""
        SELECT 
            estado,
            categoria_padronizada,
            SUM(valor) as total_gasto,
            COUNT(*) as num_despesas,
            AVG(valor) as gasto_medio
        FROM despesas 
        WHERE estado IN (?, ?) 
        AND strftime('%Y', data) = ?
        AND categoria_padronizada != 'Outros'
        {categoria_filter}
        GROUP BY estado, categoria_padronizada
        ORDER BY estado, total_gasto DESC
        """
        
        params = [uf_a.upper(), uf_b.upper(), str(ano)]
        if categorias and categorias[0]:
            params.extend(categorias)
            
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        if df.empty:
            return jsonify({
                'insight': f'Não foram encontrados dados suficientes para comparar {uf_a} e {uf_b} no ano de {ano}.'
            })
        
        # Análise dos dados
        dados_a = df[df['estado'] == uf_a.upper()]
        dados_b = df[df['estado'] == uf_b.upper()]
        
        total_a = dados_a['total_gasto'].sum()
        total_b = dados_b['total_gasto'].sum()
        
        # Categoria com maior investimento em cada estado
        top_categoria_a = dados_a.iloc[0] if len(dados_a) > 0 else None
        top_categoria_b = dados_b.iloc[0] if len(dados_b) > 0 else None
        
        # Análise de diversificação
        num_categorias_a = len(dados_a)
        num_categorias_b = len(dados_b)
        
        # Gerar insight usando GPT-4
        try:
            # Preparar dados para o prompt
            categorias_texto = ', '.join(categorias) if categorias and categorias[0] else 'todas as categorias'
            
            # Formatar valores para o prompt
            total_a_formatado = f"R$ {total_a:,.2f}".replace(',', '.')
            total_b_formatado = f"R$ {total_b:,.2f}".replace(',', '.')
            
            # Criar prompt estruturado para GPT-4
            prompt = f"""
Você é um analista especialista em políticas públicas e orçamento governamental brasileiro. 

Analise os dados de investimento público de {ano} e gere um insight profissional e objetivo sobre a comparação entre os estados.

DADOS DA COMPARAÇÃO:
- Estado A: {uf_a}
- Estado B: {uf_b}
- Ano: {ano}
- Categorias analisadas: {categorias_texto}

VALORES INVESTIDOS:
- {uf_a}: {total_a_formatado} (em {num_categorias_a} categorias)
- {uf_b}: {total_b_formatado} (em {num_categorias_b} categorias)

PRINCIPAIS FOCOS:
- Principal categoria {uf_a}: {top_categoria_a['categoria_padronizada'] if top_categoria_a is not None else 'N/A'}
- Principal categoria {uf_b}: {top_categoria_b['categoria_padronizada'] if top_categoria_b is not None else 'N/A'}

INSTRUÇÕES:
1. Gere um insight de 2-3 frases, máximo 150 palavras
2. Seja específico com percentuais e valores quando relevante
3. Mencione diferenças estratégicas entre os estados
4. Use linguagem técnica mas acessível
5. Foque nas categorias que estão sendo visualizadas no gráfico
6. Não use bullet points, apenas texto corrido

Insight:"""

            # Fazer chamada para GPT-4
            print(f"🤖 Tentando gerar insight com GPT-4 para {uf_a} vs {uf_b}...")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "Você é um analista experiente em políticas públicas brasileiras, especializado em análise orçamentária e comparações interestaduais. Suas análises são sempre objetivas, baseadas em dados e contextualmente relevantes."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            insight_final = response.choices[0].message.content.strip()
            print(f"✅ Insight gerado com sucesso pela IA: {insight_final[:50]}...")
            
        except Exception as e:
            print(f"❌ Erro ao gerar insight com GPT-4: {str(e)}")
            print(f"🔄 Usando fallback baseado em dados...")
            # Fallback para análise baseada em dados se GPT-4 falhar
            insight_parts = []
            
            if total_a > total_b:
                diferenca_pct = ((total_a - total_b) / total_b) * 100
                insight_parts.append(f"{uf_a} investiu {diferenca_pct:.1f}% mais que {uf_b} nas categorias analisadas.")
            elif total_b > total_a:
                diferenca_pct = ((total_b - total_a) / total_a) * 100
                insight_parts.append(f"{uf_b} investiu {diferenca_pct:.1f}% mais que {uf_a} nas categorias analisadas.")
            else:
                insight_parts.append(f"{uf_a} e {uf_b} tiveram investimentos similares nas categorias analisadas.")
            
            if top_categoria_a is not None and top_categoria_b is not None:
                if top_categoria_a['categoria_padronizada'] == top_categoria_b['categoria_padronizada']:
                    insight_parts.append(f"Ambos os estados priorizaram '{top_categoria_a['categoria_padronizada']}' como principal área de investimento.")
                else:
                    insight_parts.append(f"{uf_a} focou principalmente em '{top_categoria_a['categoria_padronizada']}', enquanto {uf_b} priorizou '{top_categoria_b['categoria_padronizada']}'.")
            
            insight_final = " ".join(insight_parts)
        
        return jsonify({
            'insight': insight_final,
            'dados_comparacao': {
                'total_a': float(total_a),
                'total_b': float(total_b),
                'categorias_a': num_categorias_a,
                'categorias_b': num_categorias_b,
                'top_categoria_a': top_categoria_a['categoria_padronizada'] if top_categoria_a is not None else None,
                'top_categoria_b': top_categoria_b['categoria_padronizada'] if top_categoria_b is not None else None
            }
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao gerar insight: {str(e)}'}), 500