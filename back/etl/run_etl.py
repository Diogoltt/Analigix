"""
Sistema de importação e processamento de dados de transparência de todos os estados brasileiros.
Refatorado em módulos para melhor organização e manutenibilidade.
"""

import pandas as pd
import glob
import os
import sys
import re
from datetime import datetime

# Adicionar o diretório atual ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports dos módulos criados
from config.mapeamento_estados import MAPEAMENTO_COLUNAS
from core.categorizador import mapear_categoria_padronizada, limpar_caracteres_especiais
from core.utils import detectar_colunas_csv, obter_valor_coluna, carregar_csv_com_encoding
from core.database import verificar_banco, salvar_dados


# Configurações globais
NOME_BANCO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'despesas_brasil.db'))
NOME_TABELA = 'despesas'
ANOS_SUPORTADOS = [2020, 2021, 2022, 2023, 2024, 2025]


def extrair_ano_do_arquivo(nome_arquivo):
    """
    Extrai o ano do nome do arquivo baseado no padrão SIGLA_ANO.csv
    """
    basename = os.path.basename(nome_arquivo)
    match = re.search(r'_(\d{4})\.csv$', basename)
    if match:
        ano = int(match.group(1))
        if ano in ANOS_SUPORTADOS:
            return ano
    return None


def buscar_arquivos_estado(sigla_estado, ano=None):
    """
    Busca arquivos CSV para um estado específico e opcionalmente um ano específico.
    """
    # Obter caminho absoluto da pasta csvs
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_csvs = os.path.join(script_dir, '..', 'csvs')
    pasta_csvs = os.path.abspath(pasta_csvs)  # Resolver caminho absoluto
    
    if ano:
        # Buscar arquivo específico: SIGLA_ANO.csv
        padrao = os.path.join(pasta_csvs, f"{sigla_estado}_{ano}.csv")
        arquivos = glob.glob(padrao)
    else:
        # Buscar todos os arquivos do estado: SIGLA_*.csv
        padrao = os.path.join(pasta_csvs, f"{sigla_estado}_*.csv")
        arquivos = glob.glob(padrao)
        # Filtrar apenas arquivos com anos válidos
        arquivos = [arq for arq in arquivos if extrair_ano_do_arquivo(arq) is not None]
    
    return sorted(arquivos)


def processar_estado(sigla_estado, ano=None):
    """
    Processa o CSV de um estado específico, opcionalmente para um ano específico.
    """
    if sigla_estado not in MAPEAMENTO_COLUNAS:
        print(f"❌ Estado {sigla_estado} não configurado no mapeamento.")
        return 0
    
    config = MAPEAMENTO_COLUNAS[sigla_estado]
    
    # Buscar arquivos CSV usando o novo padrão
    arquivos = buscar_arquivos_estado(sigla_estado, ano)
    
    if not arquivos:
        if ano:
            print(f"❌ Arquivo não encontrado para {sigla_estado} do ano {ano} (padrão: {sigla_estado}_{ano}.csv)")
        else:
            print(f"❌ Nenhum arquivo encontrado para {sigla_estado} (padrão: {sigla_estado}_YYYY.csv)")
        return 0
    
    total_registros = 0
    
    # Processar cada arquivo encontrado
    for arquivo in arquivos:
        ano_arquivo = extrair_ano_do_arquivo(arquivo)
        if ano_arquivo is None:
            print(f"⚠️  Pulando arquivo {arquivo} - ano não identificado")
            continue
            
        print(f"📁 Processando {sigla_estado} ({ano_arquivo}): {arquivo}")
        registros = _processar_arquivo_csv(arquivo, sigla_estado, ano_arquivo, config)
        total_registros += registros
        print(f"  ✅ {registros} registros inseridos para {sigla_estado} ({ano_arquivo})")
        print("-" * 40)
    
    return total_registros


