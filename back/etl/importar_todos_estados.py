import pandas as pd
import sqlite3
from datetime import datetime
import os
import glob
import csv
import unicodedata


NOME_BANCO = os.path.join('..', 'database', 'despesas_brasil.db')
NOME_TABELA = 'despesas'

def limpar_caracteres_especiais(texto):
    """
    Limpa caracteres especiais de encoding corrompido e normaliza o texto.
    """
    if pd.isna(texto) or texto is None:
        return texto
    
    texto_str = str(texto)
    
    
    mapeamento_caracteres = {
        
        'Judici�ria': 'Judiciária',
        'Justi�a': 'Justiça',
        'Administra��o': 'Administração',
        'Seguran�a': 'Segurança',
        'P�blica': 'Pública',
        'Rela��es': 'Relações',
        'Assist�ncia': 'Assistência',
        'Previd�ncia': 'Previdência',
        'Sa�de': 'Saúde',
        'Educa��o': 'Educação',
        'Habita��o': 'Habitação',
        'Gest�o': 'Gestão',
        'Ci�ncia': 'Ciência',
        'Organiza��o': 'Organização',
        'Agr�ria': 'Agrária',
        'Ind�stria': 'Indústria',
        'Com�rcio': 'Comércio',
        'Servi�os': 'Serviços',
        'Comunica��es': 'Comunicações',
        
        
        'EDUCAC?O': 'EDUCAÇÃO',
        'ADMINISTRAC?O': 'ADMINISTRAÇÃO',
        'SEGURANCA': 'SEGURANÇA',
        'GEST?O': 'GESTÃO',
        'CIENCIA': 'CIÊNCIA',
        'PREVID?NCIA': 'PREVIDÊNCIA',
        'SA?DE': 'SAÚDE',
        'HABITA??O': 'HABITAÇÃO',
        'COMUNICA??ES': 'COMUNICAÇÕES',
        'RELA??ES': 'RELAÇÕES',
        'ASSIST?NCIA': 'ASSISTÊNCIA',
        
        
        '�': 'ã',  
        '?': 'Ã',  
        'ï¿½': '',
        
        
        'Seguran�a P�blica': 'Segurança Pública',
        'Essencial � Justi�a': 'Essencial à Justiça',
        'Essencial � ': 'Essencial à ',
        '� ': 'à ',
        '�a': 'ça',
        '�o': 'ão',
        '�e': 'ãe',
        '�ncia': 'ência',
        '�ria': 'ária',
    }
    
    
    texto_limpo = texto_str
    for corrompido, correto in mapeamento_caracteres.items():
        texto_limpo = texto_limpo.replace(corrompido, correto)
    
    
    
    texto_final = ''.join(char for char in texto_limpo if ord(char) >= 32 or char in '\t\n\r')
    
    return texto_final.strip()


