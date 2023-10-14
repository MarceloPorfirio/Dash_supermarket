
import streamlit as st
import pandas as pd
import calendar
import plotly.express as px
import plotly.graph_objects as go


# # Configurar o ambiente local para português do Brasil
# locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
options = ('Inicio','Vendas Filial','Vendas Por Categoria', 
               'Formas De Pagamento','Clientes Crediário','Compra Por Gênero','Indicadores Mensais',
               'Avaliação de Produtos','Movimento Diário','Renda Bruta')

# Separar 'Inicio' do restante das opções
inicio, *restante = options

# Organizar as opções restantes em ordem alfabética
opcoes_ordenadas = [inicio, *sorted(restante)]

# Adicionando um rótulo HTML para estilizar o texto da barra lateral
st.sidebar.markdown("<h1 style='text-align: center;'>Navegar</h1>", unsafe_allow_html=True)

choice = st.sidebar.radio(
    label = '',
    options = opcoes_ordenadas,
    
)
    

def load_data():
    data = pd.read_csv("supermarket_sales - Sheet1.csv")
    return data

if choice == 'Inicio':
    with st.container():
        st.title('Dashboard :blue[Supermarket] :shopping_trolley:')
        st.markdown('<h2 style="font-size: 25px;">Informações organizadas referente aos dados <br>de uma rede de supermercados.</h2>', unsafe_allow_html=True)
        st.markdown('<h2 style="font-size: 25px;">Você pode navegar pelo menu lateral,<br>encontre as informações desejadas na base de dados.</h2>', unsafe_allow_html=True)
        st.caption('As informações consistem de um arquivos de dados fictícios: [Fonte](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales)')
        st.caption('Acesso ao código? [Clique aqui](https://github.com/MarceloPorfirio/Dash_supermarket)')
        
elif choice == 'Vendas Filial':
    with st.container():
       
        # Carregar os dados do arquivo CSV
        vendas = load_data()
        
        # Renomear a coluna 'Branch' para 'Filial'
        vendas = vendas.rename(columns={'Branch':'Filial'})
        
        # Tabela com as filiais que mais venderam em ordem decrescente
        supermercados_mais_vendidos = vendas.groupby('Filial')['Total'].sum().reset_index()
        supermercados_mais_vendidos = supermercados_mais_vendidos.sort_values(by='Total', ascending=False)

        # Mapear cada filial para uma cor específica
        colors = {'Filial A': 'blue', 'Filial B': 'green', 'Filial C': 'red'}

        # Gráfico de barras horizontais com cores diferentes
        fig = px.bar(supermercados_mais_vendidos, x='Total', y='Filial', orientation='h',
                 color='Filial',
                 labels={'Total': 'Total de Vendas', 'Filial': 'Filial'})

        # Ajustar layout do gráfico
        fig.update_layout(width=600,height=250, margin=dict(l=0, r=0, t=0, b=0))

       
        st.subheader('Venda Total Por Filial')
         # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)
        
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
        
        # Criar um gráfico de pizza com Plotly Express
        fig = px.pie(vendas_por_linha, names='Linha de Produto', values='Total')
        fig.update_layout(width=800,height=350)
        # Exibir o gráfico
        st.plotly_chart(fig)
        
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
        # Mapear cada forma de pagamento para uma cor específica
        colors = {'Dinheiro': 'blue', 'Crediário': 'green', 'Cartão de Crédito': 'red'}

        # Gráfico de barras horizontais com cores diferentes
        fig = px.bar(forma_pagamento, x='Total', y='Forma de Pagamento', orientation='h',
                    color='Forma de Pagamento',
                    color_discrete_map=colors,  # Usar as cores mapeadas
                    labels={'Total': 'Total de Vendas', 'Forma de Pagamento': 'Forma de Pagamento'})

        # Ajustar layout do gráfico
        fig.update_layout(width=600, height=250, margin=dict(l=0, r=0, t=0, b=0))

        # Exibir o gráfico
        st.plotly_chart(fig)
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

        # Criar um DataFrame com os resultados
        resultados = pd.DataFrame({
            "Rótulo": ["Member", "Normal"],
            "Quantidade": [members_count, normal_count]
        })

        
        # Criar um gráfico de pizza
        fig = go.Figure(data=[go.Pie(labels=['Membros', 'Clientes Normais'], values=[members_count, normal_count],hole=0.3)])
        fig.update_layout(width=600,height=400)
        # Definir as cores das fatias
        colors = ['blue', 'orange']
        fig.update_traces(marker=dict(colors=colors))

        # Exibir o gráfico de pizza no Streamlit
        st.title("Clientes Crediário")
        st.plotly_chart(fig)
        st.table(resultados)

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

    fig = px.bar(resultados, x="Total Gasto", y="Gênero", orientation="h", text="Total Gasto")
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    fig.update_layout(xaxis_title="Total Gasto", yaxis_title="Gênero",width=600,height=250)
    st.plotly_chart(fig)
    st.table(resultados)

