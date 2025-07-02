# Sistema de Importação de Dados de Transparência - Refatorado

## 📁 Nova Estrutura do Projeto

O código foi refatorado para melhor organização e manutenibilidade, dividido em módulos especializados:

```
etl/
├── run_etl.py  # Arquivo principal refatorado
├── config/
│   ├── __init__.py
│   └── mapeamento_estados.py             # Configurações de mapeamento de colunas por estado
├── core/
│   ├── __init__.py
│   ├── categorizador.py                  # Sistema de categorização de despesas
│   ├── utils.py                          # Utilitários (detecção de colunas, manipulação de dados)
│   └── database.py                       # Gerenciamento do banco SQLite
└── processadores/
    ├── __init__.py
    └── especiais.py                      # Processadores especiais (RO, RS)
```

## 🔧 Módulos e Responsabilidades

### 📋 `config/mapeamento_estados.py`
- **Responsabilidade**: Configuração de mapeamento de colunas para cada estado
- **Conteúdo**: Dicionário `MAPEAMENTO_COLUNAS` com configurações específicas de cada estado
- **Vantagem**: Facilita adicionar novos estados ou modificar mapeamentos existentes

### 🎯 `core/categorizador.py`
- **Responsabilidade**: Sistema de categorização de despesas por área
- **Funções principais**:
  - `mapear_categoria_padronizada()`: Categoriza despesas baseado no órgão
  - `limpar_caracteres_especiais()`: Processa texto mantendo caracteres corrompidos
- **Vantagem**: Fácil manutenção e expansão das regras de categorização

### 🛠️ `core/utils.py`
- **Responsabilidade**: Utilitários para processamento de dados
- **Funções principais**:
  - `detectar_colunas_csv()`: Detecção automática de colunas
  - `obter_valor_coluna()`: Extração e conversão de valores monetários
  - `carregar_csv_com_encoding()`: Carregamento de CSV com diferentes encodings
- **Vantagem**: Reutilização de código e tratamento consistente de dados

### 💾 `core/database.py`
- **Responsabilidade**: Gerenciamento do banco SQLite
- **Funções principais**:
  - `verificar_banco()`: Verifica/cria banco e tabelas
  - `salvar_dados()`: Persiste dados processados
- **Vantagem**: Centraliza operações de banco de dados

### ⚙️ `processadores/especiais.py`
- **Responsabilidade**: Processadores para estados com peculiaridades
- **Estados especiais**:
  - **RO**: Usa `csv.reader` para evitar problemas de parsing
  - **RS**: Filtra apenas dados de 2024
- **Vantagem**: Isola complexidades específicas sem afetar o fluxo principal


### Executar Diretamente
```bash
cd etl
python run_etl.py
```
