import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # Importe o Matplotlib
import sys
print(sys.path)


choice = st.sidebar.radio(
    label = 'Navegar',
    options = ('Inicio','Vendas Filial','Vendas Por Categoria', 
               'Formas De Pagamento','Clientes Crediário','Compra Por Gênero'),
    
)


def load_data():
    data = pd.read_csv("supermarket_sales - Sheet1.csv")
    return data

if choice == 'Inicio':
    with st.container():
        st.write('Filtrar dados de um supermercado')
        st.title('Dashboard :blue[Supermarket] :sunglasses:')
        st.write('Informações sobre dados de um supermercado')
        st.write('Acesso ao código? [Clique aqui](https://github.com/MarceloPorfirio/Dash_supermarket)')
        st.write('Fonte arquivo csv: [Clique aqui](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales)')
elif choice == 'Vendas Filial':
    with st.container():
       
        # Carregar os dados do arquivo CSV
        vendas = load_data()
        
        # Renomear a coluna 'Branch' para 'Filial'
        vendas = vendas.rename(columns={'Branch':'Filial'})
        
        # Tabela com as filiais que mais venderam em ordem decrescente
        supermercados_mais_vendidos = vendas.groupby('Filial')['Total'].sum().reset_index()
        supermercados_mais_vendidos = supermercados_mais_vendidos.sort_values(by='Total', ascending=False)
        
        # Dividir a página em duas colunas
        col1, col2 = st.columns(2)
        
        # Gráfico de barras com as vendas por filial (na primeira coluna)
        with col1:
            st.subheader('Gráfico de Vendas por Filial')
            st.bar_chart(supermercados_mais_vendidos['Total'], width=400, height=300)
        
        # Tabela com as vendas por filial (na segunda coluna)
        with col2:
            st.subheader('Vendas por Filial')
            st.table(supermercados_mais_vendidos)
elif choice == 'Vendas Por Categoria':
    with st.container():
        vendas = load_data()
        
        st.subheader('Venda por linha de produtos')
        
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

elif choice == 'Formas De Pagamento':
    with st.container():
        vendas = load_data()
        # Mostrar formas de pagamento mais utilizadas
        st.subheader('Formas de pagamento mais utilizadas')
        

        forma_pagamento = vendas.groupby('Payment')['Total'].sum().reset_index()
        forma_pagamento.rename(columns={'Total':'Total Soma'},inplace=True)
        forma_pagamento = forma_pagamento.sort_values(by='Total Soma', ascending=False)
        forma_pagamento['Payment'] = forma_pagamento['Payment'].map({
            'Cash': 'Dinheiro',
            'Ewallet': 'Crediário',
            'Credit card': 'Cartão de Crédito'
        })

        st.table(forma_pagamento)
elif choice == 'Clientes Crediário':
    with st.container():
        data = load_data()
        
        # Calcular o número total de clientes
        total_customers = len(data)

        # Contar o número de membros e clientes normais
        members_count = (data['Customer type'] == 'Member').sum()
        normal_count = (data['Customer type'] == 'Normal').sum()

        # Calcular as proporções em percentual
        percent_members = (members_count / total_customers) * 100
        percent_normal = (normal_count / total_customers) * 100

        # Criar um gráfico de pizza usando Streamlit
        st.subheader('Membros ativos vs Possíveis Membros')
        st.write(f'<font color="blue">Numero de Membros: {members_count}</font>', unsafe_allow_html=True)
        st.write(f'<font color="orange">Numero de Membros: {normal_count}</font>', unsafe_allow_html=True)

        # Defina o tamanho da figura

        # Criar o gráfico de pizza
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.pie([percent_members, percent_normal], labels=['Membros', 'Clientes Normais'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Exibir o gráfico de pizza no Streamlit
        st.pyplot(fig)
elif choice == 'Compra Por Gênero':
    # Título do aplicativo
    data = load_data()
    st.subheader("Análise de Compras por Categoria de Produto")
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