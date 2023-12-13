import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import os
import get_data 
import functions

usa_option = st.sidebar.selectbox('Indicadores', (
    'Escolha um indicador', 
    'Curva de Juros', 
    'Inflação - CPI', 
    'Inflação - PCE',
    'Inflação - PPI',
    'Spread de Crédito',
    'Pedidos por Seguro-Desemprego',
    'Payroll',
    'ADP',
    'Agregados Monetários',
    'Licenças de Construção',
    'Vendas de Casas Usadas/Novas',
    'JOLTS',
    'GDP'
))

if usa_option == 'Curva de Juros':
    # Dados da 'Taxa de Juros Americana'
    df_effr = get_data.effr()[0]
    fig_effr = get_data.effr()[1]

    df_diff_10y_3mo = get_data.diff_10y_3mo()[0]
    fig_diff_10y_3mo = get_data.diff_10y_3mo()[1]

    df_diff_10y_2y = get_data.diff_10y_2y()[0]
    fig_diff_10y_2y = get_data.diff_10y_2y()[1]

    df_treasury_2y = get_data.treasury_2y()[0]
    fig_treasury_2y = get_data.treasury_2y()[1]

    fig_taxa_juros_real_usa_longa = get_data.taxa_juros_real_usa_longa()

    # Título
    st.title('Taxa de Juros Americana')

    # Gráficos da 'Taxa de Juros Americana'
    st.plotly_chart(fig_effr)
    st.plotly_chart(fig_diff_10y_3mo)
    st.plotly_chart(fig_diff_10y_2y)
    st.plotly_chart(fig_treasury_2y)
    st.plotly_chart(fig_treasury_2y)
    st.plotly_chart(fig_taxa_juros_real_usa_longa)

elif usa_option == 'Inflação - CPI':
    # Dados da 'Inflação Americana'
    df_cpi_core = get_data.cpi_core()
    df_cpi_all = get_data.cpi_all()
    df_cpi_energy = get_data.cpi_energy()
    df_cpi_housing = get_data.cpi_housing()
    df_cpi_apparel = get_data.cpi_apparel()
    df_cpi_recreation = get_data.cpi_recreation()
    df_cpi_education = get_data.cpi_education()
    df_cpi_communication = get_data.cpi_communication()
    df_cpi_medical = get_data.cpi_medical()
    df_cpi_transportation = get_data.cpi_transportation()

    # Título
    st.title('Inflação Americana - CPI')

    # Gráficos da 'Inflação Americana'
    cpi_core_fig = functions.plot_heatmap_cpi(df_cpi_core)
    st.subheader('CPI Core acumulado 12 meses')
    st.plotly_chart(cpi_core_fig)

    cpi_all_fig = functions.plot_heatmap_cpi(df_cpi_all)
    st.subheader('CPI All Items acumulado 12 meses')
    st.plotly_chart(cpi_all_fig )

    cpi_energy_fig = functions.plot_heatmap_cpi(df_cpi_energy)
    st.subheader('CPI Energy acumulado 12 meses')
    st.plotly_chart(cpi_energy_fig)

    cpi_housing_fig = functions.plot_heatmap_cpi(df_cpi_housing)
    st.subheader('CPI Housing acumulado 12 meses')
    st.plotly_chart(cpi_housing_fig)

    cpi_apparel_fig = functions.plot_heatmap_cpi(df_cpi_apparel)
    st.subheader('CPI Apparel acumulado 12 meses')
    st.plotly_chart(cpi_apparel_fig)

    cpi_recreation_fig = functions.plot_heatmap_cpi(df_cpi_recreation)
    st.subheader('CPI Recreation acumulado 12 meses')
    st.plotly_chart(cpi_recreation_fig)

    cpi_education_fig = functions.plot_heatmap_cpi(df_cpi_education)
    st.subheader('CPI Education acumulado 12 meses')
    st.plotly_chart(cpi_education_fig)

    cpi_communication_fig = functions.plot_heatmap_cpi(df_cpi_communication)
    st.subheader('CPI Communication acumulado 12 meses')
    st.plotly_chart(cpi_communication_fig)

    cpi_medical_fig = functions.plot_heatmap_cpi(df_cpi_medical)
    st.subheader('CPI Medical Care acumulado 12 meses')
    st.plotly_chart(cpi_medical_fig)

    cpi_transportation_fig = functions.plot_heatmap_cpi(df_cpi_transportation)
    st.subheader('CPI Transportation acumulado 12 meses')
    st.plotly_chart(cpi_transportation_fig)

    cpi_all_vs_cpi_core_fig = get_data.cpi_all_vs_cpi_core()
    st.plotly_chart(cpi_all_vs_cpi_core_fig)

elif usa_option == 'Inflação - PCE':
    # Dados do 'PCE'
    df_pce_core = get_data.pce()[0]
    df_pce_all = get_data.pce()[1]
    df_pce_real = get_data.pce()[2]
    fig_pce_core = get_data.pce()[3]
    fig_pce_all = get_data.pce()[4]
    fig_pce_real = get_data.pce()[5]

    # Título
    st.title('Inflação Americana - PCE')

    # Gráficos do 'PCE' e dfs
    st.plotly_chart(fig_pce_core)
    st.dataframe(df_pce_core)
    st.plotly_chart(fig_pce_all)
    st.dataframe(df_pce_all)
    st.plotly_chart(fig_pce_real)
    st.dataframe(df_pce_real)