MAPEAMENTO_COLUNAS = {    'AC': {  
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
    },    'BA': {  
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
    },    'DF': {  
        'arquivo': '../csvs/*DF*.csv',
        'colunas': {
            'orgao': 'Unidade Gestora',
            'valor_pago': 'Valor Final',
            'valor_empenhado': None,  
            'ano': None,
            'estado': 'DF'
        }
    },    'ES': {  
        'arquivo': '../csvs/*ES*.csv',
        'colunas': {
            'orgao': 'Descricao',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': None,
            'estado': 'ES'
        }
    },    'GO': {  
        'arquivo': '../csvs/*GO*.csv',
        'colunas': {
            'orgao': 'View Execucao Orcamentaria Visao Geral[Nome Orgao]',
            'valor_pago': 'View Execucao Orcamentaria Visao Geral[Valor Pago]',
            'valor_empenhado': 'View Execucao Orcamentaria Visao Geral[Valor Empenho]',
            'ano': 'View Execucao Orcamentaria Visao Geral[Numero Ano]',
            'estado': 'GO'
        }
    },'MA': {  
        'arquivo': '../csvs/*MA*.csv',
        'colunas': {
            'orgao': None,  
            'valor_pago': None,
            'valor_empenhado': None,
            'ano': None,
            'estado': 'MA'
        }
    },    'MT': {  
        'arquivo': '../csvs/*MT*.csv',
        'colunas': {
            'orgao': 'Função',  
            'valor_pago': 'Valor Pagamento',
            'valor_empenhado': 'Valor Empenho',
            'ano': None,
            'estado': 'MT'
        }
    },'MS': {  
        'arquivo': '../csvs/*MS*.csv',
        'colunas': {
            'orgao': 'Orgão',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',  
            'ano': None,
            'estado': 'MS'
        }
    },    'MG': {  
        'arquivo': '../csvs/*MG*.csv',
        'colunas': {
            'orgao': 'Órgão\xa0',
            'valor_pago': 'Valor Pago\xa0',
            'valor_empenhado': 'Valor Empenhado\xa0',
            'ano': None,
            'estado': 'MG'
        }
    },    'PA': {  
        'arquivo': '../csvs/*PA*.csv',
        'colunas': {
            'orgao': 'Orgao',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': 'Ano',
            'estado': 'PA'
        }
    },    'PB': {  
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
            'orgao': None,  
            'valor_pago': None,
            'valor_empenhado': None,
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
    },    'PI': {  
        'arquivo': '../csvs/*PI*.csv',
        'colunas': {
            'orgao': 'Orgão',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': 'Data',
            'estado': 'PI'
        }
    },    'RJ': {  
        'arquivo': '../csvs/*RJ*.csv',
        'colunas': {
            'orgao': 'Fun��o',  
            'valor_pago': None,  
            'valor_empenhado': 'Valor Empenhado',
            'ano': None,
            'estado': 'RJ'
        }
    },    'RN': {  
        'arquivo': '../csvs/*RN*.csv',
        'colunas': {
            'orgao': 'Função',
            'valor_pago': 'Valor Pagamento',
            'valor_empenhado': 'Valor Empenhado',
            'ano': None,
            'estado': 'RN'
        }
    },    'RS': {  
        'arquivo': '../csvs/*RS*.csv',
        'colunas': {
            'orgao': 'Órgão',
            'valor_pago': 'Valor',  
            'valor_empenhado': None,
            'ano': 'Ano',
            'estado': 'RS'
        }
    },    'RO': {  
        'arquivo': '../csvs/*RO*.csv',
        'colunas': {
            'orgao': 'Secretaria',
            'valor_pago': 'DespesaPaga',
            'valor_empenhado': 'DespesaEmpenhada',
            'ano': None,
            'estado': 'RO'
        }
    },    'RR': {  
        'arquivo': '../csvs/*RR*.csv',
        'colunas': {
            'orgao': 'desOrgao',
            'valor_pago': 'valorPago',
            'valor_empenhado': 'valorEmpenhado',
            'ano': None,
            'estado': 'RR'
        }
    },    'SC': {  
        'arquivo': '../csvs/*SC*.csv',
        'colunas': {
            'orgao': 'nmunidadegestora',
            'valor_pago': 'vlpago',
            'valor_empenhado': 'vlempenhado',
            'ano': 'nuano',
            'estado': 'SC'
        }
    },    'SP': {  
        'arquivo': '../csvs/*SP*.csv',
        'colunas': {
            'orgao': 'Ação',  
            'valor_pago': None,  
            'valor_empenhado': 'Empenhado',
            'ano': None,
            'estado': 'SP'
        }
    },    'SE': {  
        'arquivo': '../csvs/*SE*.csv',
        'colunas': {
            'orgao': 'UNIDADE GOVERNAMENTAL',
            'valor_pago': 'PAGO',
            'valor_empenhado': 'EMPENHADO',
            'ano': 'ANO/MÊS',
            'estado': 'SE'
        }
    },    'TO': {  
        'arquivo': '../csvs/*TO*.csv',
        'colunas': {
            'orgao': 'FUNÇÃO',
            'valor_pago': 'PAGO',
            'valor_empenhado': 'EMPENHADO',
            'ano': None,
            'estado': 'TO'
        }
    }
}

