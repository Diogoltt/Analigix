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


def processar_rondonia_csv_reader(arquivo, nome_banco, nome_tabela, ano=2024):
    """
    Processa especificamente o CSV de Rondônia usando csv.reader para evitar problemas de parsing.
    """
    print(f"  🔧 Processamento especial para Rondônia usando csv.reader (ano: {ano})")
    
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
                        
                        # Criar registro com ano correto
                        ano_int = int(ano) if isinstance(ano, str) else ano
                        data = datetime(ano_int, 1, 1).date()
                        
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


def processar_rs_csv_reader(arquivo, nome_banco, nome_tabela, ano=2024):
    """
    Processa especificamente o CSV do Rio Grande do Sul filtrando dados do ano especificado.
    """
    print(f"  🔧 Processamento especial para RS filtrando ano {ano}")
    
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
            contador_ano = 0
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
                    
                    # Filtrar apenas o ano especificado
                    if ano != str(ano):
                        continue
                    
                    contador_ano += 1
                    
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
                        
                        # Criar registro com ano correto (converter para int se necessário)
                        ano_int = int(ano) if isinstance(ano, str) else ano
                        data = datetime(ano_int, 1, 1).date()
                        
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
            print(f"    - Registros do ano {ano}: {contador_ano}")
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


def processar_df_csv_reader(arquivo, nome_banco, nome_tabela, ano=2020):
    """
    Processa especificamente o CSV do Distrito Federal que tem título na primeira linha.
    """
    print(f"  🔧 Processamento especial para Distrito Federal (ano: {ano})")
    
    try:
        dados_processados = []
        
        with open(arquivo, encoding="utf-8") as arquivo_csv:
            leitor = csv.reader(arquivo_csv, delimiter=';')
            
            # Pular a primeira linha que contém o título
            next(leitor)  # Linha com "Despesa por Órgão 2020"
            
            # Ler o cabeçalho real
            cabecalho = next(leitor)
            
            # Limpar BOM e espaços do cabeçalho
            cabecalho = [col.strip().replace('\ufeff', '') for col in cabecalho]
            
            # Localizar índices das colunas importantes
            idx_orgao = cabecalho.index("Unidade Gestora")
            idx_empenhado = cabecalho.index("Empenhado")
            idx_liquidado = cabecalho.index("Liquidado")
            idx_pago = cabecalho.index("Total Pago")
            
            print(f"  📋 Colunas encontradas:")
            print(f"    - Unidade Gestora (índice {idx_orgao})")
            print(f"    - Empenhado (índice {idx_empenhado})")
            print(f"    - Liquidado (índice {idx_liquidado})")
            print(f"    - Total Pago (índice {idx_pago})")
            
            contador_empenhado = 0
            contador_liquidado = 0
            contador_pago = 0
            linhas_processadas = 0
            
            for linha in leitor:
                try:
                    linhas_processadas += 1
                    
                    # Extrair dados da linha
                    orgao = linha[idx_orgao] if idx_orgao < len(linha) else 'Não informado'
                    valor_empenhado_str = linha[idx_empenhado] if idx_empenhado < len(linha) else '0'
                    valor_liquidado_str = linha[idx_liquidado] if idx_liquidado < len(linha) else '0'
                    valor_pago_str = linha[idx_pago] if idx_pago < len(linha) else '0'
                    
                    # Função para limpar valores monetários do DF (formato brasileiro)
                    def limpar_valor_df(valor_str):
                        if not valor_str or valor_str.strip() == '':
                            return 0
                        try:
                            # Remover aspas e espaços
                            valor_limpo = valor_str.replace('"', '').strip()
                            # Converter formato brasileiro: 1.234.567,89 -> 1234567.89
                            if ',' in valor_limpo and '.' in valor_limpo:
                                # Formato: 1.234.567,89
                                valor_limpo = valor_limpo.replace('.', '').replace(',', '.')
                            elif ',' in valor_limpo:
                                # Formato: 1234567,89
                                valor_limpo = valor_limpo.replace(',', '.')
                            
                            return float(valor_limpo) if valor_limpo else 0
                        except (ValueError, AttributeError):
                            return 0
                    
                    # Converter valores
                    valor_empenhado = limpar_valor_df(valor_empenhado_str)
                    valor_liquidado = limpar_valor_df(valor_liquidado_str)
                    valor_pago = limpar_valor_df(valor_pago_str)
                    
                    # Determinar valor final - priorizar empenhado, depois liquidado, depois pago
                    valor_final = None
                    tipo_valor = None
                    
                    if valor_empenhado > 0:
                        valor_final = valor_empenhado
                        tipo_valor = 'empenhado'
                        contador_empenhado += 1
                    elif valor_liquidado > 0:
                        valor_final = valor_liquidado
                        tipo_valor = 'liquidado'
                        contador_liquidado += 1
                    elif valor_pago > 0:
                        valor_final = valor_pago
                        tipo_valor = 'pago'
                        contador_pago += 1
                    
                    # Processar apenas se há valor válido
                    if valor_final is not None and valor_final > 0:
                        # Limpar e categorizar órgão
                        orgao_limpo = limpar_caracteres_especiais(orgao.replace('"', ''))
                        categoria = mapear_categoria_padronizada(orgao_limpo)
                        
                        # Criar registro
                        ano_int = int(ano) if isinstance(ano, str) else ano
                        data = datetime(ano_int, 1, 1).date()
                        
                        dados_processados.append({
                            'estado': 'DF',
                            'data': data,
                            'orgao': orgao_limpo,
                            'categoria_padronizada': categoria,
                            'valor': valor_final
                        })
                        
                except (IndexError, ValueError) as e:
                    print(f"  ⚠️  Erro na linha {linhas_processadas}: {e}")
                    continue
            
            print(f"  📊 Estatísticas de processamento:")
            print(f"    - Linhas processadas: {linhas_processadas}")
            print(f"    - Valores empenhados: {contador_empenhado}")
            print(f"    - Valores liquidados: {contador_liquidado}")
            print(f"    - Valores pagos: {contador_pago}")
            print(f"    - Registros válidos: {len(dados_processados)}")
            
            # Salvar no banco
            if dados_processados:
                import sqlite3
                df_final = pd.DataFrame(dados_processados)
                conn = sqlite3.connect(nome_banco)
                df_final.to_sql(nome_tabela, conn, if_exists='append', index=False)
                conn.commit()
                conn.close()
                
                print(f"  ✅ {len(df_final)} registros inseridos para DF")
                return len(df_final)
            else:
                print(f"  ⚠️  Nenhum dado válido encontrado para DF")
                return 0
                
    except Exception as e:
        print(f"  ❌ Erro ao processar DF: {e}")
        import traceback
        traceback.print_exc()
        return 0


