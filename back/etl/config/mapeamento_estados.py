"""
Configuração de mapeamento de colunas para cada estado.
"""

MAPEAMENTO_COLUNAS = {
    'AC': {  
        'arquivo': '../csvs/*AC*.csv',
        'colunas': {
            'orgao': 'descricao',
            'valor_pago': 'pago',
            'valor_empenhado': 'empenhado',
            'ano': None,
            'estado': 'AC'
        }
    },
    'AL': {  
        'arquivo': '../csvs/*AL*.csv',
        'colunas': {
            'orgao': 'orgao_descricao',
            'valor_pago': 'total_pago',
            'valor_empenhado': 'total_empenhado',
            'ano': 'data_final',
            'estado': 'AL'
        }
    },
    'AP': {  
        'arquivo': '../csvs/*AP*.csv',
        'colunas': {
            'orgao': 'NOME_UNIDADE_GESTORA',
            'valor_pago': 'VAL_PAGO',
            'valor_empenhado': 'VAL_EMPENHADO',
            'ano': 'ANO',
            'estado': 'AP'
        }
    },
    'AM': {  
        'arquivo': '../csvs/*AM*.csv',
        'colunas': {
            'orgao': 'Função',  
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': None,
            'estado': 'AM'
        }
    },
    'BA': {  
        'arquivo': '../csvs/*BA*.csv',
        'colunas': {
            'orgao': 'Órgão',
            'valor_pago': 'Valor Pago',
            'valor_empenhado': 'Valor Empenhado',
            'ano': 'Ano',
            'estado': 'BA'
        }
    },
    'CE': {  
        'arquivo': '../csvs/*CE*.csv',
        'colunas': {
            'orgao': 'Unidade gestora',
            'valor_pago': 'Valor pago final',
            'valor_empenhado': 'Valor empenhado final',
            'ano': 'Exercício',
            'estado': 'CE'
        }
    },
    'DF': {  
        'arquivo': '../csvs/*DF*.csv',
        'colunas': {
            'orgao': 'Unidade Gestora',
            'valor_pago': 'Valor Final',
            'valor_empenhado': None,  
            'ano': None,
            'estado': 'DF'
        }
    },
    'ES': {  
        'arquivo': '../csvs/*ES*.csv',
        'colunas': {
            'orgao': 'Descricao',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': None,
            'estado': 'ES'
        }
    },
    'GO': {  
        'arquivo': '../csvs/*GO*.csv',
        'colunas': {
            'orgao': 'View Execucao Orcamentaria Visao Geral[Nome Orgao]',
            'valor_pago': 'View Execucao Orcamentaria Visao Geral[Valor Pago]',
            'valor_empenhado': 'View Execucao Orcamentaria Visao Geral[Valor Empenho]',
            'ano': 'View Execucao Orcamentaria Visao Geral[Numero Ano]',
            'estado': 'GO'
        }
    },
    'MA': {  
        'arquivo': '../csvs/*MA*.csv',
        'colunas': {
            'orgao': None,  
            'valor_pago': None,
            'valor_empenhado': None,
            'ano': None,
            'estado': 'MA'
        }
    },
    'MT': {  
        'arquivo': '../csvs/*MT*.csv',
        'colunas': {
            'orgao': 'Função',  
            'valor_pago': 'Valor Pagamento',
            'valor_empenhado': 'Valor Empenho',
            'ano': None,
            'estado': 'MT'
        }
    },
    'MS': {  
        'arquivo': '../csvs/*MS*.csv',
        'colunas': {
            'orgao': 'Orgão',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',  
            'ano': None,
            'estado': 'MS'
        }
    },
    'MG': {  
        'arquivo': '../csvs/*MG*.csv',
        'colunas': {
            'orgao': 'Órgão\xa0',
            'valor_pago': 'Valor Pago\xa0',
            'valor_empenhado': 'Valor Empenhado\xa0',
            'ano': None,
            'estado': 'MG'
        }
    },
    'PA': {  
        'arquivo': '../csvs/*PA*.csv',
        'colunas': {
            'orgao': 'Orgao',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': 'Ano',
            'estado': 'PA'
        }
    },
    'PB': {  
        'arquivo': '../csvs/*PB*.csv',
        'colunas': {
            'orgao': 'ORGAO',
            'valor_pago': 'VALOR PAGO',
            'valor_empenhado': 'VALOR EMPENHADO',
            'ano': 'ANO',
            'estado': 'PB'
        }
    },
    'PR': {  
        'arquivo': '../csvs/*PR*.csv',
        'colunas': {
            'orgao': 'Unidade Gestora',  
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': None,
            'estado': 'PR'
        }
    },
    'PE': {  
        'arquivo': '../csvs/*PE*.csv',
        'colunas': {
            'orgao': None,  
            'valor_pago': None,
            'valor_empenhado': None,
            'ano': None,
            'estado': 'PE'
        }
    },
    'PI': {  
        'arquivo': '../csvs/*PI*.csv',
        'colunas': {
            'orgao': 'Orgão',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': 'Data',
            'estado': 'PI'
        }
    },
    'RJ': {  
        'arquivo': '../csvs/*RJ*.csv',
        'colunas': {
            'orgao': 'Fun��o',  
            'valor_pago': None,  
            'valor_empenhado': 'Valor Empenhado',
            'ano': None,
            'estado': 'RJ'
        }
    },
    'RN': {  
        'arquivo': '../csvs/*RN*.csv',
        'colunas': {
            'orgao': 'Função',
            'valor_pago': 'Valor Pagamento',
            'valor_empenhado': 'Valor Empenhado',
            'ano': None,
            'estado': 'RN'
        }
    },
    'RS': {  
        'arquivo': '../csvs/*RS*.csv',
        'colunas': {
            'orgao': 'Órgão',
            'valor_pago': 'Valor',  
            'valor_empenhado': None,
            'ano': 'Ano',
            'estado': 'RS'
        }
    },
    'RO': {  
        'arquivo': '../csvs/*RO*.csv',
        'colunas': {
            'orgao': 'Secretaria',
            'valor_pago': 'DespesaPaga',
            'valor_empenhado': 'DespesaEmpenhada',
            'ano': None,
            'estado': 'RO'
        }
    },
    'RR': {  
        'arquivo': '../csvs/*RR*.csv',
        'colunas': {
            'orgao': 'desOrgao',
            'valor_pago': 'valorPago',
            'valor_empenhado': 'valorEmpenhado',
            'ano': None,
            'estado': 'RR'
        }
    },
    'SC': {  
        'arquivo': '../csvs/*SC*.csv',
        'colunas': {
            'orgao': 'nmunidadegestora',
            'valor_pago': 'vlpago',
            'valor_empenhado': 'vlempenhado',
            'ano': 'nuano',
            'estado': 'SC'
        }
    },
    'SP': {  
        'arquivo': '../csvs/*SP*.csv',
        'colunas': {
            'orgao': 'Ação',  
            'valor_pago': None,  
            'valor_empenhado': 'Empenhado',
            'ano': None,
            'estado': 'SP'
        }
    },
    'SE': {  
        'arquivo': '../csvs/*SE*.csv',
        'colunas': {
            'orgao': 'UNIDADE GOVERNAMENTAL',
            'valor_pago': 'PAGO',
            'valor_empenhado': 'EMPENHADO',
            'ano': 'ANO/MÊS',
            'estado': 'SE'
        }
    },
    'TO': {  
        'arquivo': '../csvs/*TO*.csv',
        'colunas': {
            'orgao': 'FUN��O',
            'valor_pago': 'PAGO',
            'valor_empenhado': 'EMPENHADO',
            'ano': None,
            'estado': 'TO'
        }
    }
}