def _processar_arquivo_csv(arquivo, sigla_estado, ano, config):
    """
    Processa um arquivo CSV específico.
    """
    # Processadores especiais para estados específicos
    if sigla_estado == 'RO':
        from processadores.especiais import processar_rondonia_csv_reader
        return processar_rondonia_csv_reader(arquivo, NOME_BANCO, NOME_TABELA, ano)
    
    if sigla_estado == 'RS':
        from processadores.especiais import processar_rs_csv_reader
        return processar_rs_csv_reader(arquivo, NOME_BANCO, NOME_TABELA, ano)
    
    if sigla_estado == 'DF':
        from processadores.especiais import processar_df_csv_reader
        return processar_df_csv_reader(arquivo, NOME_BANCO, NOME_TABELA, ano)
    
    if sigla_estado == 'MA':
        from processadores.especiais import processar_ma_csv_reader
        return processar_ma_csv_reader(arquivo, NOME_BANCO, NOME_TABELA, ano)
    
    if sigla_estado == 'GO':
        from processadores.especiais import processar_goias_csv_reader
        return processar_goias_csv_reader(arquivo, NOME_BANCO, NOME_TABELA, ano)
    
    if sigla_estado == 'MS':
        from processadores.especiais import processar_ms_csv_especial
        return processar_ms_csv_especial(arquivo, NOME_BANCO, NOME_TABELA, ano)
    
    if sigla_estado == 'RJ':
        from processadores.especiais import processar_rj_csv_especial
        return processar_rj_csv_especial(arquivo, NOME_BANCO, NOME_TABELA, ano)
    
    if sigla_estado == 'SP':
        from processadores.especiais import processar_sp_csv_especial
        return processar_sp_csv_especial(arquivo, NOME_BANCO, NOME_TABELA, ano)
    
    try:        
        # Carregar CSV com tratamento de encoding
        df = carregar_csv_com_encoding(arquivo)
        print(f"  ✅ CSV carregado. Total de linhas: {len(df)}")
        print(f"  📋 Colunas no CSV: {list(df.columns)}")
        
        # Configurar mapeamento de colunas
        colunas = config['colunas'].copy()
        colunas = _configurar_colunas(df, colunas, sigla_estado)
        
        # Processar dados linha por linha
        dados_processados = _processar_linhas_csv(df, colunas, sigla_estado, ano)
        
        # Salvar no banco
        if dados_processados:
            registros_inseridos = salvar_dados(dados_processados, NOME_BANCO, NOME_TABELA)
            return registros_inseridos
        else:
            print(f"  ⚠️  Nenhum dado válido encontrado para {sigla_estado} ({ano})")
            return 0
            
    except Exception as e:
        print(f"  ❌ Erro ao processar {sigla_estado} ({ano}): {e}")
        return 0


def _configurar_colunas(df, colunas, sigla_estado):
    """
    Configura o mapeamento de colunas, detectando automaticamente quando necessário.
    """
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
    
    # Detecção completa se ainda não temos colunas válidas
    if not colunas['orgao'] or (not colunas['valor_empenhado'] and not colunas['valor_pago']):
        print(f"  🔍 Detectando todas as colunas automaticamente para {sigla_estado}...")
        colunas_auto = detectar_colunas_csv(df, sigla_estado)
        if colunas_auto['orgao']:
            colunas['orgao'] = colunas_auto['orgao']
        if colunas_auto['valor_empenhado']:
            colunas['valor_empenhado'] = colunas_auto['valor_empenhado']
        if colunas_auto['valor_pago']:
            colunas['valor_pago'] = colunas_auto['valor_pago']
    
    # Mostrar configuração final
    print(f"  📊 Colunas que serão usadas:")
    print(f"    - Órgão: '{colunas['orgao']}'")
    print(f"    - Valor empenhado: '{colunas['valor_empenhado']}'")
    print(f"    - Valor pago: '{colunas['valor_pago']}'")
    
    return colunas