def processar_goias_csv_reader(arquivo, nome_banco, nome_tabela, ano_solicitado=2024):
    """
    Processa especificamente o CSV de Goiás filtrando dados do ano especificado.
    """
    print(f"  🔧 Processamento especial para GO filtrando ano {ano_solicitado}")
    
    try:
        dados_processados = []
        
        with open(arquivo, encoding="utf-8") as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            cabecalho = next(leitor)
            
            # Limpar BOM do cabeçalho se existir
            cabecalho = [col.strip().replace('\ufeff', '') for col in cabecalho]
            
            # Localizar índices das colunas
            idx_ano = cabecalho.index("View Execucao Orcamentaria Visao Geral[Numero Ano]")
            idx_orgao = cabecalho.index("View Execucao Orcamentaria Visao Geral[Nome Orgao]")
            idx_valor_empenhado = cabecalho.index("View Execucao Orcamentaria Visao Geral[Valor Empenho]")
            idx_valor_pago = cabecalho.index("View Execucao Orcamentaria Visao Geral[Valor Pago]")
            
            print(f"  📋 Colunas encontradas:")
            print(f"    - Ano (índice {idx_ano})")
            print(f"    - Órgão (índice {idx_orgao})")
            print(f"    - Valor Empenhado (índice {idx_valor_empenhado})")
            print(f"    - Valor Pago (índice {idx_valor_pago})")
            
            contador_total = 0
            contador_ano = 0
            contador_empenhado = 0
            contador_pago = 0
            linhas_processadas = 0
            
            for linha in leitor:
                try:
                    linhas_processadas += 1
                    contador_total += 1
                    
                    # Extrair dados da linha
                    ano_linha = linha[idx_ano] if idx_ano < len(linha) else ''
                    orgao = linha[idx_orgao] if idx_orgao < len(linha) else 'Não informado'
                    valor_empenhado_str = linha[idx_valor_empenhado] if idx_valor_empenhado < len(linha) else '0'
                    valor_pago_str = linha[idx_valor_pago] if idx_valor_pago < len(linha) else '0'
                    
                    # Filtrar apenas o ano especificado
                    if ano_linha != str(ano_solicitado):
                        continue
                    
                    contador_ano += 1
                    
                    # Limpar órgão
                    orgao_limpo = limpar_caracteres_especiais(orgao)
                    
                    # Converter valores
                    try:
                        valor_empenhado = float(valor_empenhado_str) if valor_empenhado_str and valor_empenhado_str != '' else 0
                    except (ValueError, AttributeError):
                        valor_empenhado = 0
                    
                    try:
                        valor_pago = float(valor_pago_str) if valor_pago_str and valor_pago_str != '' else 0
                    except (ValueError, AttributeError):
                        valor_pago = 0
                    
                    # Determinar valor final (prioridade para empenhado)
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
                        categoria = mapear_categoria_padronizada(orgao_limpo)
                        
                        # Criar registro com ano correto
                        data = datetime(ano_solicitado, 1, 1).date()
                        
                        dados_processados.append({
                            'estado': 'GO',
                            'data': data,
                            'orgao': orgao_limpo,
                            'categoria_padronizada': categoria,
                            'valor': valor_final
                        })
                        
                except (IndexError, ValueError) as e:
                    print(f"  ⚠️  Erro na linha {linhas_processadas}: {e}")
                    continue
            
            print(f"  📊 Estatísticas de processamento:")
            print(f"    - Total de linhas processadas: {linhas_processadas}")
            print(f"    - Registros totais no arquivo: {contador_total}")
            print(f"    - Registros do ano {ano_solicitado}: {contador_ano}")
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
                
                print(f"  ✅ {len(df_final)} registros de {ano_solicitado} inseridos para GO")
                return len(df_final)
            else:
                print(f"  ⚠️  Nenhum dado válido de {ano_solicitado} encontrado para GO")
                return 0
                
    except Exception as e:
        print(f"  ❌ Erro ao processar GO: {e}")
        import traceback
        traceback.print_exc()
        return 0


