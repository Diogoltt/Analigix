"""
Processadores especiais para estados que requerem tratamento específico.
"""

import csv
import pandas as pd
import os
import sys
from datetime import datetime

# Adicionar path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.categorizador import mapear_categoria_padronizada, limpar_caracteres_especiais


def processar_rondonia_csv_reader(arquivo, nome_banco, nome_tabela):
    """
    Processa especificamente o CSV de Rondônia usando csv.reader para evitar problemas de parsing.
    """
    print(f"  🔧 Processamento especial para Rondônia usando csv.reader")
    
    try:
        dados_processados = []
        
        with open(arquivo, encoding="utf-8") as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            cabecalho = next(leitor)
            
            # Localizar índices das colunas
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
                    
                    # Converter valores
                    try:
                        valor_empenhado = float(valor_empenhado_str.replace(',', '.')) if valor_empenhado_str and valor_empenhado_str != '' else 0
                    except (ValueError, AttributeError):
                        valor_empenhado = 0
                        
                    try:
                        valor_pago = float(valor_pago_str.replace(',', '.')) if valor_pago_str and valor_pago_str != '' else 0
                    except (ValueError, AttributeError):
                        valor_pago = 0
                    
                    # Determinar valor final
                    if valor_empenhado > 0:
                        valor_final = valor_empenhado
                        contador_empenhado += 1
                    elif valor_pago > 0:
                        valor_final = valor_pago
                        contador_pago += 1
                    else:
                        valor_final = None
                    
                    # Processar apenas se há valor válido
                    if valor_final is not None and valor_final > 0:
                        # Categorizar
                        categoria = mapear_categoria_padronizada(secretaria)
                        
                        # Criar registro
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
            
            # Salvar no banco
            if dados_processados:
                import sqlite3
                df_final = pd.DataFrame(dados_processados)
                conn = sqlite3.connect(nome_banco)
                df_final.to_sql(nome_tabela, conn, if_exists='append', index=False)
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


def processar_rs_csv_reader(arquivo, nome_banco, nome_tabela):
    """
    Processa especificamente o CSV do Rio Grande do Sul filtrando apenas dados de 2024.
    """
    print(f"  🔧 Processamento especial para RS filtrando ano 2024")
    
    try:
        dados_processados = []
        
        with open(arquivo, encoding="utf-8") as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            cabecalho = next(leitor)
            
            # Limpar BOM do cabeçalho
            cabecalho = [col.strip().replace('\ufeff', '') for col in cabecalho]
            
            # Localizar índices das colunas
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
                    
                    # Extrair dados da linha
                    ano = linha[idx_ano] if idx_ano < len(linha) else ''
                    orgao = linha[idx_orgao] if idx_orgao < len(linha) else 'Não informado'
                    valor_str = linha[idx_valor] if idx_valor < len(linha) else '0'
                    fase_gasto = linha[idx_fase] if idx_fase < len(linha) else ''
                    
                    # Filtrar apenas 2024
                    if ano != '2024':
                        continue
                    
                    contador_2024 += 1
                    
                    # Limpar órgão
                    orgao_limpo = limpar_caracteres_especiais(orgao)
                    
                    # Converter valor
                    try:
                        # Limpar valor
                        valor_limpo = valor_str.replace('R$', '').replace(' ', '').strip()
                        if ',' in valor_limpo and '.' in valor_limpo:
                            # Formato brasileiro: 1.234.567,89
                            valor_limpo = valor_limpo.replace('.', '').replace(',', '.')
                        elif ',' in valor_limpo and '.' not in valor_limpo:
                            # Formato com vírgula decimal: 1234567,89
                            valor_limpo = valor_limpo.replace(',', '.')
                        
                        valor = float(valor_limpo) if valor_limpo else 0
                    except (ValueError, AttributeError):
                        valor = 0
                    
                    # Contar tipos de despesa
                    if 'empenhado' in fase_gasto.lower():
                        contador_empenhado += 1
                    elif 'pago' in fase_gasto.lower():
                        contador_pago += 1
                    
                    # Processar apenas se há valor válido
                    if valor > 0:
                        # Categorizar
                        categoria = mapear_categoria_padronizada(orgao_limpo)
                        
                        # Criar registro
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
            
            # Salvar no banco
            if dados_processados:
                import sqlite3
                df_final = pd.DataFrame(dados_processados)
                conn = sqlite3.connect(nome_banco)
                df_final.to_sql(nome_tabela, conn, if_exists='append', index=False)
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