def _processar_linhas_csv(df, colunas, sigla_estado, ano):
    """
    Processa as linhas do CSV e extrai os dados necessários.
    """
    dados_processados = []
    contador_empenhado = 0
    contador_pago = 0
    
    for _, row in df.iterrows():
        # Extrair nome do órgão
        orgao_raw = row[colunas['orgao']] if colunas['orgao'] and colunas['orgao'] in row.index and pd.notna(row[colunas['orgao']]) else None
        
        if orgao_raw is not None:
            orgao = limpar_caracteres_especiais(str(orgao_raw))
        else:
            orgao = 'Não informado'
        
        # Extrair valores
        valor_empenhado = obter_valor_coluna(row, colunas['valor_empenhado'])
        valor_pago = obter_valor_coluna(row, colunas['valor_pago'])
        
        # Determinar valor final (prioridade para empenhado)
        if valor_empenhado is not None:
            valor_final = valor_empenhado
            contador_empenhado += 1
        elif valor_pago is not None:
            valor_final = valor_pago
            contador_pago += 1
        else:
            valor_final = None
        
        # Processar apenas registros com valor válido
        if valor_final is not None and valor_final > 0:
            # Categorizar despesa
            categoria = mapear_categoria_padronizada(orgao)
            
            # Criar data baseada no ano do arquivo
            data = datetime(ano, 1, 1).date()
            
            dados_processados.append({
                'estado': sigla_estado,
                'data': data,
                'orgao': orgao,
                'categoria_padronizada': categoria,
                'valor': valor_final
            })
    
    print(f"  📊 Valores empenhados: {contador_empenhado}, Valores pagos: {contador_pago}")
    return dados_processados


def processar_todos_estados(ano=None):
    """
    Processa todos os estados disponíveis, opcionalmente para um ano específico.
    """
    if ano:
        print(f"🚀 Iniciando processamento de todos os estados para o ano {ano}...")
    else:
        print("🚀 Iniciando processamento de todos os estados (todos os anos)...")
    print("="*60)
    
    total_registros = 0
    estados_processados = 0
    
    for sigla_estado in MAPEAMENTO_COLUNAS.keys():
        registros = processar_estado(sigla_estado, ano)
        if registros > 0:
            total_registros += registros
            estados_processados += 1
        print("-" * 60)
    
    print(f"\n🎉 RESUMO FINAL:")
    print(f"   Estados processados: {estados_processados}")
    print(f"   Total de registros inseridos: {total_registros}")


def processar_arquivo_especifico(sigla_estado, ano):
    """
    Processa um arquivo específico baseado no estado e ano.
    Função útil para quando um novo arquivo é enviado pelo frontend.
    """
    print(f"🚀 Processando arquivo específico: {sigla_estado}_{ano}.csv")
    print("="*50)
    
    if ano not in ANOS_SUPORTADOS:
        print(f"❌ Ano {ano} não é suportado. Anos válidos: {ANOS_SUPORTADOS}")
        return 0
    
    registros = processar_estado(sigla_estado, ano)
    
    if registros > 0:
        print(f"\n🎉 Processamento concluído:")
        print(f"   Estado: {sigla_estado}")
        print(f"   Ano: {ano}")
        print(f"   Registros inseridos: {registros}")
    else:
        print(f"\n⚠️  Nenhum registro foi processado para {sigla_estado} ({ano})")
    
    return registros