def processar_ma_csv_reader(arquivo, nome_banco, nome_tabela, ano=2024):
    """
    Processa especificamente o CSV do Maranhão que tem linhas inúteis no final.
    """
    print(f"  🔧 Processamento especial para Maranhão (ano: {ano})")
    
    try:
        dados_processados = []
        
        with open(arquivo, encoding="utf-8") as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            
            # Ler o cabeçalho
            cabecalho = next(leitor)
            
            # Limpar BOM e aspas do cabeçalho
            cabecalho = [col.strip().replace('\ufeff', '').replace('"', '') for col in cabecalho]
            
            # Localizar índices das colunas importantes
            idx_ano = cabecalho.index("Ano")
            idx_codigo = cabecalho.index("Código")
            idx_descricao = cabecalho.index("Descrição")
            idx_empenhado = cabecalho.index("Empenhado")
            idx_liquidado = cabecalho.index("Liquidado")
            idx_pago = cabecalho.index("Pago")
            
            print(f"  📋 Colunas encontradas:")
            print(f"    - Ano (índice {idx_ano})")
            print(f"    - Código (índice {idx_codigo})")
            print(f"    - Descrição (índice {idx_descricao})")
            print(f"    - Empenhado (índice {idx_empenhado})")
            print(f"    - Liquidado (índice {idx_liquidado})")
            print(f"    - Pago (índice {idx_pago})")
            
            contador_empenhado = 0
            contador_liquidado = 0
            contador_pago = 0
            linhas_processadas = 0
            linhas_validas = 0
            
            # Ler todas as linhas primeiro para poder ignorar as últimas
            todas_linhas = list(leitor)
            
            # Processar todas as linhas exceto as últimas 3
            for linha in todas_linhas[:-3]:
                try:
                    linhas_processadas += 1
                    
                    # Extrair dados da linha removendo aspas
                    ano_linha = linha[idx_ano].replace('"', '') if idx_ano < len(linha) else ''
                    codigo = linha[idx_codigo].replace('"', '') if idx_codigo < len(linha) else ''
                    descricao = linha[idx_descricao].replace('"', '') if idx_descricao < len(linha) else 'Não informado'
                    valor_empenhado_str = linha[idx_empenhado].replace('"', '') if idx_empenhado < len(linha) else '0'
                    valor_liquidado_str = linha[idx_liquidado].replace('"', '') if idx_liquidado < len(linha) else '0'
                    valor_pago_str = linha[idx_pago].replace('"', '') if idx_pago < len(linha) else '0'
                    
                    # Filtrar apenas o ano especificado e linhas com dados válidos
                    if not ano_linha or ano_linha != str(ano) or not codigo or not descricao:
                        continue
                    
                    linhas_validas += 1
                    
                    # Função para limpar valores monetários do MA
                    def limpar_valor_ma(valor_str):
                        if not valor_str or valor_str.strip() == '':
                            return 0
                        try:
                            # Converter ponto decimal direto (formato americano)
                            return float(valor_str) if valor_str else 0
                        except (ValueError, AttributeError):
                            return 0
                    
                    # Converter valores
                    valor_empenhado = limpar_valor_ma(valor_empenhado_str)
                    valor_liquidado = limpar_valor_ma(valor_liquidado_str)
                    valor_pago = limpar_valor_ma(valor_pago_str)
                    
                    # Determinar valor final - priorizar empenhado, depois liquidado, depois pago
                    valor_final = None
                    tipo_valor = None
                    
                    if valor_empenhado > 0:
                        valor_final = valor_empenhado
                        tipo_valor = 'empenhado'
                        contador_empenhado += 1
                    elif valor_liquidado > 0:
                        valor_final = valor_liquidado
                        tipo_valor = 'liquidado'
                        contador_liquidado += 1
                    elif valor_pago > 0:
                        valor_final = valor_pago
                        tipo_valor = 'pago'
                        contador_pago += 1
                    
                    # Processar apenas se há valor válido
                    if valor_final is not None and valor_final > 0:
                        # Limpar e categorizar órgão usando a descrição
                        orgao_limpo = limpar_caracteres_especiais(descricao)
                        categoria = mapear_categoria_padronizada(orgao_limpo)
                        
                        # Criar registro
                        ano_int = int(ano) if isinstance(ano, str) else ano
                        data = datetime(ano_int, 1, 1).date()
                        
                        dados_processados.append({
                            'estado': 'MA',
                            'data': data,
                            'orgao': orgao_limpo,
                            'categoria_padronizada': categoria,
                            'valor': valor_final
                        })
                        
                except (IndexError, ValueError) as e:
                    print(f"  ⚠️  Erro na linha {linhas_processadas}: {e}")
                    continue
            
            print(f"  📊 Estatísticas de processamento:")
            print(f"    - Linhas totais no arquivo: {len(todas_linhas)}")
            print(f"    - Linhas processadas (excluindo 3 últimas): {linhas_processadas}")
            print(f"    - Linhas válidas: {linhas_validas}")
            print(f"    - Valores empenhados: {contador_empenhado}")
            print(f"    - Valores liquidados: {contador_liquidado}")
            print(f"    - Valores pagos: {contador_pago}")
            print(f"    - Registros válidos: {len(dados_processados)}")
            
            # Salvar no banco
            if dados_processados:
                import sqlite3
                df_final = pd.DataFrame(dados_processados)
                conn = sqlite3.connect(nome_banco)
                df_final.to_sql(nome_tabela, conn, if_exists='append', index=False)
                conn.commit()
                conn.close()
                
                print(f"  ✅ {len(df_final)} registros inseridos para MA")
                return len(df_final)
            else:
                print(f"  ⚠️  Nenhum dado válido encontrado para MA")
                return 0
                
    except Exception as e:
        print(f"  ❌ Erro ao processar MA: {e}")
        import traceback
        traceback.print_exc()
        return 0


