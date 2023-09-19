import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title='Dash Supermarket')

with st.container():
    st.write('Filtrar dados de um supermercado')
    st.title('Dashboard :blue[Supermarket] :sunglasses:')
    st.write('Informações sobre dados de um supermercado')
    st.write('Acesso ao código? [Clique aqui](https://github.com/MarceloPorfirio/Dash_supermarket)')

@st.cache
def load_data():
    data = pd.read_csv("supermarket_sales - Sheet.csv")
    return data
with st.container():
    st.write('---')
    # Carregar os dados do arquivo CSV
    vendas = load_data()


   

    