def analisar_todos_csvs():
    """
    Analisa a estrutura de todos os CSVs disponíveis para verificar os mapeamentos.
    """
    print("🔍 ANALISANDO ESTRUTURA DE TODOS OS CSVs...")
    print("="*80)
    
    pasta_csvs = os.path.join('..', 'csvs')
    
    for sigla_estado, config in MAPEAMENTO_COLUNAS.items():
        # Buscar todos os arquivos do estado usando o novo padrão
        arquivos = buscar_arquivos_estado(sigla_estado)
        
        if not arquivos:
            print(f"❌ {sigla_estado}: Nenhum arquivo encontrado (padrão: {sigla_estado}_YYYY.csv)")
            continue
        
        print(f"\n📁 {sigla_estado}: {len(arquivos)} arquivo(s) encontrado(s)")
        
        for arquivo in arquivos:
            ano_arquivo = extrair_ano_do_arquivo(arquivo)
            print(f"  � {os.path.basename(arquivo)} (ano: {ano_arquivo})")
            
            try:
                # Carregar CSV
                df = carregar_csv_com_encoding(arquivo)
                
                print(f"    📋 Colunas disponíveis: {list(df.columns)}")
                print(f"    📊 Total de linhas: {len(df)}")
                
                # Verificar mapeamento atual
                colunas_config = config['colunas']
                print(f"    🗺️  Mapeamento atual:")
                print(f"      - Órgão: '{colunas_config['orgao']}' {'✅' if colunas_config['orgao'] in df.columns else '❌'}")
                print(f"      - Valor empenhado: '{colunas_config['valor_empenhado']}' {'✅' if colunas_config['valor_empenhado'] and colunas_config['valor_empenhado'] in df.columns else '❌'}")
                print(f"      - Valor pago: '{colunas_config['valor_pago']}' {'✅' if colunas_config['valor_pago'] and colunas_config['valor_pago'] in df.columns else '❌'}")
                
                # Sugerir detecção automática se necessário
                if (not colunas_config['orgao'] or colunas_config['orgao'] not in df.columns or
                    (colunas_config['valor_empenhado'] and colunas_config['valor_empenhado'] not in df.columns) or
                    (colunas_config['valor_pago'] and colunas_config['valor_pago'] not in df.columns)):
                    print(f"    🔍 Sugestões de detecção automática:")
                    colunas_auto = detectar_colunas_csv(df, sigla_estado)
                    if colunas_auto['orgao']:
                        print(f"      - Órgão: '{colunas_auto['orgao']}'")
                    if colunas_auto['valor_empenhado']:
                        print(f"      - Valor empenhado: '{colunas_auto['valor_empenhado']}'")
                    if colunas_auto['valor_pago']:
                        print(f"      - Valor pago: '{colunas_auto['valor_pago']}'")
            
            except Exception as e:
                print(f"    ❌ Erro ao analisar: {e}")
            
            print("    " + "-" * 40)
        
        print("-" * 80)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Processamento de dados de transparência')
    parser.add_argument('--estado', type=str, help='Sigla do estado para processar')
    parser.add_argument('--ano', type=int, help='Ano específico para processar')
    parser.add_argument('--todos', action='store_true', help='Processar todos os estados')
    parser.add_argument('--analisar', action='store_true', help='Analisar estrutura dos CSVs')
    
    args = parser.parse_args()
    
    print("🔍 Verificando banco de dados...")
    if not verificar_banco(NOME_BANCO, NOME_TABELA):
        print("❌ Erro ao acessar o banco de dados.")
        exit(1)
    
    if args.analisar:
        analisar_todos_csvs()
    elif args.estado and args.ano:
        # Processar arquivo específico (útil quando chamado pelo backend após upload)
        processar_arquivo_especifico(args.estado, args.ano)
    elif args.estado:
        # Processar todos os anos de um estado específico
        print(f"\n🚀 Processando todos os arquivos do estado {args.estado}...")
        processar_estado(args.estado)
    elif args.todos:
        # Processar todos os estados
        if args.ano:
            processar_todos_estados(args.ano)
        else:
            processar_todos_estados()
    else:
        # Comportamento padrão: processar todos os estados
        print("\n🚀 Iniciando processamento padrão (todos os estados)...")
        processar_todos_estados()


# Função que pode ser chamada diretamente pelo backend
def processar_novo_arquivo(sigla_estado, ano):
    """
    Função para ser chamada pelo backend quando um novo arquivo é enviado.
    Retorna True se o processamento foi bem-sucedido, False caso contrário.
    """
    try:
        if not verificar_banco(NOME_BANCO, NOME_TABELA):
            print("❌ Erro ao acessar o banco de dados.")
            return False
        
        registros = processar_arquivo_especifico(sigla_estado, ano)
        return registros > 0
    
    except Exception as e:
        print(f"❌ Erro ao processar arquivo {sigla_estado}_{ano}.csv: {e}")
        return False
