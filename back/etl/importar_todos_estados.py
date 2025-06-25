import pandas as pd
import sqlite3
from datetime import datetime
import os
import glob
import csv

# --- CONSTANTES ---
NOME_BANCO = os.path.join('..', 'database', 'despesas_brasil.db')
NOME_TABELA = 'despesas'

# --- MAPEAMENTO DE COLUNAS POR ESTADO ---
MAPEAMENTO_COLUNAS = {    'AC': {  # Acre
        'arquivo': '../csvs/*AC*.csv',
        'colunas': {
            'orgao': 'descricao',
            'valor_pago': 'pago',
            'valor_empenhado': 'empenhado',
            'ano': None,
            'estado': 'AC'
        }
    },
    'AL': {  # Alagoas
        'arquivo': '../csvs/*AL*.csv',
        'colunas': {
            'orgao': 'orgao_descricao',
            'valor_pago': 'total_pago',
            'valor_empenhado': 'total_empenhado',
            'ano': 'data_final',
            'estado': 'AL'
        }
    },
    'AP': {  # Amapá
        'arquivo': '../csvs/*AP*.csv',
        'colunas': {
            'orgao': 'NOME_UNIDADE_GESTORA',
            'valor_pago': 'VAL_PAGO',
            'valor_empenhado': 'VAL_EMPENHADO',
            'ano': 'ANO',
            'estado': 'AP'
        }
    },
    'AM': {  # Amazonas
        'arquivo': '../csvs/*AM*.csv',
        'colunas': {
            'orgao': 'Função',  # Usando função como referência
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': None,
            'estado': 'AM'
        }
    },    'BA': {  # Bahia
        'arquivo': '../csvs/*BA*.csv',
        'colunas': {
            'orgao': 'Órgão',
            'valor_pago': 'Valor Pago',
            'valor_empenhado': 'Valor Empenhado',
            'ano': 'Ano',
            'estado': 'BA'
        }
    },
    'CE': {  # Ceará
        'arquivo': '../csvs/*CE*.csv',
        'colunas': {
            'orgao': 'Unidade gestora',
            'valor_pago': 'Valor pago final',
            'valor_empenhado': 'Valor empenhado final',
            'ano': 'Exercício',
            'estado': 'CE'
        }
    },    'DF': {  # Distrito Federal
        'arquivo': '../csvs/*DF*.csv',
        'colunas': {
            'orgao': 'Unidade Gestora',
            'valor_pago': 'Valor Final',
            'valor_empenhado': None,  # DF não tem coluna específica de empenhado
            'ano': None,
            'estado': 'DF'
        }
    },    'ES': {  # Espírito Santo
        'arquivo': '../csvs/*ES*.csv',
        'colunas': {
            'orgao': 'Descricao',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': None,
            'estado': 'ES'
        }
    },    'GO': {  # Goiás
        'arquivo': '../csvs/*GO*.csv',
        'colunas': {
            'orgao': 'View Execucao Orcamentaria Visao Geral[Nome Orgao]',
            'valor_pago': 'View Execucao Orcamentaria Visao Geral[Valor Pago]',
            'valor_empenhado': 'View Execucao Orcamentaria Visao Geral[Valor Empenho]',
            'ano': 'View Execucao Orcamentaria Visao Geral[Numero Ano]',
            'estado': 'GO'
        }
    },'MA': {  # Maranhão
        'arquivo': '../csvs/*MA*.csv',
        'colunas': {
            'orgao': None,  # Precisará ser verificado no arquivo real
            'valor_pago': None,
            'valor_empenhado': None,
            'ano': None,
            'estado': 'MA'
        }
    },    'MT': {  # Mato Grosso
        'arquivo': '../csvs/*MT*.csv',
        'colunas': {
            'orgao': 'Subelemento',
            'valor_pago': 'Valor Pagamento',
            'valor_empenhado': 'Valor Empenho',
            'ano': None,
            'estado': 'MT'
        }
    },'MS': {  # Mato Grosso do Sul
        'arquivo': '../csvs/*MS*.csv',
        'colunas': {
            'orgao': 'Orgão',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',  # MS tem ambos
            'ano': None,
            'estado': 'MS'
        }
    },    'MG': {  # Minas Gerais
        'arquivo': '../csvs/*MG*.csv',
        'colunas': {
            'orgao': 'Órgão\xa0',
            'valor_pago': 'Valor Pago\xa0',
            'valor_empenhado': 'Valor Empenhado\xa0',
            'ano': None,
            'estado': 'MG'
        }
    },    'PA': {  # Pará
        'arquivo': '../csvs/*PA*.csv',
        'colunas': {
            'orgao': 'Orgao',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': 'Ano',
            'estado': 'PA'
        }
    },    'PB': {  # Paraíba
        'arquivo': '../csvs/*PB*.csv',
        'colunas': {
            'orgao': 'ORGAO',
            'valor_pago': 'VALOR PAGO',
            'valor_empenhado': 'VALOR EMPENHADO',
            'ano': 'ANO',
            'estado': 'PB'
        }
    },
    'PR': {  # Paraná
        'arquivo': '../csvs/*PR*.csv',
        'colunas': {
            'orgao': None,  # Precisará ser verificado no arquivo real
            'valor_pago': None,
            'valor_empenhado': None,
            'ano': None,
            'estado': 'PR'
        }
    },
    'PE': {  # Pernambuco
        'arquivo': '../csvs/*PE*.csv',
        'colunas': {
            'orgao': None,  # Precisará ser verificado no arquivo real
            'valor_pago': None,
            'valor_empenhado': None,
            'ano': None,
            'estado': 'PE'
        }
    },    'PI': {  # Piauí
        'arquivo': '../csvs/*PI*.csv',
        'colunas': {
            'orgao': 'Orgão',
            'valor_pago': 'Pago',
            'valor_empenhado': 'Empenhado',
            'ano': 'Data',
            'estado': 'PI'
        }
    },    'RJ': {  # Rio de Janeiro
        'arquivo': '../csvs/*RJ*.csv',
        'colunas': {
            'orgao': 'Função',
            'valor_pago': None,  # RJ não tem valor pago
            'valor_empenhado': 'Valor Empenhado',
            'ano': None,
            'estado': 'RJ'
        }
    },    'RN': {  # Rio Grande do Norte
        'arquivo': '../csvs/*RN*.csv',
        'colunas': {
            'orgao': 'Função',
            'valor_pago': 'Valor Pagamento',
            'valor_empenhado': 'Valor Empenhado',
            'ano': None,
            'estado': 'RN'
        }
    },    'RS': {  # Rio Grande do Sul
        'arquivo': '../csvs/*RS*.csv',
        'colunas': {
            'orgao': 'Órgão',
            'valor_pago': 'Valor',  # RS parece ter apenas um campo "Valor"
            'valor_empenhado': None,
            'ano': 'Ano',
            'estado': 'RS'
        }
    },    'RO': {  # Rondônia
        'arquivo': '../csvs/*RO*.csv',
        'colunas': {
            'orgao': 'Secretaria',
            'valor_pago': 'DespesaPaga',
            'valor_empenhado': 'DespesaEmpenhada',
            'ano': None,
            'estado': 'RO'
        }
    },    'RR': {  # Roraima
        'arquivo': '../csvs/*RR*.csv',
        'colunas': {
            'orgao': 'desOrgao',
            'valor_pago': 'valorPago',
            'valor_empenhado': 'valorEmpenhado',
            'ano': None,
            'estado': 'RR'
        }
    },    'SC': {  # Santa Catarina
        'arquivo': '../csvs/*SC*.csv',
        'colunas': {
            'orgao': 'nmunidadegestora',
            'valor_pago': 'vlpago',
            'valor_empenhado': 'vlempenhado',
            'ano': 'nuano',
            'estado': 'SC'
        }
    },    'SP': {  # São Paulo
        'arquivo': '../csvs/*SP*.csv',
        'colunas': {
            'orgao': 'Ação',  # SP pode usar Função ou Ação
            'valor_pago': None,  # SP não tem valor pago
            'valor_empenhado': 'Empenhado',
            'ano': None,
            'estado': 'SP'
        }
    },    'SE': {  # Sergipe
        'arquivo': '../csvs/*SE*.csv',
        'colunas': {
            'orgao': 'UNIDADE GOVERNAMENTAL',
            'valor_pago': 'PAGO',
            'valor_empenhado': 'EMPENHADO',
            'ano': 'ANO/MÊS',
            'estado': 'SE'
        }
    },    'TO': {  # Tocantins - Parece ter colunas duplicadas, usar as primeiras
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
    """
    if pd.isna(orgao) or orgao is None:
        return 'Outros'
    
    orgao_lower = str(orgao).lower()
    
    # Mapeamento de órgãos para categorias padronizadas
    if any(palavra in orgao_lower for palavra in ['educação', 'educacao', 'educaçao', 'escola', 'ensino', 'universidade', 'educacional']):
        return 'Educação'
    elif any(palavra in orgao_lower for palavra in ['saúde', 'saude', 'hospital', 'médico', 'medico', 'sus']):
        return 'Saúde'
    elif any(palavra in orgao_lower for palavra in ['segurança', 'seguranca', 'polícia', 'policia', 'bombeiro', 'militar', 'defesa']):
        return 'Segurança Pública'
    elif any(palavra in orgao_lower for palavra in ['infraestrutura', 'infra-estrutura', 'estrada', 'rodagem', 'transporte', 'obra', 'mobilidade']):
        return 'Infraestrutura e Transporte'
    elif any(palavra in orgao_lower for palavra in ['fazenda', 'finanças', 'financas', 'tributação', 'tributacao', 'receita', 'planejamento']):
        return 'Fazenda e Finanças'
    elif any(palavra in orgao_lower for palavra in ['social', 'assistência', 'assistencia', 'cidadania', 'família', 'familia']):
        return 'Assistência Social'
    elif any(palavra in orgao_lower for palavra in ['meio ambiente', 'ambiental', 'floresta', 'sustentabilidade']):
        return 'Meio Ambiente'
    elif any(palavra in orgao_lower for palavra in ['agricultura', 'rural', 'agropecuária', 'agropecuaria', 'desenvolvimento rural']):
        return 'Agricultura e Desenvolvimento Rural'
    elif any(palavra in orgao_lower for palavra in ['turismo', 'cultura', 'esporte', 'lazer']):
        return 'Cultura, Esporte e Turismo'
    elif any(palavra in orgao_lower for palavra in ['habitação','habitacao', 'moradia', 'urbanismo', 'cidade', 'desenvolvimento urbano']):
        return 'Habitação e Urbanismo'
    elif any(palavra in orgao_lower for palavra in ['trabalho', 'emprego', 'qualificação', 'profissionalização', 'carteira assinada']):
        return 'Trabalho e Emprego'
    elif any(palavra in orgao_lower for palavra in ['indústria', 'industrial', 'comércio', 'comercio', 'junta comercial', 'desenvolvimento econômico', 'empreendedorismo']):
        return 'Indústria e Comércio'
    elif any(palavra in orgao_lower for palavra in ['tecnologia', 'informação', 'informacao', 'informaçao', 'informatica', 'tic', 'inovação', 'inovacao', 'ciência', 'ciencia']):
        return 'Tecnologia da Informação e Inovação'
    elif any(palavra in orgao_lower for palavra in ['saneamento', 'água', 'agua', 'esgoto', 'hídrico', 'hidrico', 'recursos hídricos']):
        return 'Saneamento e Recursos Hídricos'
    elif any(palavra in orgao_lower for palavra in ['direitos humanos', 'igualdade', 'diversidade', 'mulher', 'racial', 'gênero', 'genero']):
        return 'Direitos Humanos e Igualdade'
    elif any(palavra in orgao_lower for palavra in ['energia', 'energética', 'energetica']):
        return 'Energia'
    elif any(palavra in orgao_lower for palavra in ['comunicação', 'comunicacao', 'rádio', 'radio', 'televisão', 'televisao']):
        return 'Comunicação'
    elif any(palavra in orgao_lower for palavra in ['administração', 'gestão', 'servidor', 'recursos humanos', 'rh', 'pessoal', 'administração pública']):
        return 'Administração e Gestão Pública'
    elif any(palavra in orgao_lower for palavra in ['legislativa', 'assembleia', 'câmara', 'camara']):
        return 'Poder Legislativo'
    elif any(palavra in orgao_lower for palavra in ['judiciário', 'judiciario', 'tribunal', 'justiça', 'justica']):
        return 'Poder Judiciário'
    elif any(palavra in orgao_lower for palavra in ['ministério público', 'ministerio publico', 'mp', 'controle externo']):
        return 'Ministério Público e Controle'
    elif any(palavra in orgao_lower for palavra in ['governadoria', 'gabinete', 'casa civil']):
        return 'Administração Geral'
    elif any(palavra in orgao_lower for palavra in ['reserva', 'contingência', 'contingencia']):
        return 'Reserva de Contingência'
    elif any(palavra in orgao_lower for palavra in ['dívida', 'divida', 'encargo', 'financiamento', 'amortização', 'amortizacao']):
        return 'Encargos da Dívida'
    else:
        return 'Outros'


def detectar_colunas_csv(df, sigla_estado):
    """
    Detecta e sugere as colunas corretas baseado no conteúdo do CSV.
    """
    colunas_disponiveis = list(df.columns)
    print(f"  🔍 Detectando colunas para {sigla_estado}...")
    
    # Detectar coluna de órgão
    possiveis_orgao = []
    for col in colunas_disponiveis:
        col_lower = col.lower()
        if any(palavra in col_lower for palavra in ['orgao', 'órgão', 'organ', 'secretaria', 'unidade', 'gestora', 'função', 'funcao', 'ação', 'acao', 'descricao', 'descrição']):
            possiveis_orgao.append(col)
    
    # Detectar colunas de valores
    possiveis_empenhado = []
    possiveis_pago = []
    
    for col in colunas_disponiveis:
        col_lower = col.lower()
        if any(palavra in col_lower for palavra in ['empenhado', 'empenho']):
            possiveis_empenhado.append(col)
        elif any(palavra in col_lower for palavra in ['pago', 'pagamento', 'valor final', 'valor pago', 'vlpago']):
            possiveis_pago.append(col)
        elif 'valor' in col_lower and 'empenhado' not in col_lower and 'pago' not in col_lower:
            # Valores genéricos que podem ser empenhado ou pago
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
        
        # Se for string, tentar converter diferentes formatos
        if isinstance(valor, str):
            # Remover espaços, R$, e outros caracteres
            valor = valor.strip().replace('R$', '').replace('$', '').replace(' ', '')
            
            # Tratar formato brasileiro (vírgula como decimal, ponto como milhares)
            if ',' in valor and '.' in valor:
                # Formato: 1.234.567,89
                valor = valor.replace('.', '').replace(',', '.')
            elif ',' in valor and '.' not in valor:
                # Formato: 1234567,89
                valor = valor.replace(',', '.')
            # Se só tem ponto, assumir formato americano: 1234567.89
            
            # Tentar converter para float
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
    
    # Buscar arquivo do estado
    arquivos = glob.glob(config['arquivo'])
    if not arquivos:
        print(f"❌ Arquivo não encontrado para {sigla_estado} (padrão: {config['arquivo']})")
        return 0
    
    arquivo = arquivos[0]
    print(f"📁 Processando {sigla_estado}: {arquivo}")
    
    # Processamento especial para Rondônia usando csv.reader
    if sigla_estado == 'RO':
        return processar_rondonia_csv_reader(arquivo)
    
    try:        # --- 1. LEITURA DO CSV ---
        # Tentar diferentes configurações de CSV
        df = None
        
        # Primeiro, tentar com UTF-8 padrão
        try:
            df = pd.read_csv(arquivo, encoding='utf-8', on_bad_lines='skip')
            # Verificar se as colunas parecem estar corretas
            if len(df.columns) == 1 and ';' in df.columns[0]:
                # Arquivo provavelmente usa separador ';'
                df = pd.read_csv(arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
        except UnicodeDecodeError:
            # Se falhar, tentar latin-1
            try:
                df = pd.read_csv(arquivo, encoding='latin-1', on_bad_lines='skip')
                # Verificar se as colunas parecem estar corretas
                if len(df.columns) == 1 and ';' in df.columns[0]:
                    # Arquivo provavelmente usa separador ';'
                    df = pd.read_csv(arquivo, encoding='latin-1', sep=';', on_bad_lines='skip')
            except:
                # Se ainda falhar, tentar com separador diferente
                try:
                    df = pd.read_csv(arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
                except:
                    df = pd.read_csv(arquivo, encoding='latin-1', sep=';', on_bad_lines='skip')
        except:
            # Se falhar, tentar com separador diferente
            try:
                df = pd.read_csv(arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
            except:
                df = pd.read_csv(arquivo, encoding='latin-1', sep=';', on_bad_lines='skip')
        
        print(f"  ✅ CSV carregado. Total de linhas: {len(df)}")
          # Debug: mostrar colunas disponíveis
        print(f"  📋 Colunas no CSV: {list(df.columns)}")
        
        # Verificar se as colunas mapeadas existem, senão detectar automaticamente
        colunas = config['colunas'].copy()
        colunas_detectadas = False
        
        # Verificar coluna de órgão
        if colunas['orgao'] and colunas['orgao'] not in df.columns:
            print(f"  ⚠️  Coluna de órgão '{colunas['orgao']}' não encontrada. Detectando automaticamente...")
            colunas_auto = detectar_colunas_csv(df, sigla_estado)
            if colunas_auto['orgao']:
                colunas['orgao'] = colunas_auto['orgao']
                colunas_detectadas = True
        
        # Verificar coluna de valor empenhado
        if colunas['valor_empenhado'] and colunas['valor_empenhado'] not in df.columns:
            print(f"  ⚠️  Coluna valor empenhado '{colunas['valor_empenhado']}' não encontrada. Detectando automaticamente...")
            if not colunas_detectadas:
                colunas_auto = detectar_colunas_csv(df, sigla_estado)
            if colunas_auto['valor_empenhado']:
                colunas['valor_empenhado'] = colunas_auto['valor_empenhado']
        
        # Verificar coluna de valor pago
        if colunas['valor_pago'] and colunas['valor_pago'] not in df.columns:
            print(f"  ⚠️  Coluna valor pago '{colunas['valor_pago']}' não encontrada. Detectando automaticamente...")
            if not colunas_detectadas:
                colunas_auto = detectar_colunas_csv(df, sigla_estado)
            if colunas_auto['valor_pago']:
                colunas['valor_pago'] = colunas_auto['valor_pago']
        
        # Se nenhuma coluna foi mapeada, detectar tudo automaticamente
        if not colunas['orgao'] or (not colunas['valor_empenhado'] and not colunas['valor_pago']):
            print(f"  🔍 Detectando todas as colunas automaticamente para {sigla_estado}...")
            colunas_auto = detectar_colunas_csv(df, sigla_estado)
            if colunas_auto['orgao']:
                colunas['orgao'] = colunas_auto['orgao']
            if colunas_auto['valor_empenhado']:
                colunas['valor_empenhado'] = colunas_auto['valor_empenhado']
            if colunas_auto['valor_pago']:
                colunas['valor_pago'] = colunas_auto['valor_pago']
        
        # Debug final: mostrar colunas que serão usadas
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
            print(f"  ⚠️  Coluna valor pago não encontrada: '{valor_pago_col}'")# --- 2. PREPARAÇÃO DOS DADOS ---
        dados_processados = []
        colunas = config['colunas']
        
        contador_empenhado = 0
        contador_pago = 0
        
        for _, row in df.iterrows():
            # Extrair informações da linha
            orgao = str(row[colunas['orgao']]) if colunas['orgao'] and colunas['orgao'] in row.index and pd.notna(row[colunas['orgao']]) else 'Não informado'
            
            # Priorizar valor empenhado, usar valor pago como fallback
            valor_empenhado = obter_valor_coluna(row, colunas['valor_empenhado'])
            valor_pago = obter_valor_coluna(row, colunas['valor_pago'])
            
            # Usar valor empenhado se disponível, senão usar valor pago
            if valor_empenhado is not None:
                valor_final = valor_empenhado
                contador_empenhado += 1
            elif valor_pago is not None:
                valor_final = valor_pago
                contador_pago += 1
            else:
                valor_final = None
            
            # Mapear categoria padronizada
            categoria = mapear_categoria_padronizada(orgao)
            
            # Data padrão para 2024
            data = datetime(2024, 1, 1).date()
            
            # Adicionar apenas se houver valor válido
            if valor_final is not None and valor_final > 0:
                dados_processados.append({
                    'estado': sigla_estado,
                    'data': data,
                    'orgao': orgao,
                    'categoria_padronizada': categoria,
                    'valor': valor_final
                })
          # --- 3. INSERÇÃO NO BANCO ---
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
        # Garantir que a pasta database existe
        database_dir = os.path.dirname(NOME_BANCO)
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)
            print(f"📁 Pasta criada: {database_dir}")
        
        conn = sqlite3.connect(NOME_BANCO)
        cursor = conn.cursor()
        
        # Verificar se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (NOME_TABELA,))
        if not cursor.fetchone():
            print(f"⚠️  Tabela '{NOME_TABELA}' não existe. Criando automaticamente...")
            
            # Criar a tabela
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
            
        # Contar registros existentes
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
            # Tentar carregar o CSV
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
            
            # Verificar mapeamento atual
            colunas_config = config['colunas']
            print(f"  🗺️  Mapeamento atual:")
            print(f"    - Órgão: '{colunas_config['orgao']}' {'✅' if colunas_config['orgao'] in df.columns else '❌'}")
            print(f"    - Valor empenhado: '{colunas_config['valor_empenhado']}' {'✅' if colunas_config['valor_empenhado'] and colunas_config['valor_empenhado'] in df.columns else '❌'}")
            print(f"    - Valor pago: '{colunas_config['valor_pago']}' {'✅' if colunas_config['valor_pago'] and colunas_config['valor_pago'] in df.columns else '❌'}")
            
            # Sugerir detecção automática se necessário
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
            
            # Encontrar índices das colunas necessárias
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
                    
                    # Extrair dados da linha
                    secretaria = linha[idx_secretaria] if idx_secretaria < len(linha) else 'Não informado'
                    valor_empenhado_str = linha[idx_empenhada] if idx_empenhada < len(linha) else '0'
                    valor_pago_str = linha[idx_paga] if idx_paga < len(linha) else '0'
                    
                    # Converter valores para números
                    try:
                        valor_empenhado = float(valor_empenhado_str.replace(',', '.')) if valor_empenhado_str and valor_empenhado_str != '' else 0
                    except (ValueError, AttributeError):
                        valor_empenhado = 0
                        
                    try:
                        valor_pago = float(valor_pago_str.replace(',', '.')) if valor_pago_str and valor_pago_str != '' else 0
                    except (ValueError, AttributeError):
                        valor_pago = 0
                    
                    # Priorizar valor empenhado, usar valor pago como fallback
                    if valor_empenhado > 0:
                        valor_final = valor_empenhado
                        contador_empenhado += 1
                    elif valor_pago > 0:
                        valor_final = valor_pago
                        contador_pago += 1
                    else:
                        valor_final = None
                    
                    # Adicionar apenas se houver valor válido
                    if valor_final is not None and valor_final > 0:
                        # Mapear categoria padronizada
                        categoria = mapear_categoria_padronizada(secretaria)
                        
                        # Data padrão para 2024
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
            
            # Inserir no banco
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

if __name__ == "__main__":
    print("🔍 Verificando banco de dados...")
    if verificar_banco():
        print("\n🚀 Iniciando processamento dos dados de todos os estados...")
        processar_todos_estados()
    else:
        print("❌ Erro ao acessar o banco de dados.")
        
    # Uncomment the line below to analyze CSV structures instead of processing
    # analisar_todos_csvs()