elif usa_option == 'Inflação - PPI':
    # Dados 'PPI'
    df_ppi_final_demand = get_data.ppi()[0]
    df_ppi_goods = get_data.ppi()[1]
    df_ppi_services = get_data.ppi()[2]
    df_ppi_manu = get_data.ppi()[3]
    fig_ppi_comparacao = get_data.ppi()[4]
    fig_ppi_manu = get_data.ppi()[5]

    # Título
    st.title('Inflação Americana - PPI')

    # Gráficos do 'PPI' 
    st.plotly_chart(fig_ppi_comparacao)
    st.plotly_chart(fig_ppi_manu)

elif usa_option == 'Spread de Crédito':
    # Dados do 'Spread de Crédito Americano'
    df_spread = get_data.spread_credito()[0]
    fig_spread = get_data.spread_credito()[1]

    # Título
    st.title('Spread de Crédito Americano')
    
    # Gráficos o 'Spread de Crédito Americano'
    st.plotly_chart(fig_spread)

elif usa_option == 'Pedidos por Seguro-Desemprego':
    # Dados do 'Pedidos por Seguro-Desemprego'
    df_seguro_desemprego = get_data.pedido_seguro_desemprego()[0]
    fig_seguro_desemprego = get_data.pedido_seguro_desemprego()[1]

    # Título
    st.title('Pedidos Iniciais por Seguro-Desemprego')
    
    # Gráficos o 'Spread de Crédito Americano'
    st.plotly_chart(fig_seguro_desemprego)

elif usa_option == 'Payroll':
    # Dados do 'Pedidos por Seguro-Desemprego'
    df_payroll = get_data.payroll()[0]
    fig_payroll = get_data.payroll()[1]

    df_ganho_medio_por_hora = get_data.ganho_medio_por_hora()[0]
    fig_ganho_medio_por_hora = get_data.ganho_medio_por_hora()[1]

    df_taxa_desemprego = get_data.taxa_desemprego()[0]
    fig_taxa_desemprego = get_data.taxa_desemprego()[1]

    # Título
    st.title('Payroll')
    
    # Gráficos o 'Spread de Crédito Americano'
    st.plotly_chart(fig_payroll)
    st.plotly_chart(fig_ganho_medio_por_hora)
    st.plotly_chart(fig_taxa_desemprego)

elif usa_option == 'ADP':
    # Dados do ADP
    df_adp_us = get_data.adp()[0]
    fig_ultimo_adp = get_data.adp()[1]
    fig_var_mining = get_data.adp()[2]
    fig_var_construction = get_data.adp()[3]
    fig_var_manufacturing = get_data.adp()[4]
    fig_var_trade = get_data.adp()[5]
    fig_var_information = get_data.adp()[6]
    fig_var_financial = get_data.adp()[7]
    fig_var_professional = get_data.adp()[8]
    fig_var_education = get_data.adp()[9]
    fig_var_leisure = get_data.adp()[10]
    fig_var_other = get_data.adp()[11]

    # Título
    st.title('ADP')

    # Dfs ADP
    st.dataframe(df_adp_us)
    st.plotly_chart(fig_ultimo_adp)
    st.subheader('ADP - Histórico do Número de Contratações de Cada Setor')
    st.plotly_chart(fig_var_mining)
    st.plotly_chart(fig_var_construction)
    st.plotly_chart(fig_var_manufacturing)
    st.plotly_chart(fig_var_trade)
    st.plotly_chart(fig_var_information)
    st.plotly_chart(fig_var_financial)
    st.plotly_chart(fig_var_professional)
    st.plotly_chart(fig_var_education)
    st.plotly_chart(fig_var_leisure)
    st.plotly_chart(fig_var_other)
    
elif usa_option == 'Agregados Monetários':
    # Dados dos 'Agregados Monetários'
    df_m1 = get_data.agregados_monetarios()[0]
    df_m2 = get_data.agregados_monetarios()[1]
    fig_m1_m2 = get_data.agregados_monetarios()[2]

    # Título
    st.title('Agregados Monetários')

    # Gráfico dos 'Agregados Monetários'
    st.plotly_chart(fig_m1_m2)

elif usa_option == 'Licenças de Construção':
    # Dados das 'Licenças de Construção'
    df_building_permits = get_data.licencas_construcao()[0]
    fig_building_permits = get_data.licencas_construcao()[1]

    # Título
    st.title('Licenças de Construção')

    # Gráfico dos 'Licenças de Construção'
    st.plotly_chart(fig_building_permits)

elif usa_option == 'Vendas de Casas Usadas/Novas':
    # Dados das vendas de 'casas usadas (Existing Home Sales)' e de 'casas novas (New Home Sales)'
    df_casas_usadas = get_data.vendas_casas()[0]
    df_casas_novas = get_data.vendas_casas()[1]
    fig_casas_usadas = get_data.vendas_casas()[2]
    fig_casas_novas = get_data.vendas_casas()[3]

    # Título
    st.title('Vendas de Casas Usadas/Novas')

    # Gráfico dos 'Licenças de Construção'
    st.plotly_chart(fig_casas_usadas)
    st.plotly_chart(fig_casas_novas)

elif usa_option == 'JOLTS':
    # Dados do 'JOLTS'
    df_jolts = get_data.jolts()[0]
    fig_jolts = get_data.jolts()[1]

    # Título
    st.title('JOLTS')

    # Gráfico dos 'JOLTS'
    st.plotly_chart(fig_jolts)

elif usa_option == 'GDP':
    # Dados do GDP
    fig_var_gdp = get_data.gdp()

    # Título
    st.title('GDP')

    # Gráfico do GDP
    st.plotly_chart(fig_var_gdp)