def processar_ms_csv_especial(arquivo, nome_banco, nome_tabela, ano=2024):
    """
    Processa especificamente o CSV do Mato Grosso do Sul (MS).
    O arquivo tem 4 linhas de texto antes do cabeçalho real.
    """
    print(f"  🔧 Processamento especial para MS - pulando 4 linhas iniciais (ano: {ano})")
    
    try:
        dados_processados = []
        
        # Ler o arquivo pulando as primeiras 4 linhas
        df = pd.read_csv(arquivo, encoding="utf-8", delimiter=";", skiprows=4)
        
        print(f"  📋 Arquivo carregado com {len(df)} linhas após pular as 4 iniciais")
        print(f"  📋 Colunas encontradas: {list(df.columns)}")
        
        # Verificar se as colunas esperadas existem
        colunas_esperadas = ['Unidade Gestora', 'Orgão', 'Empenhado', 'Liquidado', 'Pago']
        colunas_encontradas = list(df.columns)
        
        if not all(col in colunas_encontradas for col in colunas_esperadas):
            print(f"  ⚠️  Colunas esperadas não encontradas. Esperadas: {colunas_esperadas}")
            print(f"  ⚠️  Encontradas: {colunas_encontradas}")
            return 0
        
        linhas_processadas = 0
        linhas_validas = 0
        contador_empenhado = 0
        contador_liquidado = 0
        contador_pago = 0
        
        for index, row in df.iterrows():
            try:
                linhas_processadas += 1
                
                # Extrair dados da linha
                orgao = str(row['Orgão']).strip() if pd.notna(row['Orgão']) else 'Não informado'
                valor_empenhado_str = str(row['Empenhado']) if pd.notna(row['Empenhado']) else '0'
                valor_liquidado_str = str(row['Liquidado']) if pd.notna(row['Liquidado']) else '0'
                valor_pago_str = str(row['Pago']) if pd.notna(row['Pago']) else '0'
                
                # Função para converter valores monetários brasileiros
                def converter_valor_brasileiro(valor_str):
                    try:
                        # Remover aspas e espaços
                        valor_str = valor_str.replace('"', '').strip()
                        
                        # Substituir vírgula por ponto para decimal
                        valor_str = valor_str.replace(',', '.')
                        
                        # Remover pontos de milhares (se houver)
                        # Se tem mais de um ponto, todos exceto o último são separadores de milhares
                        partes = valor_str.split('.')
                        if len(partes) > 2:
                            # Reconstituir: juntar todas as partes exceto a última, depois adicionar a última
                            valor_str = ''.join(partes[:-1]) + '.' + partes[-1]
                        
                        return float(valor_str)
                    except (ValueError, AttributeError):
                        return 0.0
                
                # Converter valores
                valor_empenhado = converter_valor_brasileiro(valor_empenhado_str)
                valor_liquidado = converter_valor_brasileiro(valor_liquidado_str)
                valor_pago = converter_valor_brasileiro(valor_pago_str)
                
                # Usar o maior valor disponível (prioridade: pago > liquidado > empenhado)
                valor_final = None
                tipo_valor = None
                
                if valor_pago > 0:
                    valor_final = valor_pago
                    tipo_valor = "pago"
                    contador_pago += 1
                elif valor_liquidado > 0:
                    valor_final = valor_liquidado
                    tipo_valor = "liquidado"
                    contador_liquidado += 1
                elif valor_empenhado > 0:
                    valor_final = valor_empenhado
                    tipo_valor = "empenhado"
                    contador_empenhado += 1
                
                # Processar apenas se há valor válido
                if valor_final is not None and valor_final > 0:
                    linhas_validas += 1
                    
                    # Limpar e categorizar órgão
                    orgao_limpo = limpar_caracteres_especiais(orgao)
                    categoria = mapear_categoria_padronizada(orgao_limpo)
                    
                    # Criar registro
                    ano_int = int(ano) if isinstance(ano, str) else ano
                    data = datetime(ano_int, 1, 1).date()
                    
                    dados_processados.append({
                        'estado': 'MS',
                        'data': data,
                        'orgao': orgao_limpo,
                        'categoria_padronizada': categoria,
                        'valor': valor_final
                    })
                    
            except Exception as e:
                print(f"  ⚠️  Erro na linha {linhas_processadas}: {e}")
                continue
        
        print(f"  📊 Estatísticas de processamento:")
        print(f"    - Linhas processadas: {linhas_processadas}")
        print(f"    - Linhas válidas: {linhas_validas}")
        print(f"    - Valores empenhados: {contador_empenhado}")
        print(f"    - Valores liquidados: {contador_liquidado}")
        print(f"    - Valores pagos: {contador_pago}")
        print(f"    - Registros válidos: {len(dados_processados)}")
        
        # Salvar no banco
        if dados_processados:
            import sqlite3
            df_final = pd.DataFrame(dados_processados)
            conn = sqlite3.connect(nome_banco)
            df_final.to_sql(nome_tabela, conn, if_exists='append', index=False)
            conn.commit()
            conn.close()
            
            print(f"  ✅ {len(df_final)} registros inseridos para MS")
            return len(df_final)
        else:
            print(f"  ⚠️  Nenhum dado válido encontrado para MS")
            return 0
            
    except Exception as e:
        print(f"  ❌ Erro ao processar MS: {e}")
        import traceback
        traceback.print_exc()
        return 0