elif choice == 'Indicadores Mensais':
    with st.container():
        data = load_data()
      
        st.title("Vendas por Mês")

        # Converter a coluna 'Date' para tipo datetime
        data['Date'] = pd.to_datetime(data['Date'])

        # Adicionar colunas de mês e ano
        data['Month'] = data['Date'].dt.month
        data['Year'] = data['Date'].dt.year

        # Criar um seletor para escolher a filial
        filiais_ordenadas = sorted(data['Branch'].unique())
        filial_selecionada = st.selectbox("Selecione uma Filial:", filiais_ordenadas)

        # Filtrar os dados pela filial selecionada
        data_filial = data[data['Branch'] == filial_selecionada]

        # Criar um selectbox para escolher o mês
        nomes_meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        mes_selecionado = st.selectbox("Selecione um Mês:", nomes_meses)

        # Mapear o nome do mês de volta para o número do mês
        mes_numero = {v: k for k, v in enumerate(nomes_meses, start=1)}

        # Filtrar os dados pela filial e pelo mês selecionado
        vendas_por_mes = data_filial[data_filial['Month'] == mes_numero[mes_selecionado]]

        # Calcular o valor total das vendas para o mês selecionado
        total_vendas_mes = vendas_por_mes['Total'].sum()

        # Exibir o valor total das vendas para o mês selecionado
        st.subheader(f"Total de Vendas para o Mês de {mes_selecionado} na Filial {filial_selecionada}:")
        st.header(f"R$ {total_vendas_mes:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))


elif choice == 'Avaliação de Produtos':
    with st.container():
        data = load_data()
        data['Product line'] = data['Product line'].map({
                'Food and beverages': 'Alimentos e Bebidas',
                'Fashion accessories': 'Acessórios de Moda',
                'Electronic accessories': 'Acessórios Eletrônicos',
                'Sports and travel': 'Esportes e Viagem',
                'Home and lifestyle': 'Casa e Estilo de Vida',
                'Health and beauty': 'Saúde e Beleza'
            })
        st.subheader('Rank de avaliação de produtos')
        st.write(':star:'* 5)
        # Agrupar os dados por linha de produto e calcular a média das avaliações
        avaliacoes_por_categoria = data.groupby('Product line')['Rating'].mean().reset_index()
        avaliacoes_por_categoria.rename(columns={'Product line': 'Linha de produto'}, inplace=True)

        # Renomear colunas
        avaliacoes_por_categoria.rename(columns={'Rating': 'Avaliação por categoria'}, inplace=True)

        # Suponha que 'avaliacoes_por_categoria' seja um DataFrame do Pandas e a coluna 'Avaliação Média' seja um float
        avaliacoes_por_categoria['Avaliação por categoria'] = avaliacoes_por_categoria['Avaliação por categoria'].apply(lambda x:f'{x:.2f}')

        # Classificar as categorias com base na avaliação média
        avaliacoes_por_categoria = avaliacoes_por_categoria.sort_values(by='Avaliação por categoria', ascending=False)

        #   

        # Exibir a tabela com o rank de avaliações por categoria
        st.table(avaliacoes_por_categoria)  
elif choice == "Movimento Diário":
      with st.container():
        vendas = load_data()
        # Converter a coluna 'Date' para tipo datetime
        vendas['Date'] = pd.to_datetime(vendas['Date'])

        # Adicionar colunas de dia, mês e ano
        vendas['Day'] = vendas['Date'].dt.day
        vendas['Month'] = vendas['Date'].dt.month
        vendas['Year'] = vendas['Date'].dt.year
        st.subheader('Selecione a Filial')
        # Criar um select box para escolher a filial
        filial_escolhida = st.selectbox("", vendas["Branch"].unique())

        # Filtrar os dados com base na filial escolhida
        dados_filtrados = vendas[vendas["Branch"] == filial_escolhida]

        # Agrupar os dados por dia e calcular o total diário de vendas
        total_diario = dados_filtrados.groupby('Day')['Total'].sum().reset_index()

        # Criar um gráfico de linha dinâmico para o total diário de vendas
        fig = px.line(total_diario, x='Day', y='Total', title=f'Total Diário de Vendas - Filial {filial_escolhida}',
                    labels={'Total': 'Total de Vendas', 'Day': 'Dia'})

        # Ajustar layout do gráfico
        fig.update_layout(width=700, height=400, margin=dict(l=0, r=0, t=30, b=0))

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)
elif choice == 'Renda Bruta':
    # Carregar os dados do arquivo CSV
    vendas = load_data()

    # Renomear a coluna 'Branch' para 'Filial'
    vendas = vendas.rename(columns={'Branch':'Filial'})

    # Tabela com as filiais que mais venderam em ordem decrescente
    supermercados_mais_vendidos = vendas.groupby('Filial')['gross income'].sum().reset_index()
    supermercados_mais_vendidos = supermercados_mais_vendidos.sort_values(by='gross income', ascending=False)

    # Mapear cada filial para uma cor específica
    colors = {'Filial A': 'yellow', 'Filial B': 'green', 'Filial C': 'red'}

    # Gráfico de barras horizontais com cores diferentes
    fig = px.bar(supermercados_mais_vendidos, x='gross income', y='Filial', orientation='h',
                color='Filial',
                 color_discrete_map=colors,
                labels={'gross income': 'Renda Bruta', 'Filial': 'Filial'})

    # Ajustar layout do gráfico
    fig.update_layout(width=600, height=250, margin=dict(l=0, r=0, t=0, b=0))

    # Exibir o gráfico no Streamlit
    st.subheader('Renda Bruta Por Filial')
    st.plotly_chart(fig)
    supermercados_mais_vendidos = supermercados_mais_vendidos.rename(columns={'gross income':'Renda Bruta'})
    # Substituir o separador de milhar e decimal na tabela
    
    st.table(supermercados_mais_vendidos)
