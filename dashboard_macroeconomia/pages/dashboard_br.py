import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import os
import get_data 
import functions


st.sidebar.title('Indicadores')

br_option = st.sidebar.selectbox('Brasil', ('Curva de Juros', 
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
    df_pib_acum = get_data.pib()[0]
    df_pib_var = get_data.pib()[1]
    fig_pib_acum = get_data.pib()[2]
    fig_pib_var = get_data.pib()[3]

    # Título
    st.title('PIB')    

    # Gráfico do PIB e dfs
    st.plotly_chart(fig_pib_acum)
    st.dataframe(df_pib_acum, width=400)
    st.plotly_chart(fig_pib_var)
    
elif br_option == 'EMBI':
    # Dados do 'EMBI'
    df_embi = get_data.embi()[0]
    fig_embi = get_data.embi()[1]
    # Título
    st.title('EMBI+')

    # Gráficos do 'EMBI'    
    st.plotly_chart(fig_embi)