def processar_rj_csv_especial(arquivo, nome_banco, nome_tabela, ano=2024):
    """
    Processa especificamente o CSV do Rio de Janeiro (RJ).
    O arquivo tem 15 linhas de texto/cabeçalho antes dos dados reais.
    """
    print(f"  🔧 Processamento especial para RJ - pulando 15 linhas iniciais (ano: {ano})")
    
    try:
        dados_processados = []
        
        # Tentar diferentes encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                print(f"  🔄 Tentando encoding: {encoding}")
                df = pd.read_csv(arquivo, encoding=encoding, delimiter=";", skiprows=15)
                print(f"  ✅ Sucesso com encoding: {encoding}")
                break
            except UnicodeDecodeError:
                print(f"  ❌ Falhou com encoding: {encoding}")
                continue
        
        if df is None:
            print(f"  ❌ Não foi possível ler o arquivo com nenhum dos encodings testados")
            return 0
        
        print(f"  📋 Arquivo carregado com {len(df)} linhas após pular as 15 iniciais")
        print(f"  📋 Colunas encontradas: {list(df.columns)}")
        
        # Verificar se as colunas esperadas existem
        colunas_esperadas = ['Função', 'Valor Empenhado']
        colunas_encontradas = list(df.columns)
        
        # Verificar se pelo menos as colunas principais existem
        if not ('Função' in colunas_encontradas and 'Valor Empenhado' in colunas_encontradas):
            print(f"  ⚠️  Colunas esperadas não encontradas. Esperadas: {colunas_esperadas}")
            print(f"  ⚠️  Encontradas: {colunas_encontradas}")
            return 0
        
        linhas_processadas = 0
        linhas_validas = 0
        contador_empenhado = 0
        
        for index, row in df.iterrows():
            try:
                linhas_processadas += 1
                
                # Extrair dados da linha
                funcao = str(row['Função']).strip() if pd.notna(row['Função']) else 'Não informado'
                valor_empenhado_str = str(row['Valor Empenhado']) if pd.notna(row['Valor Empenhado']) else '0'
                
                # Pular linhas vazias ou inválidas
                if pd.isna(row['Função']) or funcao == 'nan' or funcao == '':
                    continue
                
                # Função para converter valores monetários brasileiros
                def converter_valor_brasileiro(valor_str):
                    try:
                        # Remover espaços e caracteres especiais
                        valor_str = valor_str.strip()
                        
                        # Substituir vírgula por ponto para decimal
                        valor_str = valor_str.replace(',', '.')
                        
                        # Remover pontos de milhares (se houver múltiplos pontos)
                        partes = valor_str.split('.')
                        if len(partes) > 2:
                            # Reconstituir: juntar todas as partes exceto a última, depois adicionar a última
                            valor_str = ''.join(partes[:-1]) + '.' + partes[-1]
                        
                        return float(valor_str)
                    except (ValueError, AttributeError):
                        return 0.0
                
                # Converter valor
                valor_empenhado = converter_valor_brasileiro(valor_empenhado_str)
                
                # Processar apenas se há valor válido
                if valor_empenhado > 0:
                    linhas_validas += 1
                    contador_empenhado += 1
                    
                    # Limpar e categorizar função (que será tratada como órgão)
                    # Remove o número e traço do início (ex: "01 - Legislativa" vira "Legislativa")
                    funcao_limpa = funcao
                    if ' - ' in funcao:
                        funcao_limpa = funcao.split(' - ', 1)[1]
                    
                    orgao_limpo = limpar_caracteres_especiais(funcao_limpa)
                    categoria = mapear_categoria_padronizada(orgao_limpo)
                    
                    # Criar registro
                    ano_int = int(ano) if isinstance(ano, str) else ano
                    data = datetime(ano_int, 1, 1).date()
                    
                    dados_processados.append({
                        'estado': 'RJ',
                        'data': data,
                        'orgao': orgao_limpo,
                        'categoria_padronizada': categoria,
                        'valor': valor_empenhado
                    })
                    
            except Exception as e:
                print(f"  ⚠️  Erro na linha {linhas_processadas}: {e}")
                continue
        
        print(f"  📊 Estatísticas de processamento:")
        print(f"    - Linhas processadas: {linhas_processadas}")
        print(f"    - Linhas válidas: {linhas_validas}")
        print(f"    - Valores empenhados: {contador_empenhado}")
        print(f"    - Registros válidos: {len(dados_processados)}")
        
        # Salvar no banco
        if dados_processados:
            import sqlite3
            df_final = pd.DataFrame(dados_processados)
            conn = sqlite3.connect(nome_banco)
            df_final.to_sql(nome_tabela, conn, if_exists='append', index=False)
            conn.commit()
            conn.close()
            
            print(f"  ✅ {len(df_final)} registros inseridos para RJ")
            return len(df_final)
        else:
            print(f"  ⚠️  Nenhum dado válido encontrado para RJ")
            return 0
            
    except Exception as e:
        print(f"  ❌ Erro ao processar RJ: {e}")
        import traceback
        traceback.print_exc()
        return 0


