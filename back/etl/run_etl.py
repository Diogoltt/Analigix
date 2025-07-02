"""
Sistema de importação e processamento de dados de transparência de todos os estados brasileiros.
Refatorado em módulos para melhor organização e manutenibilidade.
"""

import pandas as pd
import glob
import os
import sys
from datetime import datetime

# Adicionar o diretório atual ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports dos módulos criados
from config.mapeamento_estados import MAPEAMENTO_COLUNAS
from core.categorizador import mapear_categoria_padronizada, limpar_caracteres_especiais
from core.utils import detectar_colunas_csv, obter_valor_coluna, carregar_csv_com_encoding
from core.database import verificar_banco, salvar_dados


# Configurações globais
NOME_BANCO = os.path.join('..', 'database', 'despesas_brasil.db')
NOME_TABELA = 'despesas'


def processar_estado(sigla_estado):
    """
    Processa o CSV de um estado específico.
    """
    if sigla_estado not in MAPEAMENTO_COLUNAS:
        print(f"❌ Estado {sigla_estado} não configurado no mapeamento.")
        return 0
    
    config = MAPEAMENTO_COLUNAS[sigla_estado]
    
    # Buscar arquivo CSV
    arquivos = glob.glob(config['arquivo'])
    if not arquivos:
        print(f"❌ Arquivo não encontrado para {sigla_estado} (padrão: {config['arquivo']})")
        return 0
    
    arquivo = arquivos[0]
    print(f"📁 Processando {sigla_estado}: {arquivo}")
    
    # Processadores especiais para estados específicos
    if sigla_estado == 'RO':
        from processadores.especiais import processar_rondonia_csv_reader
        return processar_rondonia_csv_reader(arquivo, NOME_BANCO, NOME_TABELA)
    
    if sigla_estado == 'RS':
        from processadores.especiais import processar_rs_csv_reader
        return processar_rs_csv_reader(arquivo, NOME_BANCO, NOME_TABELA)
    
    try:        
        # Carregar CSV com tratamento de encoding
        df = carregar_csv_com_encoding(arquivo)
        print(f"  ✅ CSV carregado. Total de linhas: {len(df)}")
        print(f"  📋 Colunas no CSV: {list(df.columns)}")
        
        # Configurar mapeamento de colunas
        colunas = config['colunas'].copy()
        colunas = _configurar_colunas(df, colunas, sigla_estado)
        
        # Processar dados linha por linha
        dados_processados = _processar_linhas_csv(df, colunas, sigla_estado)
        
        # Salvar no banco
        if dados_processados:
            registros_inseridos = salvar_dados(dados_processados, NOME_BANCO, NOME_TABELA)
            print(f"  ✅ {registros_inseridos} registros inseridos para {sigla_estado}")
            return registros_inseridos
        else:
            print(f"  ⚠️  Nenhum dado válido encontrado para {sigla_estado}")
            return 0
            
    except Exception as e:
        print(f"  ❌ Erro ao processar {sigla_estado}: {e}")
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


def _processar_linhas_csv(df, colunas, sigla_estado):
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
            
            # Criar registro
            data = datetime(2024, 1, 1).date()
            
            dados_processados.append({
                'estado': sigla_estado,
                'data': data,
                'orgao': orgao,
                'categoria_padronizada': categoria,
                'valor': valor_final
            })
    
    print(f"  📊 Valores empenhados: {contador_empenhado}, Valores pagos: {contador_pago}")
    return dados_processados


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
            # Carregar CSV
            df = carregar_csv_com_encoding(arquivo)
            
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


if __name__ == "__main__":
    print("🔍 Verificando banco de dados...")
    if verificar_banco(NOME_BANCO, NOME_TABELA):
        print("\n🚀 Iniciando processamento dos dados de todos os estados...")
        processar_todos_estados()
    else:
        print("❌ Erro ao acessar o banco de dados.")
