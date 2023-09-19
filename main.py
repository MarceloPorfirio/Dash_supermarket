import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title='Dash Supermarket')

with st.container():
    st.write('Filtrar dados de um supermercado')
    st.title('Dashboard :blue[Supermarket] :sunglasses:')
    st.write('Informações sobre dados de um supermercado')
    st.write('Acesso ao código? [Clique aqui](https://github.com/MarceloPorfirio/Dash_supermarket)')

@st.cache_data
def load_data():
    data = pd.read_csv("supermarket_sales - Sheet1.csv")
    return data
with st.container():
    st.write('---')
    # Carregar os dados do arquivo CSV
    vendas = load_data()
    # Renomear a coluna 'Branch' para 'Filial'
    vendas = vendas.rename(columns={'Branch':'Filial'})
    # Tabela com os supermercados que mais venderam em ordem decrescente
    supermercados_mais_vendidos = vendas.groupby('Filial')['Total'].sum().reset_index()
    supermercados_mais_vendidos = supermercados_mais_vendidos.sort_values(by='Total', ascending=False)
    
    # Dividir a página em duas colunas
    col1, col2 = st.columns(2)
    
    # Gráfico de barras com as vendas por filial (na primeira coluna)
    with col1:
        st.subheader('Gráfico de Vendas por Filial')
        st.bar_chart(supermercados_mais_vendidos['Total'], width=350, height=250)
    
    # Tabela com as vendas por filial (na segunda coluna)
    with col2:
        st.subheader('Vendas por Filial')
        st.table(supermercados_mais_vendidos)


   

    