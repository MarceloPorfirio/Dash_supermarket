
import streamlit as st
import pandas as pd
import calendar
import plotly.express as px
import plotly.graph_objects as go
# import locale  # Importe o módulo locale

# # Configurar o ambiente local para português do Brasil
# locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


choice = st.sidebar.radio(
    label = 'Navegar',
    options = ('Inicio','Vendas Filial','Vendas Por Categoria', 
               'Formas De Pagamento','Clientes Crediário','Compra Por Gênero','Indicadores Mensais',
               'Avaliação de Produtos'),
    
)


def load_data():
    data = pd.read_csv("supermarket_sales - Sheet1.csv")
    return data

if choice == 'Inicio':
    with st.container():
        st.title('Dashboard :blue[Supermarket] :shopping_trolley:')
        st.subheader('Informações organizadas sobre dados de um supermercado.')
        st.caption('As informações consistem de um arquivos de dados fictícios [Fonte](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales)')
        st.caption('Acesso ao código? [Clique aqui](https://github.com/MarceloPorfirio/Dash_supermarket)')
        st.markdown('<p style="font-family: \'Arial\', sans-serif; color: blue; font-size: 20px;">Exemplo de personalização com html</p>',unsafe_allow_html=True )
        
elif choice == 'Vendas Filial':
    with st.container():
       
        # Carregar os dados do arquivo CSV
        vendas = load_data()
        
        # Renomear a coluna 'Branch' para 'Filial'
        vendas = vendas.rename(columns={'Branch':'Filial'})
        
        # Tabela com as filiais que mais venderam em ordem decrescente
        supermercados_mais_vendidos = vendas.groupby('Filial')['Total'].sum().reset_index()
        supermercados_mais_vendidos = supermercados_mais_vendidos.sort_values(by='Total', ascending=False)
        
        st.subheader('Vendas por Filial')
        st.bar_chart(supermercados_mais_vendidos['Total'], width=300, height=280)
        
        # Tabela com as vendas por filial (na segunda coluna)

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
        
        # Gráfico de barras
        # st.subheader('Gráfico')
        st.bar_chart(vendas_por_linha.set_index('Linha de Produto')['Total'])
        st.table(vendas_por_linha)
elif choice == 'Formas De Pagamento':
    with st.container():
        vendas = load_data()
        # Mostrar formas de pagamento mais utilizadas
        st.subheader('Formas de pagamento mais utilizadas')
        

        forma_pagamento = vendas.groupby('Payment')['Total'].sum().reset_index()
        forma_pagamento.rename(columns={'Payment':'Forma de Pagamento'},inplace=True)
        forma_pagamento = forma_pagamento.sort_values(by='Total', ascending=False)
        forma_pagamento['Forma de Pagamento'] = forma_pagamento['Forma de Pagamento'].map({
            'Cash': 'Dinheiro',
            'Ewallet': 'Crediário',
            'Credit card': 'Cartão de Crédito'
        })
        st.bar_chart(forma_pagamento['Total'],width=300,height=300)
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

        
        # Criar um gráfico de pizza
        fig = go.Figure(data=[go.Pie(labels=['Membros', 'Clientes Normais'], values=[members_count, normal_count],hole=0.3)])

        # Definir as cores das fatias
        colors = ['blue', 'orange']
        fig.update_traces(marker=dict(colors=colors))

        # Exibir o gráfico de pizza no Streamlit
        st.title("Clientes Crediário")
        st.subheader('Membros Ativos vs Clientes Normais')
        st.plotly_chart(fig)

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
        "Gênero": ["Masculino", "Feminino"],
        "Total Gasto": [total_gasto_male, total_gasto_female]
    })

    # Exibir os resultados em uma tabela
    # st.write("Resultados:")
    # st.bar_chart(resultados.set_index("Total Gasto").T
    # Criar um gráfico de barras horizontal com a biblioteca Plotly
    # st.write(f"Total Gasto por Gênero em {categoria_escolhida}")
    fig = px.bar(resultados, x="Total Gasto", y="Gênero", orientation="h", text="Total Gasto")
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    fig.update_layout(xaxis_title="Total Gasto", yaxis_title="Gênero",width=600,height=250)
    st.plotly_chart(fig)
    st.table(resultados)

elif choice == 'Indicadores Mensais':
    with st.container():
        data = load_data()
        # Título do aplicativo
        st.title("Análise de Vendas por Mês")

        # Converter a coluna 'Date' para tipo datetime
        data['Date'] = pd.to_datetime(data['Date'])

        # Adicionar colunas de mês e ano
        data['Month'] = data['Date'].dt.month
        data['Year'] = data['Date'].dt.year

        # Criar um selectbox para escolher o mês
        nomes_meses = [calendar.month_name[i].capitalize() for i in range(1, 13)]  # Nomes dos meses em português

        # Modificar os nomes dos meses para portugues
        nomes_meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        mes_selecionado = st.selectbox("Selecione um Mês:", nomes_meses)

        # Mapear o nome do mês de volta para o número do mês
        mes_numero = {v: k for k, v in enumerate(nomes_meses, start=1)}

        # Filtrar os dados pelo mês selecionado
        vendas_por_mes = data[data['Month'] == mes_numero[mes_selecionado]]

        # Calcular o valor total das vendas para o mês selecionado
        total_vendas_mes = vendas_por_mes['Total'].sum()

        # Exibir o valor total das vendas para o mês selecionado
        st.subheader(f"Total de Vendas para o Mês de {mes_selecionado}:")
        st.header(f"R$ {total_vendas_mes:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
elif choice == 'Avaliação de Produtos':
    with st.container():
        data = load_data()
        st.subheader('Rank de avaliação de produtos')
        # Agrupar os dados por linha de produto e calcular a média das avaliações
        avaliacoes_por_categoria = data.groupby('Product line')['Rating'].mean().reset_index()

        # Renomear colunas
        avaliacoes_por_categoria.rename(columns={'Rating': 'Avaliação Média'}, inplace=True)

        # Classificar as categorias com base na avaliação média
        avaliacoes_por_categoria = avaliacoes_por_categoria.sort_values(by='Avaliação Média', ascending=False)

        #

        # Exibir a tabela com o rank de avaliações por categoria
        st.table(avaliacoes_por_categoria)   