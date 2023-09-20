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

with st.container():
    st.write('---')
    st.subheader('Vendas por linha de produtos')
    
    # Traduzindo os valores na coluna 'Product line' para o português
    vendas_por_linha = vendas.groupby('Product line')['Total'].sum().reset_index()
    vendas_por_linha = vendas_por_linha.sort_values(by='Total', ascending=False)
    vendas_por_linha.rename(columns={'Product line': 'Linha de Produto'}, inplace=True)
    vendas_por_linha['Linha de Produto'] = vendas_por_linha['Linha de Produto'].map({
        'Food and beverages': 'Alimentos e Bebidas',
        'Fashion accessories': 'Acessórios de Moda',
        'Electronic accessories': 'Acessórios Eletrônicos',
        'Sports and travel': 'Esportes e Viagem',
        'Home and lifestyle': 'Casa e Estilo de Vida',
        'Health and beauty': 'Saúde e Beleza'
    })
    
    # Exibir a tabela com os totais por linha de produtos em português
    st.table(vendas_por_linha)
   

    