def processar_sp_csv_especial(arquivo, nome_banco, nome_tabela, ano=2024):
    """
    Processa especificamente o CSV de São Paulo (SP).
    Ignora a última linha que contém apenas o total.
    """
    print(f"  🔧 Processamento especial para SP - ignorando última linha com total (ano: {ano})")
    
    try:
        dados_processados = []
        
        # Tentar diferentes encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                print(f"  🔄 Tentando encoding: {encoding}")
                df = pd.read_csv(arquivo, encoding=encoding, delimiter=",")
                print(f"  ✅ Sucesso com encoding: {encoding}")
                break
            except UnicodeDecodeError:
                print(f"  ❌ Falhou com encoding: {encoding}")
                continue
        
        if df is None:
            print(f"  ❌ Não foi possível ler o arquivo com nenhum dos encodings testados")
            return 0
        
        # Remover a última linha (que contém o total)
        if len(df) > 0:
            df = df.iloc[:-1]  # Remove a última linha
            print(f"  📋 Arquivo carregado com {len(df)} linhas (removida última linha com total)")
        
        print(f"  📋 Colunas encontradas: {list(df.columns)}")
        
        # Verificar se as colunas esperadas existem
        colunas_esperadas = ['Função', 'Ação', 'Despesa', 'Empenhado']
        colunas_encontradas = list(df.columns)
        
        # Verificar se pelo menos as colunas principais existem  
        if not ('Ação' in colunas_encontradas and 'Empenhado' in colunas_encontradas):
            print(f"  ⚠️  Colunas esperadas não encontradas. Esperadas: {colunas_esperadas}")
            print(f"  ⚠️  Encontradas: {colunas_encontradas}")
            return 0
        
        linhas_processadas = 0
        linhas_validas = 0
        contador_empenhado = 0
        
        for index, row in df.iterrows():
            try:
                linhas_processadas += 1
                
                # Extrair dados da linha
                acao = str(row['Ação']).strip() if pd.notna(row['Ação']) else 'Não informado'
                valor_empenhado_str = str(row['Empenhado']) if pd.notna(row['Empenhado']) else '0'
                
                # Pular linhas vazias ou inválidas
                if pd.isna(row['Ação']) or acao == 'nan' or acao == '':
                    continue
                
                # Função para converter valores monetários brasileiros
                def converter_valor_brasileiro(valor_str):
                    try:
                        # Remover espaços e caracteres especiais
                        valor_str = valor_str.strip()
                        
                        # Substituir vírgula por ponto para decimal
                        valor_str = valor_str.replace(',', '.')
                        
                        # Remover pontos de milhares (se houver múltiplos pontos)
                        partes = valor_str.split('.')
                        if len(partes) > 2:
                            # Reconstituir: juntar todas as partes exceto a última, depois adicionar a última
                            valor_str = ''.join(partes[:-1]) + '.' + partes[-1]
                        
                        return float(valor_str)
                    except (ValueError, AttributeError):
                        return 0.0
                
                # Converter valor
                valor_empenhado = converter_valor_brasileiro(valor_empenhado_str)
                
                # Processar apenas se há valor válido
                if valor_empenhado > 0:
                    linhas_validas += 1
                    contador_empenhado += 1
                    
                    # Limpar e categorizar ação (que será tratada como órgão)
                    orgao_limpo = limpar_caracteres_especiais(acao)
                    categoria = mapear_categoria_padronizada(orgao_limpo)
                    
                    # Criar registro
                    ano_int = int(ano) if isinstance(ano, str) else ano
                    data = datetime(ano_int, 1, 1).date()
                    
                    dados_processados.append({
                        'estado': 'SP',
                        'data': data,
                        'orgao': orgao_limpo,
                        'categoria_padronizada': categoria,
                        'valor': valor_empenhado
                    })
                    
            except Exception as e:
                print(f"  ⚠️  Erro na linha {linhas_processadas}: {e}")
                continue
        
        print(f"  📊 Estatísticas de processamento:")
        print(f"    - Linhas processadas: {linhas_processadas}")
        print(f"    - Linhas válidas: {linhas_validas}")
        print(f"    - Valores empenhados: {contador_empenhado}")
        print(f"    - Registros válidos: {len(dados_processados)}")
        
        # Salvar no banco
        if dados_processados:
            import sqlite3
            df_final = pd.DataFrame(dados_processados)
            conn = sqlite3.connect(nome_banco)
            df_final.to_sql(nome_tabela, conn, if_exists='append', index=False)
            conn.commit()
            conn.close()
            
            print(f"  ✅ {len(df_final)} registros inseridos para SP")
            return len(df_final)
        else:
            print(f"  ⚠️  Nenhum dado válido encontrado para SP")
            return 0
            
    except Exception as e:
        print(f"  ❌ Erro ao processar SP: {e}")
        import traceback
        traceback.print_exc()
        return 0
