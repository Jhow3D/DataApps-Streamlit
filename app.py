import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    "Dashboard de Vendas",
    layout="wide",
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help':'http://http://www.meusite.com.br',
        'About':'App desenvolvivo no curso'
    }
)

with open('assets\styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

df = pd.read_excel(r'./assets/base_dados.xlsx')

#df

# Criando o SideBar para colocar os filtros: 

with st.sidebar:
    st.subheader("MENU - DASHBOARD DE VENDAS")
    fVendedor = st.selectbox(
        "Selecione o vendendor:",
        options=df['Vendedor'].unique()
    )
    
    fProduto = st.selectbox(
        "Selecione o produto:",
        options=df['Produto vendido'].unique()
    )
    fCliente = st.selectbox(
        "Selecione o cliente:",
        options=df['Cliente'].unique()
    )
    
    tabel_qtde_produto = df.loc[
        (df['Vendedor'] == fVendedor) & 
        (df['Cliente'] == fCliente)]

 #Tabela de quantidade de vendas por produto    
    tabel_qtde_produto = tabel_qtde_produto.drop(columns=['Data',
                                                         'Vendedor',
                                                         'Cliente',
                                                         'Nº pedido',
                                                         "Região"])

    tabel_qtde_produto = tabel_qtde_produto.groupby('Produto vendido').sum().reset_index()

#Tabela de Vendas e Margem

# tab1_qtde_produto = pd.pivot_table(df, values=['Quantidade', 'Preço', 'Valor Pedido', 'Margem Lucro'], index=['Produto vendido'], aggfunc={'Quantidade': 'sum', 'Preço': 'sum', 'Valor Pedido': 'sum', 'Margem Lucro': 'sum'} )
# tab1_qtde_produto

tabel_vendas_margem = df.loc[(
    df['Vendedor'] == fVendedor) & 
    (df['Produto vendido'] == fProduto) & 
    (df['Cliente'] == fCliente)]

#tabel_vendas_margem

#Tabela de vendas por vendendor: 
tabel_vendas_vendedor = df.loc[
    (df['Produto vendido'] == fProduto) &
    (df['Cliente'] == fCliente)
]
tabel_vendas_vendedor = tabel_vendas_vendedor.drop(columns=['Data',
                                                        'Cliente',
                                                        "Região",
                                                        'Produto vendido',
                                                        'Nº pedido',
                                                        'Preço'])

tabel_vendas_vendedor = tabel_vendas_vendedor.groupby('Vendedor').sum().reset_index()
#tabel_vendas_vendedor

# Vendas por cliente: 

tabel_vendas_cliente = df.loc[(df['Vendedor'] == fVendedor) &
                              (df['Produto vendido'] == fProduto)]

tabel_vendas_cliente = tabel_vendas_cliente.drop(columns=['Data',
                                                        "Região",
                                                        'Produto vendido',
                                                        'Nº pedido',
                                                        'Preço',
                                                        'Vendedor'])

tabel_vendas_cliente = tabel_vendas_cliente.groupby('Cliente').sum().reset_index()
#tabel_vendas_cliente

# Criação dos gráficos:

# Gráfico de quantidade de produto:
graf1_qtde_produto = px.bar(tabel_qtde_produto,x='Produto vendido',
                            y='Quantidade',
                            title="QUANTIDADE VENDIDA POR PRODUTO",
                            text_auto='.2s')
graf1_qtde_produto.update_traces(marker_color='rgb(158,202,225)',
                                 marker_line_color = 'rgb(8,48,107)',
                                 marker_line_width=1.5,
                                 opacity=0.6,  
                                 textfont_size=12, 
                                 textangle=0, 
                                 textposition="outside", 
                                 cliponaxis=False)
graf1_qtde_produto.update_layout(title_x=0.3)

#st.write(graf1_qtde_produto)

# Gráfico valor da vendas por produto: 
graf2_valor_produto = px.bar(tabel_qtde_produto,x='Produto vendido',
                            y='Valor Pedido',
                            title="VALOR TOTAL POR PRODUTO",
                            text_auto='.2s')
graf2_valor_produto.update_traces(marker_color='rgb(158,202,225)',
                                 marker_line_color = 'rgb(8,48,107)',
                                 marker_line_width=1.5,
                                 opacity=0.6,  
                                 textfont_size=12, 
                                 textangle=0, 
                                 textposition="outside", 
                                 cliponaxis=False)
graf2_valor_produto.update_layout(title_x=0.3)


#st.write(graf2_valor_produto)

# Gráfico de total de vendas por vendedor: 

graf3_total_vendedor = px.bar(tabel_vendas_vendedor,x='Vendedor',
                              y='Valor Pedido',
                              title='VALOR DE VENDA POR VENDEDOR',
                              text_auto='.2s')
graf3_total_vendedor.update_traces(marker_color='rgb(158,202,225)',
                                 marker_line_color = 'rgb(8,48,107)',
                                 marker_line_width=1.5,
                                 opacity=0.6,  
                                 textfont_size=12, 
                                 textangle=0, 
                                 textposition="outside", 
                                 cliponaxis=False)
graf3_total_vendedor.update_layout(title_x=0.3)

#graf3_total_vendedor

# Gráfico de vendas por cliente:

graf4_venda_cliente = px.bar(tabel_vendas_cliente,x='Cliente',
                             y='Valor Pedido',
                             title='VENDAS POR CLIENTE',
                             text_auto='.2s')
graf4_venda_cliente.update_traces(marker_color='rgb(158,202,225)',
                                 marker_line_color = 'rgb(8,48,107)',
                                 marker_line_width=1.5,
                                 opacity=0.6,  
                                 textfont_size=12, 
                                 textangle=0, 
                                 textposition="outside", 
                                 cliponaxis=False)
graf4_venda_cliente.update_layout(title_x=0.3)

#graf4_venda_cliente

# PÁGINA INICIAL
st.header(":bar_chart: DASHBOARD DE VENDAS")
st.write("---")
col1,col2,col3 = st.columns([2,2,3],gap='small')

total_vendas = round(tabel_vendas_margem['Valor Pedido'].sum(),2)
total_margem = round(tabel_vendas_margem['Margem Lucro'].sum(),2)
porc_margem = int(100*total_margem/total_vendas)

st.write("---")

with col1:
    st.metric("VENDAS TOTAIS",value=f"R${total_vendas}")
    
with col2:
    st.metric("MARGEM TOTAL",value=f"R${total_margem}")
    
with col3:
    st.metric("MARGEM",value=f"{porc_margem}%")
    
st.write(graf1_qtde_produto)
with st.expander("Análise:"):
    st.write(f"Gráfico que mostra a quantidade de vendas por produto análisando o vendedor {fVendedor} e o cliente {fCliente}")
    st.write("TABELA:")
    st.write(tabel_qtde_produto)

st.write(graf2_valor_produto)
with st.expander("Análise:"):
    st.write(f"Gráfico que mostra o valor total do produto com base no vendedor {fVendedor} e o cliente {fCliente}")
    st.write("TABELA:")
    st.write(tabel_qtde_produto)

st.write(graf3_total_vendedor)
with st.expander("Análise:"):
    st.write(f"Gráfico que mostra o valor total de venda por fornecedor de acordo com o produto: {fProduto} e o cliente: {fCliente} ")
    st.write("TABELA:")
    st.write(tabel_vendas_vendedor)

st.write(graf4_venda_cliente)
with st.expander("Análise:"):
    st.write(f"Gráfico que mostra o valor total de vendas por cliente de acordo com o produto: {fProduto} e vendedor: {fVendedor}")
    st.write("TABELA:")
    st.write(tabel_vendas_cliente)
