import streamlit as st
import pandas as pd

# Carregue o DataFrame (substitua "data.csv" pelo nome do seu arquivo CSV)
data = pd.read_csv("supermarket_sales - Sheet1.csv")

# Título do aplicativo
st.title("Análise de Compras por Categoria de Produto")
data['Product line'] = data['Product line'].map({
            'Food and beverages': 'Alimentos e Bebidas',
            'Fashion accessories': 'Acessórios de Moda',
            'Electronic accessories': 'Acessórios Eletrônicos',
            'Sports and travel': 'Esportes e Viagem',
            'Home and lifestyle': 'Casa e Estilo de Vida',
            'Health and beauty': 'Saúde e Beleza'
        })
# Caixa de seleção para escolher a categoria de produto
categoria_escolhida = st.selectbox("Escolha a Categoria de Produto:", data["Product line"].unique())

# Filtrar os dados com base na categoria de produto escolhida
dados_filtrados = data[data["Product line"] == categoria_escolhida]

# Calcular o total gasto por gênero
total_gasto_male = dados_filtrados[dados_filtrados["Gender"] == "Male"]["Total"].sum()
total_gasto_female = dados_filtrados[dados_filtrados["Gender"] == "Female"]["Total"].sum()


# Criar um DataFrame com os resultados
resultados = pd.DataFrame({
    "Gênero": ["Male", "Female"],
    "Total Gasto": [total_gasto_male, total_gasto_female]
})

# Exibir os resultados em uma tabela
st.write("Resultados:")
st.table(resultados)
