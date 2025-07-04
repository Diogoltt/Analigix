# 📊 Analigix - Análise de Transparência Pública dos Estados Brasileiros

Analigix é uma plataforma completa para análise e visualização de dados de transparência pública dos estados brasileiros. O sistema permite processar, analisar e visualizar informações sobre gastos públicos de todos os 26 estados brasileiros e o Distrito Federal.

## 🎯 Funcionalidades

- **ETL Automatizado**: Sistema de importação e processamento de dados de transparência de todos os estados
- **Análise de Dados**: Categorização automática de despesas públicas
- **Visualizações Interativas**: Gráficos e mapas para análise dos dados
- **API RESTful**: Backend em Flask para servir os dados processados
- **Interface Web**: Frontend React para visualização e interação
- **Banco de Dados**: SQLite para armazenamento dos dados processados

## 🏗️ Arquitetura do Projeto

```
Analigix/
├── back/                          # Backend (Python/Flask)
│   ├── app/                       # Aplicação Flask
│   │   ├── __init__.py           # Configuração da app
│   │   ├── routes.py             # Rotas da API
│   │   └── swagger_config.py     # Configuração do Swagger
│   ├── etl/                      # Sistema ETL
│   │   ├── config/               # Configurações do ETL
│   │   │   └── mapeamento_estados.py  # Mapeamento de colunas por estado
│   │   ├── core/                 # Núcleo do ETL
│   │   │   ├── categorizador.py  # Categorização de despesas
│   │   │   ├── database.py       # Operações de banco
│   │   │   └── utils.py          # Utilitários
│   │   ├── processadores/        # Processadores especiais
│   │   │   └── especiais.py      # Estados com formato especial
│   │   └── run_etl.py            # Script principal do ETL
│   ├── csvs/                     # Dados CSV dos estados
│   ├── database/                 # Banco de dados SQLite
│   ├── requirements.txt          # Dependências Python
│   ├── run.py                    # Servidor da API
│   └── .env                      # Variáveis de ambiente
├── front/                        # Frontend (React)
│   ├── public/                   # Arquivos públicos
│   ├── src/                      # Código fonte React
│   │   ├── componentes/          # Componentes React
│   │   ├── pages/                # Páginas da aplicação
│   │   ├── routes/               # Configuração de rotas
│   │   └── util/                 # Utilitários
│   ├── package.json              # Dependências Node.js
│   └── README.md                 # Documentação do frontend
└── README.md                     # Este arquivo
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

- **Python 3.8+** instalado
- **Node.js 16+** e **npm** instalados
- **Git** para clonar o repositório

### 1. Clone o Repositório

```bash
git clone https://github.com/Diogoltt/Analigix.git
cd Analigix
```

### 2. Configuração do Backend

#### 2.1. Navegue para o diretório do backend

```bash
cd back
```

#### 2.2. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 2.3. Configure as variáveis de ambiente

Edite o arquivo `.env` e configure suas variáveis:

```env
# OpenAI API Configuration (opcional)
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_PATH=database/despesas_brasil.db
```

#### 2.4. Inicie o servidor da API

```bash
python run.py
```

A API estará disponível em: `http://127.0.0.1:5000`

### 3. Configuração do Frontend

#### 3.1. Em outro terminal, navegue para o frontend

```bash
cd front
```

#### 3.2. Instale as dependências

```bash
npm install
```

#### 3.3. Inicie o servidor de desenvolvimento

```bash
npm start
```

A aplicação estará disponível em: `http://localhost:3000`

## 🔧 Sistema ETL

O sistema ETL (Extract, Transform, Load) é responsável por processar os dados de transparência dos estados brasileiros.

### Estados Suportados

O sistema suporta todos os 26 estados brasileiros + DF, exceto Pernambuco(PE) e Sergipe(SE):

- AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PI, RJ, RN, RS, RO, RR, SC, SP, TO

Alguns estados possuem processadores especiais devido a formatos específicos de seus CSVs:

- **Tocantins (TO)**: Pula 2 linhas iniciais e remove linha de total
- **São Paulo (SP)**: Remove linha de total
- **Rio de Janeiro (RJ)**: Pula 15 linhas iniciais
- **Mato Grosso do Sul (MS)**: Pula 4 linhas iniciais
- **Distrito Federal (DF)**: Pula linha de título
- **Maranhão (MA)**: Remove 3 linhas finais inúteis
- **Rio Grande do Sul (RS)**: Filtragem por ano
- **Goiás (GO)**: Filtragem por ano
- **Rondônia (RO)**: Processamento especial com csv.reader

## 📊 API Endpoints

A API oferece endpoints para acessar os dados processados:

- `GET /` - Status da API
- `GET /docs` - Documentação Swagger (quando disponível)

## 🎨 Frontend

O frontend é desenvolvido em React e oferece:

- **Mapa Interativo**: Visualização geográfica dos dados
- **Dashboards**: Painéis com gráficos e estatísticas
- **Comparações**: Análise comparativa entre estados
- **Filtros**: Filtros por ano, estado e categoria de despesa

### Componentes Principais

- **Mapas**: Componentes SVG dos estados brasileiros
- **Gráficos**: Visualizações usando Recharts
- **Botões**: Interface de navegação
- **Modais**: Janelas de detalhes

## 🗄️ Banco de Dados

O sistema utiliza SQLite para armazenar os dados processados. A tabela principal contém:

- `id`: Identificador único
- `estado`: Sigla do estado (ex: SP, RJ)
- `data`: Data do registro
- `orgao`: Nome do órgão/função
- `categoria_padronizada`: Categoria padronizada da despesa
- `valor`: Valor da despesa

## 🛠️ Scripts Utilitários

### Backend

- `run.py`: Inicia o servidor da API
- `verificar_db.py`: Verifica status do banco de dados
- `remover_registros.py`: Remove registros do banco

### Frontend

- `npm start`: Servidor de desenvolvimento
- `npm build`: Build para produção
- `npm test`: Executa testes

## 🔍 Troubleshooting

### Problemas Comuns

1. **Erro de encoding ao processar CSV**

   - O sistema tenta múltiplos encodings automaticamente
   - Verifique se o arquivo CSV está correto

2. **Banco de dados não encontrado**

   - Execute o ETL primeiro para criar o banco
   - Verifique o caminho em `.env`

3. **API não responde**

   - Verifique se o servidor Flask está rodando
   - Confirme a porta 5000 está disponível

4. **Frontend não carrega**
   - Verifique se as dependências foram instaladas
   - Confirme se a API está rodando

---

**Analigix** - Tornando a transparência pública mais acessível e compreensível.
