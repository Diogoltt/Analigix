#!/usr/bin/env python3
"""
Script para remover registros de estados específicos do banco de dados.
"""

import sqlite3
import os
import sys
from datetime import datetime

def remover_registros_estado(estado=None, ano=None):
    """
    Remove registros do banco de dados baseado no estado e/ou ano especificado.
    
    Args:
        estado (str): Sigla do estado (ex: 'AP', 'CE', 'BA')
        ano (int): Ano específico para filtrar (ex: 2020, 2024)
    """
    # Caminho para o banco de dados
    banco_path = os.path.join(os.path.dirname(__file__), 'database', 'despesas_brasil.db')
    
    if not os.path.exists(banco_path):
        print(f"❌ Banco de dados não encontrado: {banco_path}")
        return False
    
    # Construir a query e parâmetros baseado nos filtros
    where_conditions = []
    params = []
    
    if estado:
        where_conditions.append("estado = ?")
        params.append(estado.upper())
    
    if ano:
        where_conditions.append("strftime('%Y', data) = ?")
        params.append(str(ano))
    
    if not where_conditions:
        print("❌ Nenhum filtro especificado. Informe pelo menos um estado ou ano.")
        return False
    
    where_clause = " AND ".join(where_conditions)
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect(banco_path)
        cursor = conn.cursor()
        
        # Verificar quantos registros existem antes da remoção
        query_count = f'SELECT COUNT(*) FROM despesas WHERE {where_clause}'
        cursor.execute(query_count, params)
        count_antes = cursor.fetchone()[0]
        
        if count_antes == 0:
            filtro_desc = []
            if estado:
                filtro_desc.append(f"estado {estado}")
            if ano:
                filtro_desc.append(f"ano {ano}")
            print(f"ℹ️  Nenhum registro encontrado para {' e '.join(filtro_desc)}.")
            conn.close()
            return True
        
        # Mostrar detalhes dos registros encontrados
        filtro_desc = []
        if estado:
            filtro_desc.append(f"estado {estado}")
        if ano:
            filtro_desc.append(f"ano {ano}")
        
        print(f"🔍 Encontrados {count_antes:,} registros para {' e '.join(filtro_desc)}.")
        
        # Mostrar breakdown por estado e ano se aplicável
        if estado and not ano:
            cursor.execute(f'SELECT strftime("%Y", data) as ano, COUNT(*) FROM despesas WHERE estado = ? GROUP BY ano ORDER BY ano', (estado.upper(),))
            breakdown = cursor.fetchall()
            if len(breakdown) > 1:
                print("📊 Breakdown por ano:")
                for ano_db, count in breakdown:
                    print(f"  {ano_db}: {count:,}")
        elif ano and not estado:
            cursor.execute(f'SELECT estado, COUNT(*) FROM despesas WHERE strftime("%Y", data) = ? GROUP BY estado ORDER BY estado', (str(ano),))
            breakdown = cursor.fetchall()
            if len(breakdown) > 1:
                print("📊 Breakdown por estado:")
                for estado_db, count in breakdown:
                    print(f"  {estado_db}: {count:,}")
        
        # Confirmar a remoção
        resposta = input(f"\nDeseja realmente remover {count_antes:,} registros? (s/N): ")
        
        if resposta.lower() not in ['s', 'sim', 'y', 'yes']:
            print("❌ Operação cancelada pelo usuário.")
            conn.close()
            return False
        
        # Remover registros
        query_delete = f'DELETE FROM despesas WHERE {where_clause}'
        cursor.execute(query_delete, params)
        registros_removidos = cursor.rowcount
        
        # Confirmar as mudanças
        conn.commit()
        
        print(f"✅ Removidos {registros_removidos:,} registros com sucesso!")
        
        # Verificar o estado final do banco
        cursor.execute('SELECT COUNT(*) FROM despesas')
        total_final = cursor.fetchone()[0]
        print(f"📊 Total de registros restantes no banco: {total_final:,}")
        
        # Mostrar registros por estado após remoção
        cursor.execute('SELECT estado, COUNT(*) FROM despesas GROUP BY estado ORDER BY estado')
        registros_por_estado = cursor.fetchall()
        
        if registros_por_estado:
            print("\n📊 Registros por estado após remoção:")
            for estado_db, count in registros_por_estado:
                print(f"  {estado_db}: {count:,}")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao acessar o banco de dados: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def mostrar_ajuda():
    """Mostra informações de uso do script."""
    print("📖 Uso do script:")
    print("  python remover_registros.py [--estado ESTADO] [--ano ANO]")
    print()
    print("Exemplos:")
    print("  python remover_registros.py --estado AP")
    print("  python remover_registros.py --ano 2020") 
    print("  python remover_registros.py --estado CE --ano 2024")
    print()
    print("Parâmetros:")
    print("  --estado: Sigla do estado (AP, CE, BA, etc.)")
    print("  --ano: Ano específico (2020, 2021, 2022, etc.)")
    print("  --help: Mostra esta ajuda")

def main():
    """Função principal que processa argumentos da linha de comando."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Remove registros de despesas do banco de dados por estado e/ou ano",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python remover_registros.py --estado AP
  python remover_registros.py --ano 2020
  python remover_registros.py --estado CE --ano 2024
        """
    )
    
    parser.add_argument('--estado', '-e', 
                       help='Sigla do estado para remover (ex: AP, CE, BA)')
    parser.add_argument('--ano', '-a', type=int,
                       help='Ano específico para remover (ex: 2020, 2024)')
    
    args = parser.parse_args()
    
    # Verificar se pelo menos um parâmetro foi fornecido
    if not args.estado and not args.ano:
        print("❌ Erro: Informe pelo menos um estado (--estado) ou ano (--ano)")
        print()
        mostrar_ajuda()
        return False
    
    print("🗑️  Script de Remoção de Registros")
    print("=" * 50)
    
    sucesso = remover_registros_estado(args.estado, args.ano)
    
    if sucesso:
        print("\n✅ Script executado com sucesso!")
    else:
        print("\n❌ Script falhou na execução.")
    
    return sucesso

if __name__ == "__main__":
    main()
