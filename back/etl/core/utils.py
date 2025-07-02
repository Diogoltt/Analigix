"""
Utilitários para detecção automática de colunas em CSVs e manipulação de dados.
"""

import pandas as pd


def detectar_colunas_csv(df, sigla_estado):
    """
    Detecta e sugere as colunas corretas baseado no conteúdo do CSV.
    """
    colunas_disponiveis = list(df.columns)
    print(f"  🔍 Detectando colunas para {sigla_estado}...")
    
    # Detectar possíveis colunas de órgão
    possiveis_orgao = []
    for col in colunas_disponiveis:
        col_lower = col.lower()
        if any(palavra in col_lower for palavra in ['orgao', 'órgão', 'organ', 'secretaria', 'unidade', 'gestora', 'função', 'funcao', 'ação', 'acao', 'descricao', 'descrição']):
            possiveis_orgao.append(col)
    
    # Detectar possíveis colunas de valores
    possiveis_empenhado = []
    possiveis_pago = []
    
    for col in colunas_disponiveis:
        col_lower = col.lower()
        if any(palavra in col_lower for palavra in ['empenhado', 'empenho']):
            possiveis_empenhado.append(col)
        elif any(palavra in col_lower for palavra in ['pago', 'pagamento', 'valor final', 'valor pago', 'vlpago']):
            possiveis_pago.append(col)
        elif 'valor' in col_lower and 'empenhado' not in col_lower and 'pago' not in col_lower:
            # Verificar o conteúdo para decidir se é empenhado ou pago
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
        
        # Se for string, fazer limpeza
        if isinstance(valor, str):
            # Remover símbolos de moeda e espaços
            valor = valor.strip().replace('R$', '').replace('$', '').replace(' ', '')
            
            # Tratar separadores decimais diferentes
            if ',' in valor and '.' in valor:
                # Formato brasileiro: 1.234.567,89
                valor = valor.replace('.', '').replace(',', '.')
            elif ',' in valor and '.' not in valor:
                # Formato com vírgula decimal: 1234567,89
                valor = valor.replace(',', '.')
            
            # Converter para float
            try:
                valor = float(valor)
            except ValueError:
                return None
        else:
            valor = float(valor)
            
        return valor if valor > 0 else None
    except (KeyError, ValueError, TypeError):
        return None


def carregar_csv_com_encoding(arquivo):
    """
    Carrega um CSV tentando diferentes encodings e separadores.
    """
    df = None
    
    # Primeira tentativa: UTF-8
    try:
        df = pd.read_csv(arquivo, encoding='utf-8', on_bad_lines='skip')
        # Verificar se precisa de separador diferente
        if len(df.columns) == 1 and ';' in df.columns[0]:
            df = pd.read_csv(arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
    except UnicodeDecodeError:
        # Segunda tentativa: Latin-1
        try:
            df = pd.read_csv(arquivo, encoding='latin-1', on_bad_lines='skip')
            # Verificar se precisa de separador diferente
            if len(df.columns) == 1 and ';' in df.columns[0]:
                df = pd.read_csv(arquivo, encoding='latin-1', sep=';', on_bad_lines='skip')
        except:
            # Terceira tentativa: forçar separador
            try:
                df = pd.read_csv(arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
            except:
                df = pd.read_csv(arquivo, encoding='latin-1', sep=';', on_bad_lines='skip')
    except:
        # Fallback: tentar com separador ponto e vírgula
        try:
            df = pd.read_csv(arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
        except:
            df = pd.read_csv(arquivo, encoding='latin-1', sep=';', on_bad_lines='skip')
    
    return df