def mapear_categoria_padronizada(orgao):
    """
    Mapeia o órgão para uma categoria padronizada baseada na área de atuação.
    Usa sistema de pontuação para priorizar categorias mais específicas.
    """
    if pd.isna(orgao) or orgao is None:
        return 'Outros'
    
    orgao_lower = str(orgao).lower()
    
    
    
    categorias_pontuacao = {}
    
    
    categorias_config = {
        'Tecnologia da Informação e Inovação': {
            'palavras': ['tecnologia', 'informação', 'informacao', 'informaçao', 'informatica', 'tic', 'inovação', 'inovacao', 'ciência', 'ciencia'],
            'peso_base': 100,
            'palavras_especificas': ['ciência, tecnologia', 'tecnologia e inovação', 'desenvolvimento, ciência, tecnologia']
        },
        'Educação': {
            'palavras': ['educação', 'educacao', 'educaçao', 'escola', 'ensino', 'universidade', 'educacional'],
            'peso_base': 90,
            'palavras_especificas': []
        },
        'Saúde': {
            'palavras': ['saúde', 'saude', 'hospital', 'médico', 'medico', 'medicamento'],
            'peso_base': 90,
            'palavras_especificas': []
        },        'Segurança Pública': {
            'palavras': ['segurança', 'seguranca', 'polícia', 'policia', 'bombeiro', 'militar', 'defesa civil', 'penitenciário', 'presídio'],
            'peso_base': 85,
            'palavras_especificas': ['segurança pública', 'defesa civil']
        },        'Infraestrutura e Transporte': {
            'palavras': ['infraestrutura', 'infra-estrutura', 'estrada', 'rodagem', 'transporte', 'obra', 'mobilidade', 'logística', 'logistica'],
            'peso_base': 80,
            'palavras_especificas': ['infraestrutura e logística', 'infraestrutura e transporte']
        },
        'Fazenda e Finanças': {
            'palavras': ['fazenda', 'finanças', 'financas', 'tributação', 'tributacao', 'receita', 'planejamento'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Meio Ambiente': {
            'palavras': ['meio ambiente', 'ambiental', 'floresta', 'sustentabilidade'],
            'peso_base': 70,  
            'palavras_especificas': []
        },        'Agricultura e Desenvolvimento Rural': {
            'palavras': ['agricultura', 'agraria', 'agrária', 'rural', 'agropecuária', 'agropecuaria', 'desenvolvimento rural', 'sanitária, animal', 'vegetal', 'fitossanitário', 'pecuária', 'defesa sanitária'],
            'peso_base': 75,
            'palavras_especificas': ['defesa sanitária, animal e vegetal', 'sanitária, animal e vegetal']
        },
        'Assistência Social': {
            'palavras': ['social', 'assistência', 'assistencia', 'cidadania', 'família', 'familia'],
            'peso_base': 65,
            'palavras_especificas': []
        },
        'Cultura, Esporte e Turismo': {
            'palavras': ['turismo', 'cultura', 'esporte', 'lazer'],
            'peso_base': 70,
            'palavras_especificas': []
        },
        'Habitação e Urbanismo': {
            'palavras': ['habitação','habitacao', 'moradia', 'urbanismo', 'cidade', 'desenvolvimento urbano'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Trabalho e Emprego': {
            'palavras': ['trabalho', 'emprego', 'qualificação', 'profissionalização', 'carteira assinada'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Indústria e Comércio': {
            'palavras': ['indústria', 'industrial', 'comércio', 'comercio', 'junta comercial', 'desenvolvimento econômico', 'empreendedorismo'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Saneamento e Recursos Hídricos': {
            'palavras': ['saneamento', 'água', 'agua', 'esgoto', 'hídrico', 'hidrico', 'recursos hídricos'],
            'peso_base': 80,
            'palavras_especificas': []
        },
        'Direitos Humanos e Igualdade': {
            'palavras': ['direitos humanos', 'igualdade', 'diversidade', 'mulher', 'racial', 'gênero', 'genero'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Energia': {
            'palavras': ['energia', 'energética', 'energetica'],
            'peso_base': 80,
            'palavras_especificas': []
        },
        'Comunicação': {
            'palavras': ['comunicação', 'comunicacao', 'rádio', 'radio', 'televisão', 'televisao'],
            'peso_base': 75,
            'palavras_especificas': []
        },
        'Administração e Gestão Pública': {
            'palavras': ['administração', 'gestão', 'servidor', 'recursos humanos', 'rh', 'pessoal', 'administração pública'],
            'peso_base': 50,  
            'palavras_especificas': []
        },
        'Poder Legislativo': {
            'palavras': ['legislativa', 'assembleia', 'câmara', 'camara'],
            'peso_base': 85,
            'palavras_especificas': []
        },
        'Poder Judiciário': {
            'palavras': ['judiciário', 'judiciario', 'judiciária', 'judiciaria', 'tribunal', 'justiça', 'justica'],
            'peso_base': 85,
            'palavras_especificas': []
        },
        'Ministério Público e Controle': {
            'palavras': ['ministério público', 'ministerio publico', 'mp', 'controle externo'],
            'peso_base': 85,
            'palavras_especificas': []
        },
        'Administração Geral': {
            'palavras': ['governadoria', 'gabinete', 'casa civil'],
            'peso_base': 80,
            'palavras_especificas': []
        },
        'Reserva de Contingência': {
            'palavras': ['reserva', 'contingência', 'contingencia'],
            'peso_base': 90,
            'palavras_especificas': []
        },
        'Encargos da Dívida': {
            'palavras': ['dívida', 'divida', 'encargo', 'financiamento', 'amortização', 'amortizacao'],
            'peso_base': 85,
            'palavras_especificas': []
        }
    }
    
    
    for categoria, config in categorias_config.items():
        pontuacao = 0
        
        
        for palavra_especifica in config['palavras_especificas']:
            if palavra_especifica in orgao_lower:
                pontuacao += config['peso_base'] * 2  
        
        
        for palavra in config['palavras']:
            if palavra in orgao_lower:
                pontuacao += config['peso_base']
        
        if pontuacao > 0:
            categorias_pontuacao[categoria] = pontuacao
    
    
    if categorias_pontuacao:
        categoria_escolhida = max(categorias_pontuacao.items(), key=lambda x: x[1])
        return categoria_escolhida[0]
    
    return 'Outros'


def detectar_colunas_csv(df, sigla_estado):
    """
    Detecta e sugere as colunas corretas baseado no conteúdo do CSV.
    """
    colunas_disponiveis = list(df.columns)
    print(f"  🔍 Detectando colunas para {sigla_estado}...")
    
    
    possiveis_orgao = []
    for col in colunas_disponiveis:
        col_lower = col.lower()
        if any(palavra in col_lower for palavra in ['orgao', 'órgão', 'organ', 'secretaria', 'unidade', 'gestora', 'função', 'funcao', 'ação', 'acao', 'descricao', 'descrição']):
            possiveis_orgao.append(col)
    
    
    possiveis_empenhado = []
    possiveis_pago = []
    
    for col in colunas_disponiveis:
        col_lower = col.lower()
        if any(palavra in col_lower for palavra in ['empenhado', 'empenho']):
            possiveis_empenhado.append(col)
        elif any(palavra in col_lower for palavra in ['pago', 'pagamento', 'valor final', 'valor pago', 'vlpago']):
            possiveis_pago.append(col)
        elif 'valor' in col_lower and 'empenhado' not in col_lower and 'pago' not in col_lower:
            
            if 'empenhado' in str(df[col].head()).lower():
                possiveis_empenhado.append(col)
            else:
                possiveis_pago.append(col)
    
    print(f"    📋 Possíveis colunas de órgão: {possiveis_orgao}")
    print(f"    💰 Possíveis colunas de valor empenhado: {possiveis_empenhado}")
    print(f"    💵 Possíveis colunas de valor pago: {possiveis_pago}")
    
    return {
        'orgao': possiveis_orgao[0] if possiveis_orgao else None,
        'valor_empenhado': possiveis_empenhado[0] if possiveis_empenhado else None,
        'valor_pago': possiveis_pago[0] if possiveis_pago else None
    }

def obter_valor_coluna(row, nome_coluna):
    """
    Obtém o valor de uma coluna, tratando diferentes tipos de dados e formatos.
    """
    if nome_coluna is None:
        return None
    
    try:
        if nome_coluna not in row.index:
            return None
            
        valor = row[nome_coluna]
        if pd.isna(valor) or valor == 0 or valor == '':
            return None
        
        
        if isinstance(valor, str):
            
            valor = valor.strip().replace('R$', '').replace('$', '').replace(' ', '')
            
            
            if ',' in valor and '.' in valor:
                
                valor = valor.replace('.', '').replace(',', '.')
            elif ',' in valor and '.' not in valor:
                
                valor = valor.replace(',', '.')
            
            
            
            try:
                valor = float(valor)
            except ValueError:
                return None
        else:
            valor = float(valor)
            
        return valor if valor > 0 else None
    except (KeyError, ValueError, TypeError):
        return None

def processar_estado(sigla_estado):
    """
    Processa o CSV de um estado específico.
    """
    if sigla_estado not in MAPEAMENTO_COLUNAS:
        print(f"❌ Estado {sigla_estado} não configurado no mapeamento.")
        return 0
    
    config = MAPEAMENTO_COLUNAS[sigla_estado]
    
    
    arquivos = glob.glob(config['arquivo'])
    if not arquivos:
        print(f"❌ Arquivo não encontrado para {sigla_estado} (padrão: {config['arquivo']})")
        return 0
    
    arquivo = arquivos[0]
    print(f"📁 Processando {sigla_estado}: {arquivo}")
    
    
    if sigla_estado == 'RO':
        return processar_rondonia_csv_reader(arquivo)
    
    
    if sigla_estado == 'RS':
        return processar_rs_csv_reader(arquivo)
    
    elif sigla_estado == 'RS':
        return processar_rs_csv_reader(arquivo)
    
    try:        
        
        df = None
        
        
        try:
            df = pd.read_csv(arquivo, encoding='utf-8', on_bad_lines='skip')
            
            if len(df.columns) == 1 and ';' in df.columns[0]:
                
                df = pd.read_csv(arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
        except UnicodeDecodeError:
            
            try:
                df = pd.read_csv(arquivo, encoding='latin-1', on_bad_lines='skip')
                
                if len(df.columns) == 1 and ';' in df.columns[0]:
                    
                    df = pd.read_csv(arquivo, encoding='latin-1', sep=';', on_bad_lines='skip')
            except:
                
                try:
                    df = pd.read_csv(arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
                except:
                    df = pd.read_csv(arquivo, encoding='latin-1', sep=';', on_bad_lines='skip')
        except:
            
            try:
                df = pd.read_csv(arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
            except:
                df = pd.read_csv(arquivo, encoding='latin-1', sep=';', on_bad_lines='skip')
        
        print(f"  ✅ CSV carregado. Total de linhas: {len(df)}")
          
        print(f"  📋 Colunas no CSV: {list(df.columns)}")
        
        
        colunas = config['colunas'].copy()
        colunas_detectadas = False
        
        
        if colunas['orgao'] and colunas['orgao'] not in df.columns:
            print(f"  ⚠️  Coluna de órgão '{colunas['orgao']}' não encontrada. Detectando automaticamente...")
            colunas_auto = detectar_colunas_csv(df, sigla_estado)
            if colunas_auto['orgao']:
                colunas['orgao'] = colunas_auto['orgao']
                colunas_detectadas = True
        
        
        if colunas['valor_empenhado'] and colunas['valor_empenhado'] not in df.columns:
            print(f"  ⚠️  Coluna valor empenhado '{colunas['valor_empenhado']}' não encontrada. Detectando automaticamente...")
            if not colunas_detectadas:
                colunas_auto = detectar_colunas_csv(df, sigla_estado)
            if colunas_auto['valor_empenhado']:
                colunas['valor_empenhado'] = colunas_auto['valor_empenhado']
        
        
        if colunas['valor_pago'] and colunas['valor_pago'] not in df.columns:
            print(f"  ⚠️  Coluna valor pago '{colunas['valor_pago']}' não encontrada. Detectando automaticamente...")
            if not colunas_detectadas:
                colunas_auto = detectar_colunas_csv(df, sigla_estado)
            if colunas_auto['valor_pago']:
                colunas['valor_pago'] = colunas_auto['valor_pago']
        
        
        if not colunas['orgao'] or (not colunas['valor_empenhado'] and not colunas['valor_pago']):
            print(f"  🔍 Detectando todas as colunas automaticamente para {sigla_estado}...")
            colunas_auto = detectar_colunas_csv(df, sigla_estado)
            if colunas_auto['orgao']:
                colunas['orgao'] = colunas_auto['orgao']
            if colunas_auto['valor_empenhado']:
                colunas['valor_empenhado'] = colunas_auto['valor_empenhado']
            if colunas_auto['valor_pago']:
                colunas['valor_pago'] = colunas_auto['valor_pago']
        
        
        print(f"  📊 Colunas que serão usadas:")
        print(f"    - Órgão: '{colunas['orgao']}'")
        print(f"    - Valor empenhado: '{colunas['valor_empenhado']}'")
        print(f"    - Valor pago: '{colunas['valor_pago']}'")
        
        valor_empenhado_col = colunas['valor_empenhado']
        valor_pago_col = colunas['valor_pago']
        
        if valor_empenhado_col and valor_empenhado_col in df.columns:
            print(f"  ✅ Coluna valor empenhado encontrada: '{valor_empenhado_col}'")
        else:
            print(f"  ⚠️  Coluna valor empenhado não encontrada: '{valor_empenhado_col}'")
            
        if valor_pago_col and valor_pago_col in df.columns:
            print(f"  ✅ Coluna valor pago encontrada: '{valor_pago_col}'")
        else:
            print(f"  ⚠️  Coluna valor pago não encontrada: '{valor_pago_col}'")
        dados_processados = []
        colunas = config['colunas']
        
        contador_empenhado = 0
        contador_pago = 0
        
        for _, row in df.iterrows():
            
            orgao_raw = row[colunas['orgao']] if colunas['orgao'] and colunas['orgao'] in row.index and pd.notna(row[colunas['orgao']]) else None
            
            if orgao_raw is not None:
                
                orgao = limpar_caracteres_especiais(str(orgao_raw))
            else:
                orgao = 'Não informado'
            
            
            valor_empenhado = obter_valor_coluna(row, colunas['valor_empenhado'])
            valor_pago = obter_valor_coluna(row, colunas['valor_pago'])
            
            
            if valor_empenhado is not None:
                valor_final = valor_empenhado
                contador_empenhado += 1
            elif valor_pago is not None:
                valor_final = valor_pago
                contador_pago += 1
            else:
                valor_final = None
            
            
            categoria = mapear_categoria_padronizada(orgao)
            
            
            data = datetime(2024, 1, 1).date()
            
            
            if valor_final is not None and valor_final > 0:
                dados_processados.append({
                    'estado': sigla_estado,
                    'data': data,
                    'orgao': orgao,
                    'categoria_padronizada': categoria,
                    'valor': valor_final
                })
          
        if dados_processados:
            df_final = pd.DataFrame(dados_processados)
            conn = sqlite3.connect(NOME_BANCO)
            df_final.to_sql(NOME_TABELA, conn, if_exists='append', index=False)
            conn.commit()
            conn.close()
            
            print(f"  ✅ {len(df_final)} registros inseridos para {sigla_estado}")
            print(f"  📊 Valores empenhados: {contador_empenhado}, Valores pagos: {contador_pago}")
            return len(df_final)
        else:
            print(f"  ⚠️  Nenhum dado válido encontrado para {sigla_estado}")
            return 0
            
    except Exception as e:
        print(f"  ❌ Erro ao processar {sigla_estado}: {e}")
        return 0

def processar_todos_estados():
    """
    Processa todos os estados disponíveis.
    """
    print("🚀 Iniciando processamento de todos os estados...")
    print("="*60)
    
    total_registros = 0
    estados_processados = 0
    
    for sigla_estado in MAPEAMENTO_COLUNAS.keys():
        registros = processar_estado(sigla_estado)
        if registros > 0:
            total_registros += registros
            estados_processados += 1
        print("-" * 60)
    
    print(f"\n🎉 RESUMO FINAL:")
    print(f"   Estados processados: {estados_processados}")
    print(f"   Total de registros inseridos: {total_registros}")

def verificar_banco():
    """
    Verifica se o banco existe e cria a tabela se necessário.
    """
    try:
        
        database_dir = os.path.dirname(NOME_BANCO)
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)
            print(f"📁 Pasta criada: {database_dir}")
        
        conn = sqlite3.connect(NOME_BANCO)
        cursor = conn.cursor()
        
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (NOME_TABELA,))
        if not cursor.fetchone():
            print(f"⚠️  Tabela '{NOME_TABELA}' não existe. Criando automaticamente...")
            
            
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
            print(f"✅ Tabela '{NOME_TABELA}' criada com sucesso!")
            
        
        cursor.execute(f"SELECT COUNT(*) FROM {NOME_TABELA}")
        total_registros = cursor.fetchone()[0]
        print(f"📊 Banco atual possui {total_registros} registros.")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao verificar/criar o banco: {e}")
        return False

def analisar_todos_csvs():
    """
    Analisa a estrutura de todos os CSVs disponíveis para verificar os mapeamentos.
    """
    print("🔍 ANALISANDO ESTRUTURA DE TODOS OS CSVs...")
    print("="*80)
    
    for sigla_estado, config in MAPEAMENTO_COLUNAS.items():
        arquivos = glob.glob(config['arquivo'])
        if not arquivos:
            print(f"❌ {sigla_estado}: Arquivo não encontrado (padrão: {config['arquivo']})")
            continue
            
        arquivo = arquivos[0]
        print(f"\n📁 {sigla_estado}: {arquivo}")
        
        try:
            
            df = None
            try:
                df = pd.read_csv(arquivo, encoding='utf-8', on_bad_lines='skip')
                if len(df.columns) == 1 and ';' in df.columns[0]:
                    df = pd.read_csv(arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(arquivo, encoding='latin-1', on_bad_lines='skip')
                    if len(df.columns) == 1 and ';' in df.columns[0]:
                        df = pd.read_csv(arquivo, encoding='latin-1', sep=';', on_bad_lines='skip')
                except:
                    df = pd.read_csv(arquivo, encoding='latin-1', sep=';', on_bad_lines='skip')
            except:
                df = pd.read_csv(arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
            
            print(f"  📋 Colunas disponíveis: {list(df.columns)}")
            print(f"  📊 Total de linhas: {len(df)}")
            
            
            colunas_config = config['colunas']
            print(f"  🗺️  Mapeamento atual:")
            print(f"    - Órgão: '{colunas_config['orgao']}' {'✅' if colunas_config['orgao'] in df.columns else '❌'}")
            print(f"    - Valor empenhado: '{colunas_config['valor_empenhado']}' {'✅' if colunas_config['valor_empenhado'] and colunas_config['valor_empenhado'] in df.columns else '❌'}")
            print(f"    - Valor pago: '{colunas_config['valor_pago']}' {'✅' if colunas_config['valor_pago'] and colunas_config['valor_pago'] in df.columns else '❌'}")
            
            
            if (not colunas_config['orgao'] or colunas_config['orgao'] not in df.columns or
                (colunas_config['valor_empenhado'] and colunas_config['valor_empenhado'] not in df.columns) or
                (colunas_config['valor_pago'] and colunas_config['valor_pago'] not in df.columns)):
                print(f"  🔍 Sugestões de detecção automática:")
                colunas_auto = detectar_colunas_csv(df, sigla_estado)
                if colunas_auto['orgao']:
                    print(f"    - Órgão: '{colunas_auto['orgao']}'")
                if colunas_auto['valor_empenhado']:
                    print(f"    - Valor empenhado: '{colunas_auto['valor_empenhado']}'")
                if colunas_auto['valor_pago']:
                    print(f"    - Valor pago: '{colunas_auto['valor_pago']}'")
        
        except Exception as e:
            print(f"  ❌ Erro ao analisar: {e}")
        
        print("-" * 80)

def processar_rondonia_csv_reader(arquivo):
    """
    Processa especificamente o CSV de Rondônia usando csv.reader para evitar problemas de parsing.
    """
    print(f"  🔧 Processamento especial para Rondônia usando csv.reader")
    
    try:
        dados_processados = []
        
        with open(arquivo, encoding="utf-8") as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            cabecalho = next(leitor)
            
            
            idx_secretaria = cabecalho.index("Secretaria")
            idx_empenhada = cabecalho.index("DespesaEmpenhada")
            idx_paga = cabecalho.index("DespesaPaga")
            
            print(f"  📋 Colunas encontradas:")
            print(f"    - Secretaria (índice {idx_secretaria})")
            print(f"    - DespesaEmpenhada (índice {idx_empenhada})")
            print(f"    - DespesaPaga (índice {idx_paga})")
            
            contador_empenhado = 0
            contador_pago = 0
            linhas_processadas = 0
            
            for linha in leitor:
                try:
                    linhas_processadas += 1
                    
                    
                    secretaria = linha[idx_secretaria] if idx_secretaria < len(linha) else 'Não informado'
                    valor_empenhado_str = linha[idx_empenhada] if idx_empenhada < len(linha) else '0'
                    valor_pago_str = linha[idx_paga] if idx_paga < len(linha) else '0'
                    
                    
                    try:
                        valor_empenhado = float(valor_empenhado_str.replace(',', '.')) if valor_empenhado_str and valor_empenhado_str != '' else 0
                    except (ValueError, AttributeError):
                        valor_empenhado = 0
                        
                    try:
                        valor_pago = float(valor_pago_str.replace(',', '.')) if valor_pago_str and valor_pago_str != '' else 0
                    except (ValueError, AttributeError):
                        valor_pago = 0
                    
                    
                    if valor_empenhado > 0:
                        valor_final = valor_empenhado
                        contador_empenhado += 1
                    elif valor_pago > 0:
                        valor_final = valor_pago
                        contador_pago += 1
                    else:
                        valor_final = None
                    
                    
                    if valor_final is not None and valor_final > 0:
                        
                        categoria = mapear_categoria_padronizada(secretaria)
                        
                        
                        data = datetime(2024, 1, 1).date()
                        
                        dados_processados.append({
                            'estado': 'RO',
                            'data': data,
                            'orgao': secretaria,
                            'categoria_padronizada': categoria,
                            'valor': valor_final
                        })
                        
                except (IndexError, ValueError) as e:
                    print(f"  ⚠️  Erro na linha {linhas_processadas}: {e}")
                    continue
            
            print(f"  📊 Linhas processadas: {linhas_processadas}")
            print(f"  📊 Registros válidos: {len(dados_processados)}")
            
            
            if dados_processados:
                df_final = pd.DataFrame(dados_processados)
                conn = sqlite3.connect(NOME_BANCO)
                df_final.to_sql(NOME_TABELA, conn, if_exists='append', index=False)
                conn.commit()
                conn.close()
                
                print(f"  ✅ {len(df_final)} registros inseridos para RO")
                print(f"  📊 Valores empenhados: {contador_empenhado}, Valores pagos: {contador_pago}")
                return len(df_final)
            else:
                print(f"  ⚠️  Nenhum dado válido encontrado para RO")
                return 0
                
    except Exception as e:
        print(f"  ❌ Erro ao processar RO: {e}")
        return 0

def processar_rs_csv_reader(arquivo):
    """
    Processa especificamente o CSV do Rio Grande do Sul filtrando apenas dados de 2024.
    """
    print(f"  🔧 Processamento especial para RS filtrando ano 2024")
    
    try:
        dados_processados = []
        
        with open(arquivo, encoding="utf-8") as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            cabecalho = next(leitor)
            
            
            cabecalho = [col.strip().replace('\ufeff', '') for col in cabecalho]
            
            
            idx_ano = cabecalho.index("Ano")
            idx_orgao = cabecalho.index("Órgão")
            idx_valor = cabecalho.index("Valor")
            idx_fase = cabecalho.index("Fase Gasto")
            
            print(f"  📋 Colunas encontradas:")
            print(f"    - Ano (índice {idx_ano})")
            print(f"    - Órgão (índice {idx_orgao})")
            print(f"    - Valor (índice {idx_valor})")
            print(f"    - Fase Gasto (índice {idx_fase})")
            
            contador_total = 0
            contador_2024 = 0
            contador_empenhado = 0
            contador_pago = 0
            linhas_processadas = 0
            
            for linha in leitor:
                try:
                    linhas_processadas += 1
                    contador_total += 1
                    
                    
                    ano = linha[idx_ano] if idx_ano < len(linha) else ''
                    orgao = linha[idx_orgao] if idx_orgao < len(linha) else 'Não informado'
                    valor_str = linha[idx_valor] if idx_valor < len(linha) else '0'
                    fase_gasto = linha[idx_fase] if idx_fase < len(linha) else ''
                    
                    
                    if ano != '2024':
                        continue
                    
                    contador_2024 += 1
                    
                    
                    orgao_limpo = limpar_caracteres_especiais(orgao)
                    
                    
                    try:
                        
                        valor_limpo = valor_str.replace('R$', '').replace(' ', '').strip()
                        if ',' in valor_limpo and '.' in valor_limpo:
                            
                            valor_limpo = valor_limpo.replace('.', '').replace(',', '.')
                        elif ',' in valor_limpo and '.' not in valor_limpo:
                            
                            valor_limpo = valor_limpo.replace(',', '.')
                        
                        valor = float(valor_limpo) if valor_limpo else 0
                    except (ValueError, AttributeError):
                        valor = 0
                    
                    
                    if 'empenhado' in fase_gasto.lower():
                        contador_empenhado += 1
                    elif 'pago' in fase_gasto.lower():
                        contador_pago += 1
                    
                    
                    if valor > 0:
                        
                        categoria = mapear_categoria_padronizada(orgao_limpo)
                        
                        
                        data = datetime(2024, 1, 1).date()
                        
                        dados_processados.append({
                            'estado': 'RS',
                            'data': data,
                            'orgao': orgao_limpo,
                            'categoria_padronizada': categoria,
                            'valor': valor
                        })
                        
                except (IndexError, ValueError) as e:
                    print(f"  ⚠️  Erro na linha {linhas_processadas}: {e}")
                    continue
            
            print(f"  📊 Estatísticas de processamento:")
            print(f"    - Total de linhas processadas: {linhas_processadas}")
            print(f"    - Registros totais no arquivo: {contador_total}")
            print(f"    - Registros de 2024: {contador_2024}")
            print(f"    - Registros empenhados: {contador_empenhado}")
            print(f"    - Registros pagos: {contador_pago}")
            print(f"    - Registros válidos para inserção: {len(dados_processados)}")
            
            
            if dados_processados:
                df_final = pd.DataFrame(dados_processados)
                conn = sqlite3.connect(NOME_BANCO)
                df_final.to_sql(NOME_TABELA, conn, if_exists='append', index=False)
                conn.commit()
                conn.close()
                
                print(f"  ✅ {len(df_final)} registros de 2024 inseridos para RS")
                return len(df_final)
            else:
                print(f"  ⚠️  Nenhum dado válido de 2024 encontrado para RS")
                return 0
                
    except Exception as e:
        print(f"  ❌ Erro ao processar RS: {e}")
        import traceback
        traceback.print_exc()
        return 0

if __name__ == "__main__":
    print("🔍 Verificando banco de dados...")
    if verificar_banco():
        print("\n🚀 Iniciando processamento dos dados de todos os estados...")
        processar_todos_estados()
    else:
        print("❌ Erro ao acessar o banco de dados.")
        
    
    