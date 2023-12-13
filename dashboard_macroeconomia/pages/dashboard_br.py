import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import os
import get_data 
import functions


st.sidebar.title('Indicadores')

br_option = st.sidebar.selectbox('Brasil', (
    'Escolha um indicador',
    'Curva de Juros', 
    'Inflação',
    'CAGED',
    'PNAD Contínua',
    'Expectativas FOCUS',
    'PIB',
    'EMBI'
))

if br_option == 'Curva de Juros':
    # Título
    st.title('Curva de Juros')

elif br_option == 'Inflação':
    # Dados do 'IPCA'
    df_ipca = get_data.ipca()[0]
    df_ipca_anual = get_data.ipca()[1]
    fig_ipca_acumulado = get_data.ipca()[2]
    fig_ipca_anual = get_data.ipca()[3]
    tj_real = get_data.ipca()[4]

    # Título
    st.title('Inflação Brasileiro')

    # Gráficos do 'IPCA' e dfs
    st.plotly_chart(fig_ipca_acumulado)
    st.dataframe(df_ipca)
    st.plotly_chart(fig_ipca_anual)
    st.dataframe(df_ipca_anual)

    # Texto da 'Taxa de Juros Real'
    st.subheader('Taxa de Juros Real')
    st.write(f'- A taxa de juros real é de {round(tj_real, 3)}%')

elif br_option == 'CAGED':
    # Dados do 'CAGED'
    df_admissoes = get_data.caged()[0]
    df_demissoes = get_data.caged()[1]
    df_saldos = get_data.caged()[2]
    fig_admissoes = get_data.caged()[3]
    fig_demissoes = get_data.caged()[4]
    fig_saldos = get_data.caged()[5]

    # Título
    st.title('CAGED')

    # Gráficos do 'CAGED'
    st.plotly_chart(fig_admissoes)
    st.plotly_chart(fig_demissoes)
    st.plotly_chart(fig_saldos)

elif br_option == 'PNAD Contínua':
    # Dados do 'PNAD'
    fig_taxa_desocupacao = get_data.pnad()[0]
    fig_taxa_desocupacao_tri = get_data.pnad()[1]
    fig_taxa_desocupação_sexo = get_data.pnad()[2]
    fig_taxa_desocupação_idade = get_data.pnad()[3]
    fig_idade_trabalho = get_data.pnad()[4]
    fig_nivel_ocupacao = get_data.pnad()[5]

    # Título
    st.title('PNAD Contínua')

    # Gráficos do 'PNAD'
    st.plotly_chart(fig_taxa_desocupacao)
    st.plotly_chart(fig_taxa_desocupacao_tri)
    st.plotly_chart(fig_taxa_desocupação_sexo)
    st.plotly_chart(fig_taxa_desocupação_idade)
    st.plotly_chart(fig_idade_trabalho)
    st.plotly_chart(fig_nivel_ocupacao)

elif br_option == 'Expectativas FOCUS':
    # Dados 'Expectativas FOCUS'
    df_ipca_expec = get_data.expectativa_focus()[0]
    df_selic_expec = get_data.expectativa_focus()[1]
    df_pib_expec = get_data.expectativa_focus()[2]
    df_cambio_expec = get_data.expectativa_focus()[3]
    fig_ipca_expec = get_data.expectativa_focus()[4]
    fig_selic_expec = get_data.expectativa_focus()[5]
    fig_pib_expec = get_data.expectativa_focus()[6]
    fig_cambio_expec = get_data.expectativa_focus()[7]

    # Título
    st.title('Expectativas FOCUS')

    # Gráficos das 'Expectativas FOCUS'
    st.plotly_chart(fig_ipca_expec)
    st.plotly_chart(fig_selic_expec)
    st.plotly_chart(fig_pib_expec)
    st.plotly_chart(fig_cambio_expec)

elif br_option == 'PIB':
    # Dados PIB
    fig_var_pib_trimestral = get_data.variacao_pib_trimestral()
    fig_var_pib_anual = get_data.variacao_pib_anual()
    fig_var_fbcf_trimestral = get_data.variacao_fbcf_trimestral()
    fig_var_fbcf_anual = get_data.variacao_fbcf_anual()
    fig_var_desp_familia_trimestral = get_data.variacao_desp_familia_trimestral()
    fig_var_desp_familia_anual = get_data.variacao_desp_familia_anual()
    fig_var_governo_trimestral = get_data.variacao_governo_trimestral()
    fig_var_governo_anual = get_data.variacao_governo_anual()
    fig_variacao_acumulada_pib_consumo_fbcf = get_data.variacao_acumulada_pib_consumo_fbcf()
    fig_otica_producao = get_data.otica_producao_demanda()[0]
    fig_otica_demanda = get_data.otica_producao_demanda()[1]
    fig_exportacoes_importacoes = get_data.exportacoes_importacoes()[0]
    fig_saldo_balanca_comercial = get_data.exportacoes_importacoes()[1]

    # Título
    st.title('PIB')    

    # Gráficos do PIB
    st.plotly_chart(fig_var_pib_trimestral)
    st.plotly_chart(fig_var_pib_anual)
    st.markdown('***')
    st.plotly_chart(fig_var_fbcf_trimestral)
    st.plotly_chart(fig_var_fbcf_anual)
    st.markdown('***')
    st.plotly_chart(fig_var_desp_familia_trimestral)
    st.plotly_chart(fig_var_desp_familia_anual)
    st.markdown('***')
    st.plotly_chart(fig_var_governo_trimestral)
    st.plotly_chart(fig_var_governo_anual)
    st.markdown('***')
    st.plotly_chart(fig_variacao_acumulada_pib_consumo_fbcf)
    st.markdown('***')
    st.plotly_chart(fig_otica_producao)
    st.plotly_chart(fig_otica_demanda)
    st.markdown('***')
    st.plotly_chart(fig_exportacoes_importacoes)
    st.plotly_chart(fig_saldo_balanca_comercial)

elif br_option == 'EMBI':
    # Dados do 'EMBI'
    df_embi = get_data.embi()[0]
    fig_embi = get_data.embi()[1]
    # Título
    st.title('EMBI+')

    # Gráficos do 'EMBI'    
    st.plotly_chart(fig_embi)