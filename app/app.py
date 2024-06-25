import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis do arquivo .env
DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

# Criar a URL de conexão do banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criar o engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

def get_data():
    query = f"""
    SELECT
        data,
        simbolo,
        valor_fechamento,
        acao,
        quantidade,
        valor,
        ganho
    FROM
        public.dm_commodities;
    """
    df = pd.read_sql(query, engine)

 # Tratamento de valores nulos e conversão de tipos
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df['simbolo'] = df['simbolo'].astype(str)
    df['valor_fechamento'] = pd.to_numeric(df['valor_fechamento'], errors='coerce')
    df['acao'] = df['acao'].astype(str)
    df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df['ganho'] = pd.to_numeric(df['ganho'], errors='coerce')
    # trate valores nulos após a conversão, se necessário
    df = df.fillna({
        'valor_fechamento': 0,
        'quantidade': 0,
        'valor': 0,
        'ganho': 0
        })
        
    return df


# Configurar a página do Streamlit
st.set_page_config(page_title='Dashboard do diretor', layout='wide')

# Título do Dashboard
st.title('Esse e um texto')

# Descrição
st.write("""
Este dashboard mostra os dados de commodities e suas transações.
""")

# Obter os dados
df = get_data()

st.dataframe(df)