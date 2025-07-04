from flask_restx import Api, Resource, fields, Namespace
from flask import request, jsonify
import sqlite3
import pandas as pd

def init_swagger(app):
    """
    Inicializa a documentação Swagger para a API Analigix
    """
    api = Api(
        app,
        version='1.0',
        title='Analigix API',
        description='API para análise de despesas públicas brasileiras',
        doc='/docs/',
        prefix='/api'
    )

    # Namespace para análises
    analise_ns = Namespace('analise', description='Operações de análise de dados')
    ranking_ns = Namespace('ranking', description='Operações de ranking e comparação')
    dados_ns = Namespace('dados', description='Operações de dados brutos')
    upload_ns = Namespace('upload', description='Upload de arquivos CSV')
    
    api.add_namespace(analise_ns)
    api.add_namespace(ranking_ns)
    api.add_namespace(dados_ns)
    api.add_namespace(upload_ns)

    # Models para documentação
    analise_model = api.model('Analise', {
        'categoria_padronizada': fields.String(description='Nome da categoria'),
        'total_gasto': fields.Float(description='Valor total gasto em reais')
    })

    ranking_model = api.model('Ranking', {
        'estado': fields.String(description='Sigla do estado'),
        'total_investido': fields.Float(description='Total investido em reais')
    })

    despesas_estado_model = api.model('DespesasEstado', {
        'categoria': fields.String(description='Categoria da despesa'),
        'valor': fields.Float(description='Valor da despesa em reais')
    })

    insight_model = api.model('Insight', {
        'insight': fields.String(description='Texto do insight gerado por IA'),
        'dados_comparacao': fields.Raw(description='Dados estatísticos da comparação')
    })

    error_model = api.model('Error', {
        'error': fields.String(description='Mensagem de erro')
    })

    # Rotas documentadas
    @analise_ns.route('')
    @analise_ns.doc('get_analise')
    class AnaliseResource(Resource):
        @analise_ns.doc('analise_gastos')
        @analise_ns.param('uf', 'Sigla do estado (opcional)', type='string')
        @analise_ns.param('ano', 'Ano de análise (opcional)', type='integer')
        @analise_ns.marshal_list_with(analise_model)
        @analise_ns.response(500, 'Erro interno', error_model)
        def get(self):
            """Retorna as top 2 categorias de maior gasto (exceto 'Outros')"""
            from app.routes import get_analysis
            return get_analysis()

    @ranking_ns.route('/nacional')
    @ranking_ns.doc('ranking_nacional')
    class RankingNacionalResource(Resource):
        @ranking_ns.doc('ranking_estados')
        @ranking_ns.param('ano', 'Ano de análise', type='integer')
        @ranking_ns.marshal_list_with(ranking_model)
        @ranking_ns.response(500, 'Erro interno', error_model)
        def get(self):
            """Retorna ranking dos 5 estados que mais investiram"""
            from app.routes import get_ranking_nacional
            return get_ranking_nacional()

    @analise_ns.route('/despesas-estado/<string:estado>/<int:ano>')
    @analise_ns.doc('despesas_estado_ano')
    class DespesasEstadoAnoResource(Resource):
        @analise_ns.doc('despesas_por_categoria')
        @analise_ns.param('estado', 'Sigla do estado', required=True)
        @analise_ns.param('ano', 'Ano de consulta', required=True)
        @analise_ns.marshal_list_with(despesas_estado_model)
        @analise_ns.response(500, 'Erro interno', error_model)
        def get(self, estado, ano):
            """Retorna despesas de um estado específico por categoria em um ano"""
            from app.routes import get_despesas_estado_ano
            return get_despesas_estado_ano(estado, ano)

    @analise_ns.route('/categorias')
    @analise_ns.doc('categorias')
    class CategoriasResource(Resource):
        @analise_ns.doc('listar_categorias')
        @analise_ns.response(200, 'Lista de categorias', fields.List(fields.String))
        @analise_ns.response(500, 'Erro interno', error_model)
        def get(self):
            """Retorna todas as categorias disponíveis no sistema"""
            from app.routes import get_categorias
            return get_categorias()

    @analise_ns.route('/insight-comparacao')
    @analise_ns.doc('insight_comparacao')
    class InsightComparacaoResource(Resource):
        @analise_ns.doc('gerar_insight')
        @analise_ns.param('ufA', 'Sigla do primeiro estado', required=True)
        @analise_ns.param('ufB', 'Sigla do segundo estado', required=True)
        @analise_ns.param('ano', 'Ano de análise', type='integer', default=2024)
        @analise_ns.param('categorias', 'Categorias separadas por vírgula (opcional)')
        @analise_ns.marshal_with(insight_model)
        @analise_ns.response(400, 'Parâmetros inválidos', error_model)
        @analise_ns.response(500, 'Erro interno', error_model)
        def get(self):
            """Gera insight comparativo entre dois estados usando IA"""
            from app.routes import get_insight_comparacao
            return get_insight_comparacao()

    @dados_ns.route('')
    @dados_ns.doc('dados_paginados')
    class DadosResource(Resource):
        @dados_ns.doc('listar_dados')
        @dados_ns.param('page', 'Número da página', type='integer', default=1)
        @dados_ns.param('per_page', 'Itens por página', type='integer', default=100)
        @dados_ns.param('uf', 'Sigla do estado (opcional)')
        @dados_ns.param('ano', 'Ano de consulta (opcional)', type='integer')
        def get(self):
            """Retorna dados paginados com filtros opcionais"""
            from app.routes import get_dados_paginados
            return get_dados_paginados()

    @ranking_ns.route('/comparativo-geral')
    @ranking_ns.doc('comparativo_geral')
    class ComparativoGeralResource(Resource):
        @ranking_ns.doc('comparacao_estados')
        @ranking_ns.param('categoria', 'Categoria específica (opcional)')
        @ranking_ns.param('ano', 'Ano de análise (opcional)', type='integer')
        @ranking_ns.marshal_list_with(ranking_model)
        def get(self):
            """Retorna comparativo de investimento entre todos os estados"""
            from app.routes import get_comparativo_geral
            return get_comparativo_geral()

    return api
