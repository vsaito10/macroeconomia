import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import requests
import json
import functions
from fredapi import Fred
import ipeadatapy


# USA
fred = Fred(api_key=os.environ.get('FREDAPI_KEY'))

# Curva de Juros Americana
@st.cache_data
def effr():
    # Effective Federal Funds Rate
    effr = fred.get_series('EFFR')

    df = pd.DataFrame({'effr': effr})
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['effr'],
        mode='lines'
    ))

    # Mostre a data completa no quadro dinâmica do plotly
    fig.update_xaxes(tickformat='%Y-%m-%d')

    fig.update_layout(
        title='Effective Federal Funds Rate',
        xaxis_title='Years',
        yaxis_title='Percent',
        template='seaborn'
    )

    return df, fig


@st.cache_data
def diff_10y_3mo():
    # 10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity
    df = fred.get_series('T10Y3M')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df,
        mode='lines'
    ))

    fig.add_hline(y=0, line_width=1, line_color='red')

    # Mostre a data completa no quadro dinâmica do plotly
    fig.update_xaxes(tickformat='%Y-%m-%d')

    fig.update_layout(
        title='10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity',
        xaxis_title='Years',
        yaxis_title='Percent',
        template='seaborn'
    )

    return df, fig


@st.cache_data
def diff_10y_2y():
    # 10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity
    df = fred.get_series('T10Y2Y')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df,
        mode='lines'
    ))

    fig.add_hline(y=0, line_width=1, line_color='red')

    # Mostre a data completa no quadro dinâmica do plotly
    fig.update_xaxes(tickformat='%Y-%m-%d')

    fig.update_layout(
        title='10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity',
        xaxis_title='Years',
        yaxis_title='Percent',
        template='seaborn'
    )

    return df, fig


@st.cache_data
def treasury_2y():
    # 2-Year Treasury Constant Maturity - https://fred.stlouisfed.org/series/DGS2
    df = fred.get_series('DGS2')
    df = df.loc['2000':]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df,
        mode='lines'
    ))

    fig.add_hline(y=5, line_width=1, line_color='red')

    # Mostre a data completa no quadro dinâmica do plotly
    fig.update_xaxes(tickformat='%Y-%m-%d')

    fig.update_layout(
        title='2-Year Treasury Constant Maturity - Above 5%',
        xaxis_title='Years',
        yaxis_title='Percent',
        template='seaborn'
    )

    return df, fig


@st.cache_data
def taxa_juros_real_usa_longa():
    # 5-Year Treasury Constant Maturity 
    df_t5y = fred.get_series('DGS5')
    df_t5y = df_t5y.loc['2008':]

    # 5-Year Constant Maturity, Quoted on an Investment Basis, Inflation-Indexed
    df_5y_inflation = fred.get_series('DFII5')
    df_5y_inflation = df_5y_inflation.loc['2008':]

    if df_t5y.shape == df_5y_inflation.shape:
        # Juntando os dois dfs
        juros_real_us_5y = pd.concat([df_t5y, df_5y_inflation], axis=1)
        # Renomeando as colunas
        juros_real_us_5y = juros_real_us_5y.rename(
            columns={0: 'taxa_juros_nominal_5y', 1: 'inflacao_5y'})
        # Calculando a taxa de juros real
        juros_real_us_5y['taxa_juros_real_5y'] = round(
            ((((juros_real_us_5y['taxa_juros_nominal_5y'] / 100) + 1) / ((juros_real_us_5y['inflacao_5y'] / 100) + 1)) - 1) * 100, 2)

    # 10-Year Treasury Constant Maturity
    df_t10y = fred.get_series('DGS10')
    df_t10y = df_t10y.loc['2008':]

    # 10-Year Constant Maturity, Quoted on an Investment Basis, Inflation-Indexed
    df_10y_inflation = fred.get_series('DFII10')
    df_10y_inflation = df_10y_inflation.loc['2008':]

    if df_t10y.shape == df_10y_inflation.shape:
        # Juntando os dois dfs
        juros_real_us_10y = pd.concat([df_t10y, df_10y_inflation], axis=1)
        # Renomeando as colunas
        juros_real_us_10y = juros_real_us_10y.rename(
            columns={0: 'taxa_juros_nominal_10y', 1: 'inflacao_10y'})
        # Calculando a taxa de juros real
        juros_real_us_10y['taxa_juros_real_10y'] = round(
            ((((juros_real_us_10y['taxa_juros_nominal_10y'] / 100) + 1) / ((juros_real_us_10y['inflacao_10y'] / 100) + 1)) - 1) * 100, 2)

    # Plotando o juros real americano
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=juros_real_us_5y.index,
        y=juros_real_us_5y['taxa_juros_real_5y'],
        mode='lines',
        name='taxa_juros_real_5y'
    ))

    fig.add_trace(go.Scatter(
        x=juros_real_us_10y.index,
        y=juros_real_us_10y['taxa_juros_real_10y'],
        mode='lines',
        name='taxa_juros_real_10y'
    ))

    fig.add_hline(y=0, line_width=2, line_color='red')

    # Mostre a data completa no quadro dinâmica do plotly
    fig.update_xaxes(tickformat='%Y-%m-%d')

    fig.update_layout(
        title='Comparação entre a Taxa de Juros Real USA (5y e 10y)',
        xaxis_title='Anos',
        yaxis_title='Porcentagem',
        template='seaborn'
    )

    return fig


# Inflação Americana (CPI)
@st.cache_data
def cpi_core():
    df = functions.data_bls(series_id=['CUUR0000SA0L1E'], 
                            start_year=2015, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )
    return df


@st.cache_data
def cpi_all():
    df = functions.data_bls(series_id=['CUUR0000SA0'], 
                            start_year=2015, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )
    return df


@st.cache_data
def cpi_energy():
    df = functions.data_bls(series_id=['CUUR0000SA0E'], 
                            start_year=2015, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )
    return df


@st.cache_data
def cpi_housing():
    df = functions.data_bls(series_id=['CUUR0000SAH'], 
                            start_year=2015, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )
    return df


@st.cache_data
def cpi_apparel():
    df = functions.data_bls(series_id=['CUUR0000SAA'], 
                            start_year=2015, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )
    return df


@st.cache_data
def cpi_recreation():
    df = functions.data_bls(series_id=['CUUR0000SAR'], 
                            start_year=2015, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )
    return df


@st.cache_data
def cpi_education():
    df = functions.data_bls(series_id=['CUUR0000SAE1'], 
                            start_year=2015, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )
    return df


@st.cache_data
def cpi_communication():
    df = functions.data_bls(series_id=['CUUR0000SAE2'], 
                            start_year=2015, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )
    return df


@st.cache_data
def cpi_medical():
    df = functions.data_bls(series_id=['CUUR0000SAM'], 
                            start_year=2015, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )
    return df


@st.cache_data
def cpi_transportation():
    df = functions.data_bls(series_id=['CUUR0000SAT'], 
                            start_year=2015, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )
    return df


@st.cache_data
def cpi_all_vs_cpi_core():
    df_cpi_core = cpi_core()
    df_cpi_all = cpi_all()

    # Comparando a variação dos últimos 12 meses 'CPI all' vs 'CPI all items less food and energy'
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_cpi_all.index,
        y=df_cpi_all['pct_change_ultimo_12_meses'],
        mode='lines',
        name='CPI all'
    ))

    fig.add_trace(go.Scatter(
        x=df_cpi_core.index,
        y=df_cpi_core['pct_change_ultimo_12_meses'],
        mode='lines',
        name='CPI less f/e'
    ))

    fig.update_layout(
        title='Gráfico CPI all items vs CPI Core',
        xaxis_title='Anos',
        yaxis_title='CPI',
        template='seaborn'
    )

    return fig


# Inflação Americana (PCE)
@st.cache_data
def pce():
    # PCE Excluding Food and Energy (mensal)
    pce_core = fred.get_series('PCEPILFE')
    # Criando o df
    df_pce_core = pd.DataFrame(pce_core, columns=['value'])
    # Calculando a variação percentual
    df_pce_core['pct_change'] = round(df_pce_core['value'].pct_change(), 6) * 100

    # Plotando o PCE Excluding Food and Energy
    fig_pce_core = go.Figure()

    fig_pce_core.add_trace(go.Scatter(
        x=df_pce_core.index,
        y=df_pce_core['value'],
        mode='lines'
    ))

    fig_pce_core.update_layout(
        title='PCE Excluding Food and Energy',
        xaxis_title='Years',
        yaxis_title='Billions of Dollars',
        template='seaborn'
    )

    # PCE (mensal)
    pce_all = fred.get_series('PCE')
    # Criando o df
    df_pce_all = pd.DataFrame(pce_all, columns=['value'])
    # Calculando a variação percentual
    df_pce_all['pct_change'] = round(df_pce_all['value'].pct_change(), 6) * 100

    # Plotando o PCE
    fig_pce_all = go.Figure()

    fig_pce_all.add_trace(go.Scatter(
        x=df_pce_all.index,
        y=df_pce_all['value'],
        mode='lines'
    ))

    fig_pce_all.update_layout(
        title='PCE',
        xaxis_title='Years',
        yaxis_title='Billions of Dollars',
        template='seaborn'
    )

    # Real PCE (mensal)
    pce_real = fred.get_series('PCEC96', observation_start='2002-02-01')
    # Criando o df
    df_pce_real = pd.DataFrame(pce_real, columns=['value'])
    # Calculando a variação percentual
    df_pce_real['pct_change'] = round(df_pce_real['value'].pct_change(), 6) * 100

    # Plotando o PCE real
    fig_pce_real = go.Figure()

    fig_pce_real.add_trace(go.Scatter(
        x=df_pce_real.index,
        y=df_pce_real['value'],
        mode='lines'
    ))

    fig_pce_real.update_layout(
        title='PCE Real',
        xaxis_title='Years',
        yaxis_title='Billions of Dollars',
        template='seaborn'
    )

    return df_pce_core, df_pce_all, df_pce_real, fig_pce_core, fig_pce_all, fig_pce_real


# Inflação Americana (PPI)
@st.cache_data
def ppi():
    # PPI commodity data for final demand, seasonally adjusted
    df_ppi_final_demand = functions.data_bls(series_id=['WPSFD4'], 
                                          start_year=2010, 
                                          end_year=2023, 
                                          api_key=os.environ.get('BSLAPI_KEY')
    )
    # PPI final demand goods
    df_ppi_goods = functions.data_bls(series_id=['WPUFD41'], 
                                   start_year=2010, 
                                   end_year=2023, 
                                   api_key=os.environ.get('BSLAPI_KEY')
    )
    # PPI final demand services
    df_ppi_services = functions.data_bls(series_id=['WPUFD42'], 
                                      start_year=2010, 
                                      end_year=2023, 
                                      api_key=os.environ.get('BSLAPI_KEY')
    )

    # Gráfico Comparação da Variação Percentual dos PPI Final Demands
    fig_ppi_comparacao = go.Figure()
    fig_ppi_comparacao.add_trace(go.Scatter(
        x=df_ppi_final_demand.index,
        y=df_ppi_final_demand['pct_change'],
        mode='lines',
        name='PPI Final Demand'
    ))

    fig_ppi_comparacao.add_trace(go.Scatter(
        x=df_ppi_goods.index,
        y=df_ppi_goods['pct_change'],
        mode='lines',
        name='PPI Final Demand Goods'
    ))

    fig_ppi_comparacao.add_trace(go.Scatter(
        x=df_ppi_services.index,
        y=df_ppi_services['pct_change'],
        mode='lines',
        name='PPI Final Demand Services'
    ))

    fig_ppi_comparacao.add_hline(
        y=0,
        line_width=2,
        line_color='black',
        line_dash="dash"
    )

    fig_ppi_comparacao.update_layout(
        title='Gráfico Comparação da Variação Percentual dos PPI Final Demands',
        xaxis_title='Anos',
        yaxis_title='PPI Final Demands',
        template='seaborn'
    )

    # PPI total manufacturing industries
    df_ppi_manu = functions.data_bls(series_id=['PCUOMFG--OMFG--'], 
                                        start_year=2010, 
                                        end_year=2023, 
                                        api_key=os.environ.get('BSLAPI_KEY')
    )

    # Gráfico Comparação da Variação Percentual do PPI total manufacturing industries
    fig_ppi_manu = go.Figure()
    fig_ppi_manu.add_trace(go.Scatter(
        x=df_ppi_manu.index,
        y=df_ppi_manu['pct_change'],
        mode='lines',
        name='Total Manufacturing Industries'
    ))

    fig_ppi_manu.add_hline(
        y=0,
        line_width=2,
        line_color='black',
        line_dash="dash"
    )

    fig_ppi_manu.update_layout(
        title='Gráfico Variação Percentual do PPI Total Manufacturing Industries',
        xaxis_title='Anos',
        yaxis_title='PPI Total Manufacturing Industries',
        template='seaborn'
    )

    return df_ppi_final_demand, df_ppi_goods, df_ppi_services, df_ppi_manu, fig_ppi_comparacao, fig_ppi_manu 


# Spreads de Crédito
@st.cache_data
def spread_credito():
    # ICE BofA US High Yield Index Option-Adjusted Spread
    df = fred.get_series('BAMLH0A0HYM2')

    # Criando o df
    df_spread = pd.DataFrame(df, columns=['value'])

    # Calculando a variação percentual
    df_spread['pct_change'] = df_spread['value'].pct_change()

    # Plotando o df do spread
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_spread.index,
        y=df_spread['value'],
        mode='lines',
        name='Spread de Crédito'
    ))

    # Adicionando uma linha horizontal da média do spread de crédito
    fig.add_hline(y=df_spread['value'].mean(), line_width=1, line_color='red')

    fig.update_layout(
        title='Spread de Crédito entre os Bonds High Yield e a Taxa Livre de Risco (spot Treasury)',
        xaxis_title='Anos',
        yaxis_title='Porcentagem'
    )

    return df_spread, fig


# Pedidos Iniciais por Seguro-Desemprego
@st.cache_data
def pedido_seguro_desemprego():
    # Unemployment Insurance Weekly Claims Report
    df = fred.get_series('ICSA')

    # Criando o df
    df = pd.DataFrame(df, columns=['value'])

    # Calculando a variação percentual
    df['pct_change'] = df['value'].pct_change()

    # Plotando o gráfico de linha do 'Unemployment Insurance Weekly Claims Report'
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['value'],
        mode='lines'
    ))

    # Adicionando uma linha horizontal da média do 'Unemployment Insurance Weekly Claims Report'
    fig.add_hline(y=df['value'].mean(), line_width=1, line_color='red')

    fig.update_layout(
        title='Unemployment Insurance Weekly Claims',
        xaxis_title='Years',
        yaxis_title='Percent',
        template='seaborn')

    return df, fig


# Payroll
@st.cache_data
def payroll():
    # Total Nonfarm Employment
    df = functions.data_bls(series_id=['CES0000000001'], 
                            start_year=2012, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )

    # A diferença entre os meses é o número do Payroll que é mostrado nos relatórios
    df['diff'] = df['value'].diff()

    # Criando subplots com 2 linhas e 1 colunas
    fig = make_subplots(rows=2,
                        cols=1,
                        subplot_titles=('Total Nonfarm Payroll',
                                        'Diff Payroll'
                                        ))

    # Adicionando traces (gráficos) aos subplots
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['value'],
        name='Total Nonfarm Payroll'
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['diff'],
        name='Diff Payroll'
    ), row=2, col=1)

    # Atualizando os layout dos subplots
    fig.update_layout(
        height=1000,
        width=1500,
        title_text="Relatório Payroll",
        xaxis_title='Year',
        yaxis_title='Thousands of Persons'
    )

    # Colocando a legenda dos eixos 'x' e 'y' no segundo plot
    fig.update_xaxes(title_text='Year', row=2, col=1)
    fig.update_yaxes(title_text='Thousands of Persons', row=2, col=1)

    return df, fig


# Private Average Hourly Earnings of All Employees
@st.cache_data
def ganho_medio_por_hora():
    df = functions.data_bls(series_id=['CES0500000003'], 
                            start_year=2012, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )

    # Plotando o 'Total Private Average Hourly Earnings of All Employees'
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df.index,
        y=round(df['pct_change'], 1)
    ))

    # Adicionando uma linha horizontal da média do 'pct_change' do 'Total Private Average Hourly Earnings of All Employees'
    fig.add_hline(y=df['pct_change'].mean(), line_width=1, line_color='red')

    fig.update_layout(
        title='Total Private Average Hourly Earnings of All Employees',
        xaxis_title='Years',
        yaxis_title='Percent',
        template='seaborn')

    return df, fig


# Taxa de desemprego
@st.cache_data
def taxa_desemprego():
    df = functions.data_bls(series_id=['LNS14000000'], 
                            start_year=2012, 
                            end_year=2023, 
                            api_key=os.environ.get('BSLAPI_KEY')
    )
    df = df[['value']]

    # Plotando o 'Unemployment Rate'
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['value'],
        mode='lines'
    ))

    fig.update_layout(
        title='Unemployment Rate',
        xaxis_title='Years',
        yaxis_title='Percent',
        template='seaborn')

    return df, fig


# ADP
@st.cache_data
def adp():
    # Total Nonfarm Private Payroll Employment
    adp_us = fred.get_series('ADPMNUSNERSA')

    # Transformando em um df
    df_adp_us = pd.DataFrame(adp_us, columns=['value'])

    # A diferença entre os meses é o número do ADP que é mostrado nos relatórios
    df_adp_us['diff'] = df_adp_us['value'].diff()

    # Setores que o ADP monitora
    # Nonfarm Private Payroll Employment for Natural Resources and Mining
    adp_mining = fred.get_series('ADPMINDNRMINNERSA')
    # Nonfarm Private Payroll Employment for Construction
    adp_construction = fred.get_series('ADPMINDCONNERSA')
    # Nonfarm Private Payroll Employment for Manufacturing
    adp_manufacturing = fred.get_series('ADPMINDMANNERSA')
    # Nonfarm Private Payroll Employment for Trade, Transportation, and Utilities
    adp_trade = fred.get_series('ADPMINDTTUNERSA')
    # Nonfarm Private Payroll Employment for Information
    adp_information = fred.get_series('ADPMINDINFONERSA')
    # Nonfarm Private Payroll Employment for Financial Activities
    adp_financial = fred.get_series('ADPMINDFINNERSA')
    # Nonfarm Private Payroll Employment for Professional and Business Services
    adp_professional = fred.get_series('ADPMINDPROBUSNERSA')
    # Nonfarm Private Payroll Employment for Education and Health Services
    adp_education = fred.get_series('ADPMINDEDHLTNERSA')
    # Nonfarm Private Payroll Employment for Leisure and Hospitality
    adp_leisure = fred.get_series('ADPMINDLSHPNERSA')
    # Nonfarm Private Payroll Employment for Other Services
    adp_other = fred.get_series('ADPMINDOTHSRVNERSA')

    adp_setores = pd.concat([
        adp_mining,
        adp_construction,
        adp_manufacturing,
        adp_trade,
        adp_information,
        adp_financial,
        adp_professional,
        adp_education,
        adp_leisure,
        adp_other], axis=1)

    adp_setores = adp_setores.rename(columns={
        0: 'mining',
        1: 'construction',
        2: 'manufacturing',
        3: 'trade',
        4: 'information',
        5: 'financial',
        6: 'professional',
        7: 'education',
        8: 'leisure',
        9: 'other'
    })

    # Calculando a diferença entre os meses de cada setor
    df_adp_setores = adp_setores.diff().dropna()

    # Último dado (última linha) do df dos setores monitorados pelo ADP
    ultimo_adp = df_adp_setores.iloc[-1]
    # Rank dos setores que mais contrataram
    df_adp_setores_rank = pd.DataFrame(ultimo_adp.sort_values(ascending=False))

    return df_adp_us, df_adp_setores, df_adp_setores_rank


# Agregados monetários
@st.cache_data
def agregados_monetarios():
    # M1 (agregado monetario)
    m1 = fred.get_series('WM1NS')
    # Criando o df
    df_m1 = pd.DataFrame(m1, columns=['value'])
    # Calculando a variação percentual
    df_m1['pct_change'] = df_m1['value'].pct_change()

    # M2 (agregado monetario)
    m2 = fred.get_series('WM2NS')
    # Criando o df
    df_m2 = pd.DataFrame(m2, columns=['value'])
    # Calculando a variação percentual
    df_m2['pct_change'] = df_m2['value'].pct_change()

    # Plotando o df
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_m1.index,
        y=df_m1['value'],
        mode='lines',
        name='M1'
    ))

    fig.add_trace(go.Scatter(
        x=df_m2.index,
        y=df_m2['value'],
        mode='lines',
        name='M2'
    ))

    fig.update_layout(
        title='Comparação dos Agregados Monetários - M1 e M2',
        xaxis_title='Anos',
        yaxis_title='Billions of Dollars'
    )

    return df_m1, df_m2, fig


# Licenças de construção
@st.cache_data
def licencas_construcao():
    # Building Permits
    building_permits = fred.get_series('PERMIT')
    # Criando o df
    df = pd.DataFrame(building_permits, columns=['value'])
    # Calculando a variação percentual
    df['pct_change'] = df['value'].pct_change()

    # Plotando o df
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['value'],
        mode='lines',
        name='Building Permits'
    ))

    fig.update_layout(
        title='Building Permits',
        xaxis_title='Anos',
        yaxis_title='Thousands of Units'
    )

    return df, fig


# Vendas de casas usadas/novas
@st.cache_data
def vendas_casas():
    # Vendas de casas usadas (Existing Home Sales)
    casas_usadas = fred.get_series('EXHOSLUSM495S')
    # Criando o df
    df_casas_usadas = pd.DataFrame(casas_usadas, columns=['value'])
    # Calculando a variação percentual
    df_casas_usadas['pct_change'] = df_casas_usadas['value'].pct_change()

    # Plotando o df das vendas de casas usadas
    fig_casas_usadas = go.Figure()

    fig_casas_usadas.add_trace(go.Scatter(
        x=df_casas_usadas.index,
        y=df_casas_usadas['value'],
        mode='lines'
    ))

    fig_casas_usadas.update_layout(
        title='Vendas de Casas Usadas',
        xaxis_title='Anos',
        yaxis_title='Número das Unidades'
    )

    # Vendas de Casas Novas (New Home Sales)
    casas_novas = fred.get_series('NHSDPTS')
    # Criando o df
    df_casas_novas = pd.DataFrame(casas_novas, columns=['value'])
    # Calculando a variação percentual
    df_casas_novas['pct_change'] = df_casas_novas['value'].pct_change()

    # Plotando o df das vendas de casas novas
    fig_casas_novas = go.Figure()

    fig_casas_novas.add_trace(go.Scatter(
        x=df_casas_novas.index,
        y=df_casas_novas['value'],
        mode='lines',
        name='Vendas de Casas Novas'
    ))

    fig_casas_novas.update_layout(
        title='Vendas de Casas Novas',
        xaxis_title='Anos',
        yaxis_title='Milhares de Unidades'
    )

    return df_casas_usadas, df_casas_novas, fig_casas_usadas, fig_casas_novas


# JOLTS (job openings)
@st.cache_data
def jolts():
    df = functions.data_bls(series_id=['JTS000000000000000JOL'], 
                                  start_year=2012, 
                                  end_year=2023, 
                                  api_key=os.environ.get('BSLAPI_KEY')
    )

    # Plotando o JOLTS
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['value'],
        mode='lines',
        name='Empregos'
    ))

    fig.update_layout(
        title="Job Openings and Labor Turnover Survey",
        xaxis_title="Meses",
        yaxis_title="Empregos Abertos"
    )

    return df, fig


# BRASIL

# Inflação IPCA
@st.cache_data
def ipca():
    # Dados IPCA mensais
    df_ipca = functions.data_bcb(433)
    # Meta da Inflação
    meta_inflacao = functions.data_bcb(13521)
    # Criando as colunas: 'intervalo', 'banda_superior', 'banda_inferior' da inflação
    meta_inflacao['intervalo'] = [
        2, 2, 2, 2, 2.5,           #1999, 2000, 2001, 2002, 2003
        5.5, 2.5, 2, 2, 2,         #2004, 2005, 2006, 2007, 2008
        2, 2, 2, 2, 2,             #2009, 2010, 2011, 2012, 2013
        2, 2, 2, 1.5, 1.5,         #2014, 2015, 2016, 2017, 2018
        1.5, 1.5, 1.5, 1.5, 1.5,   #2019, 2020, 2021, 2022, 2023
        1.5, 1.5                   #2024, 2025                                
    ]
    meta_inflacao['banda_superior'] = meta_inflacao['valor'] + meta_inflacao['intervalo']
    meta_inflacao['banda_inferior'] = meta_inflacao['valor'] - meta_inflacao['intervalo']
    # Calculando o IPCA acumulado dos últimos 12 meses
    df_ipca['taxa_unit'] = (df_ipca / 100) + 1
    df_ipca['ipca_acumulado'] = round((df_ipca['taxa_unit'].rolling(window=12).agg(lambda x : x.prod()) -1) * 100, 2)
    # O IPCA começa nos anos 1980, mas quero a partir do ano 1999 para que eu consiga juntar com os dados da meta da inflação (começa em 1999)
    df_ipca['ipca_acumulado'] = df_ipca['ipca_acumulado'].loc['1999-01-01':]
    # Criando um ipca acumulado sem os NaN p/ fazer o plot mais bonito. Se eu deixo os NaN, não bate o index com o ipca acumulado, ficando um gráfico maior sem necessidade
    ipca_acumludado_filt = df_ipca['ipca_acumulado'].dropna()

    # Gráfico da meta de inflação com o IPCA acumulado 12
    fig_ipca_acumulado = go.Figure()

    fig_ipca_acumulado.add_trace(go.Scatter(
        x=ipca_acumludado_filt.index,
        y=ipca_acumludado_filt,
        mode='lines',
        name='IPCA Acumulado'
    ))

    fig_ipca_acumulado.add_trace(go.Scatter(
        x=meta_inflacao.index,
        y=meta_inflacao['banda_inferior'],
        mode='lines',
        name='Banda Inferior',
        line=dict(color='red', dash='dashdot')
    ))

    fig_ipca_acumulado.add_trace(go.Scatter(
        x=meta_inflacao.index,
        y=meta_inflacao['banda_superior'],
        mode='lines',
        name='Banda Superior',
        line=dict(color='red', dash='dashdot')
    ))

    fig_ipca_acumulado.add_trace(go.Scatter(
        x=meta_inflacao.index,
        y=meta_inflacao['valor'],
        mode='lines',
        name='Meta Inflação',
        line=dict(color='red')
    ))

    fig_ipca_acumulado.update_layout(
        title='Gráfico da meta da inflação com o IPCA acumulado 12 meses',
        xaxis_title='Anos',
        yaxis_title='IPCA Acumulado',
        template='seaborn'
    )

    # Calculando o IPCA anual
    ipca_unit_anual = df_ipca['taxa_unit'].resample('Y')
    ipca_anual = round(ipca_unit_anual.agg(lambda x : x.prod() - 1)*100, 2)
    df_ipca_anual = pd.DataFrame(ipca_anual)
    df_ipca_anual = df_ipca_anual.rename(columns={'taxa_unit':'value'})
    # Como de 1980 a 1994 tinha hiperflação, eu cortei esses anos para não bagunçar a escala do gráfico
    df_ipca_anual_cortado = df_ipca_anual['1995-12-31':]

    # Tabela do IPCA anual
    fig_ipca_anual = go.Figure()

    fig_ipca_anual.add_trace(go.Bar(
        x=df_ipca_anual_cortado.index,
        y=df_ipca_anual_cortado['value']
    ))

    fig_ipca_anual.update_layout(
        title='IPCA Anual', 
        xaxis_title='Data', 
        yaxis_title='IPCA', 
        template='seaborn'
    )

    # Meta Selic
    selic = functions.data_bcb(432)
    # Selecionando a última Meta Selic
    ultima_selic = selic['valor'].iloc[-1]
    # Selecionando o último IPCA
    ultimo_ipca = df_ipca['ipca_acumulado'].iloc[-1]
    # Calculando a Taxa de Juros Real (Taxa de Juros Nominal - Inflação)
    tj_real = (((1 + (ultima_selic/100)) / (1 + (ultimo_ipca/100))) - 1) * 100 

    return df_ipca, df_ipca_anual, fig_ipca_acumulado, fig_ipca_anual, tj_real


# CAGED
@st.cache_data
def caged():
    # Novo CAGED - Admissões
    df_admissoes = ipeadatapy.timeseries('CAGED12_ADMISN12')
    # Renomeando a coluna 'VALUE (Pessoa)'
    df_admissoes = df_admissoes.rename(columns={'VALUE (Pessoa)': 'admissoes'})
    # Selecionando a principal coluna
    df_admissoes = df_admissoes[['admissoes']]

    # Gráfico Admissões
    fig_admissoes = go.Figure()

    fig_admissoes.add_trace(go.Bar(
        x=df_admissoes.index,
        y=df_admissoes['admissoes']
    ))

    fig_admissoes.update_layout(
        title='Admissões', 
        xaxis_title='Data', 
        yaxis_title='Admissões', 
        template='seaborn'
    )

    # Novo CAGED - Demissões
    df_demissoes = ipeadatapy.timeseries('CAGED12_DESLIGN12')
    # Renomeando a coluna 'VALUE (Pessoa)'
    df_demissoes = df_demissoes.rename(columns={'VALUE (Pessoa)': 'demissoes'})
    # Selecionando a principal coluna
    df_demissoes = df_demissoes[['demissoes']]

    # Gráfico demissões
    fig_demissoes = go.Figure()

    fig_demissoes.add_trace(go.Bar(
        x=df_demissoes.index,
        y=df_demissoes['demissoes']
    ))

    fig_demissoes.update_layout(
        title='Demissões', 
        xaxis_title='Data', 
        yaxis_title='Demissões', 
        template='seaborn'
    )

    # Novo CAGED - Saldo
    df_saldo = ipeadatapy.timeseries('CAGED12_SALDON12')
    # Renomeando a coluna 'VALUE (Pessoa)'
    df_saldo = df_saldo.rename(columns={'VALUE (Pessoa)': 'saldo'})
    # Selecionando a principal coluna
    df_saldo = df_saldo[['saldo']]

    # Gráfico saldo
    fig_saldo = go.Figure()

    fig_saldo.add_trace(go.Bar(
        x=df_saldo.index,
        y=df_saldo['saldo']
    ))

    fig_saldo.update_layout(
        title='Saldo', 
        xaxis_title='Data', 
        yaxis_title='Saldo', 
        template='seaborn'
    )

    return df_admissoes, df_demissoes, df_saldo, fig_admissoes, fig_demissoes, fig_saldo


# PNAD
@st.cache_data
def pnad():
    """
    Query Builder - TAXA DE DESOCUPAÇÃO MENSAL

    Pesquisa: Pesquisa Nacional por Amostra de Domicílios Contínua Mensal
    Agregado: 6381- Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade - Total, coeficiente de variação, variações em relação aos três trimestres móveis anteriores e ao mesmo trimestre móvel do ano anterior
    Variáveis: 4099- Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade
    Períodos: Selecionar todos
    Nível Geográfico: N1 - Brasil
    Localidades: 1 - Brasil
    """
    link = 'http://servicodados.ibge.gov.br/api/v3/agregados/6381/periodos/201203|201204|201205|201206|201207|201208|201209|201210|201211|201212|201301|201302|201303|201304|201305|201306|201307|201308|201309|201310|201311|201312|201401|201402|201403|201404|201405|201406|201407|201408|201409|201410|201411|201412|201501|201502|201503|201504|201505|201506|201507|201508|201509|201510|201511|201512|201601|201602|201603|201604|201605|201606|201607|201608|201609|201610|201611|201612|201701|201702|201703|201704|201705|201706|201707|201708|201709|201710|201711|201712|201801|201802|201803|201804|201805|201806|201807|201808|201809|201810|201811|201812|201901|201902|201903|201904|201905|201906|201907|201908|201909|201910|201911|201912|202001|202002|202003|202004|202005|202006|202007|202008|202009|202010|202011|202012|202101|202102|202103|202104|202105|202106|202107|202108|202109|202110|202111|202112|202201|202202|202203|202204|202205|202206|202207|202208|202209|202210|202211|202212|202301|202302|202303|202304|202305|202306/variaveis/4099?localidades=N1[all]'
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    # Taxa de desocupação total mensal
    resultados = informacoes[0]['resultados'][0]['series'][0]['serie']
    # Transformando em um dataframe
    taxa_desocupacao = pd.DataFrame({'taxa_desocupacao':resultados})
    # Transformando o dtype da coluna e index
    taxa_desocupacao['taxa_desocupacao'] = taxa_desocupacao['taxa_desocupacao'].astype(float)
    taxa_desocupacao.index = pd.to_datetime(taxa_desocupacao.index, format='%Y%m')

    # Plotando a 'Taxa de Desocupação Mensal'
    fig_taxa_desocupacao = go.Figure()

    fig_taxa_desocupacao.add_trace(go.Scatter(
        x=taxa_desocupacao.index, 
        y=taxa_desocupacao['taxa_desocupacao'], 
        mode='lines'
    ))

    fig_taxa_desocupacao.update_traces(mode="markers+lines")

    fig_taxa_desocupacao.update_layout(
        title="Taxa de Desocupação Mensal - Brasil",
        xaxis_title="Mensal",
        yaxis_title="Taxa de Desocupação"
    )

    """
    Query Builder - TAXA DE DESOCUPAÇÃO TRIMESTRAL

    Pesquisa: Pesquisa Nacional por Amostra de Domicílios Contínua Trimestral
    Agregado: 6468 - Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade
    Variáveis: 4099 - Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade
    Períodos: Selecionar todos
    Nível Geográfico: N1 - Brasil
    Localidades: 1 - Brasil
    """
    link = 'http://servicodados.ibge.gov.br/api/v3/agregados/6468/periodos/201201|201202|201203|201204|201301|201302|201303|201304|201401|201402|201403|201404|201501|201502|201503|201504|201601|201602|201603|201604|201701|201702|201703|201704|201801|201802|201803|201804|201901|201902|201903|201904|202001|202002|202003|202004|202101|202102|202103|202104|202201|202202|202203|202204|202301/variaveis/4099?localidades=N1[all]'
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    # Taxa de desocupação total trimestral
    resultados = informacoes[0]['resultados'][0]['series'][0]['serie']
    # Transformando em um dataframe
    taxa_desocupacao_tri = pd.DataFrame({'taxa_desocupacao':resultados})
    # Transformando o dtype da coluna
    taxa_desocupacao_tri['taxa_desocupacao'] = taxa_desocupacao_tri['taxa_desocupacao'].astype(float)
    # Formatando o index do df trimestral de '201201' para '20121T'
    taxa_desocupacao_tri.index = taxa_desocupacao_tri.index.map(functions.formatar_str_trimestre)

    # Plotando a 'Taxa de Desocupação Trimestral'
    fig_taxa_desocupacao_tri = go.Figure()

    fig_taxa_desocupacao_tri.add_trace(go.Scatter(
        x=taxa_desocupacao_tri.index,
        y=taxa_desocupacao_tri['taxa_desocupacao'],
        mode='lines',
        name='Taxa'
    ))

    fig_taxa_desocupacao_tri.update_traces(mode="markers+lines")

    fig_taxa_desocupacao_tri.update_layout(
        title="Taxa de Desocupação Trimestral - Brasil",
        xaxis_title="Trimestral",
        yaxis_title="Taxa de Desocupação"
    )

    """
    Query Builder - TAXA DE DESOCUPAÇÃO SEXO

    Pesquisa: Pesquisa Nacional por Amostra de Domicílios Contínua Trimestral
    Agregado: 4093 - Pessoas de 14 ou mais de idade, total, na força de trabalho, ocupadas, desocupadas, fora da força de trabalho, e respectivas taxas e níveis, por sexo
    Variáveis: 4099 - Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade
    Períodos: Selecionar todos
    Sexo: Total; Homens; Mulheres
    Nível Geográfico: N1 - Brasil
    Localidades: 1 - Brasil
    """
    link = 'http://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/201201|201202|201203|201204|201301|201302|201303|201304|201401|201402|201403|201404|201501|201502|201503|201504|201601|201602|201603|201604|201701|201702|201703|201704|201801|201802|201803|201804|201901|201902|201903|201904|202001|202002|202003|202004|202101|202102|202103|202104|202201|202202|202203|202204|202301/variaveis/4099?localidades=N1[all]&classificacao=2[all]'
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    # Taxa de desocupação - homens e mulheres trimestral
    resultados_homens = informacoes[0]['resultados'][1]['series'][0]['serie']
    resultados_mulheres = informacoes[0]['resultados'][2]['series'][0]['serie']
    # Transformando em um dataframe
    taxa_homens = pd.DataFrame({'taxa_desocupacao_homens':resultados_homens})
    taxa_mulheres = pd.DataFrame({'taxa_desocupacao_mulheres':resultados_mulheres})
    # Mesclando os dfs
    taxa_desocupação_sexo = taxa_homens.merge(taxa_mulheres, left_index=True, right_index=True)
    # Transformando o dtype da coluna
    taxa_desocupação_sexo['taxa_desocupacao_homens'] = taxa_desocupação_sexo['taxa_desocupacao_homens'].astype(float)
    taxa_desocupação_sexo['taxa_desocupacao_mulheres'] = taxa_desocupação_sexo['taxa_desocupacao_mulheres'].astype(float)
    # Transformando a string do index em '20121T', '20122T', '20123T', '20124T'
    taxa_desocupação_sexo.index = taxa_desocupação_sexo.index.map(functions.formatar_str_trimestre)

    # Plotando o df
    fig_desocupação_sexo = go.Figure()

    fig_desocupação_sexo.add_trace(go.Scatter(
        x=taxa_desocupação_sexo.index,
        y=taxa_desocupação_sexo['taxa_desocupacao_homens'],
        mode='lines',
        name='Taxa Homens'
    ))

    fig_desocupação_sexo.add_trace(go.Scatter(
        x=taxa_desocupação_sexo.index,
        y=taxa_desocupação_sexo['taxa_desocupacao_mulheres'],
        mode='lines',
        name='Taxa Mulheres'
    ))

    fig_desocupação_sexo.update_traces(mode="markers+lines")

    fig_desocupação_sexo.update_layout(
        title="Taxa de Desocupação por Sexo Trimestral - Brasil",
        xaxis_title="Trimestral",
        yaxis_title="Taxa de Desocupação"
    )

    """
    Query Builder - TAXA DE DESOCUPAÇÃO IDADE

    Pesquisa: Pesquisa Nacional por Amostra de Domicílios Contínua Trimestral
    Agregado: 4094- Pessoas de 14 anos ou mais de idade, total, na força de trabalho, ocupadas, desocupadas, fora da força de trabalho, e respectivas taxas e níveis, por grupo de idade
    Variáveis: 4099- Taxa de desocupação, na semana de referência, das pessoas de 14 anos ou mais de idade
    Períodos: Selecionar todos
    Grupo de idade: Total; 14 a 17 anos; 18 a 24 anos; 25 a 39 anos; 40 a 59 anos; 60 anos ou mais
    Nível Geográfico: N1 - Brasil
    Localidades: 1 - Brasil
    """
    link = 'http://servicodados.ibge.gov.br/api/v3/agregados/4094/periodos/201201|201202|201203|201204|201301|201302|201303|201304|201401|201402|201403|201404|201501|201502|201503|201504|201601|201602|201603|201604|201701|201702|201703|201704|201801|201802|201803|201804|201901|201902|201903|201904|202001|202002|202003|202004|202101|202102|202103|202104|202201|202202|202203|202204|202301/variaveis/4099?localidades=N1[all]&classificacao=58[all]'
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    # Taxa de desocupação por idade trimestral
    resultados_1417 = informacoes[0]['resultados'][1]['series'][0]['serie']   # 14 a 17 anos
    resultados_1824 = informacoes[0]['resultados'][2]['series'][0]['serie']   # 18 a 24 anos
    resultados_2539 = informacoes[0]['resultados'][3]['series'][0]['serie']   # 25 a 39 anos
    resultados_4059 = informacoes[0]['resultados'][4]['series'][0]['serie']   # 40 a 59 anos
    resultados_60mais = informacoes[0]['resultados'][5]['series'][0]['serie'] # 60 anos ou mais
    # Transformando em um dataframe
    taxa_1417 = pd.DataFrame({'taxa_desocupacao_14_a_17_anos':resultados_1417})
    taxa_1824 = pd.DataFrame({'taxa_desocupacao_18_a_24_anos':resultados_1824})
    taxa_2539 = pd.DataFrame({'taxa_desocupacao_25_a_39_anos':resultados_2539})
    taxa_4059 = pd.DataFrame({'taxa_desocupacao_40_a_59_anos':resultados_4059})
    taxa_60mais = pd.DataFrame({'taxa_desocupacao_60_anos_ou_mais':resultados_60mais})
    # Mesclando todos os dfs
    taxa_desocupacao_idade = pd.concat([taxa_1417, taxa_1824, taxa_2539, taxa_4059, taxa_60mais], axis=1)
    # Transformando o dtype da coluna
    taxa_desocupacao_idade['taxa_desocupacao_14_a_17_anos'] = taxa_desocupacao_idade['taxa_desocupacao_14_a_17_anos'].astype(float)
    taxa_desocupacao_idade['taxa_desocupacao_18_a_24_anos'] = taxa_desocupacao_idade['taxa_desocupacao_18_a_24_anos'].astype(float)
    taxa_desocupacao_idade['taxa_desocupacao_25_a_39_anos'] = taxa_desocupacao_idade['taxa_desocupacao_25_a_39_anos'].astype(float)
    taxa_desocupacao_idade['taxa_desocupacao_40_a_59_anos'] = taxa_desocupacao_idade['taxa_desocupacao_40_a_59_anos'].astype(float)
    taxa_desocupacao_idade['taxa_desocupacao_60_anos_ou_mais'] = taxa_desocupacao_idade['taxa_desocupacao_60_anos_ou_mais'].astype(float)
    # Transformando a string do index em '20121T', '20122T', '20123T', '20124T'
    taxa_desocupacao_idade.index = taxa_desocupacao_idade.index.map(functions.formatar_str_trimestre)

    # Plotando o df
    fig_taxa_desocupacao_idade = go.Figure()

    fig_taxa_desocupacao_idade.add_trace(go.Scatter(
    x=taxa_desocupacao_idade.index,
    y=taxa_desocupacao_idade['taxa_desocupacao_14_a_17_anos'],
    mode='lines',
    name='14 a 17 anos'
    ))

    fig_taxa_desocupacao_idade.add_trace(go.Scatter(
    x=taxa_desocupacao_idade.index,
    y=taxa_desocupacao_idade['taxa_desocupacao_18_a_24_anos'],
    mode='lines',
    name='18 a 24 anos'
    ))

    fig_taxa_desocupacao_idade.add_trace(go.Scatter(
    x=taxa_desocupacao_idade.index,
    y=taxa_desocupacao_idade['taxa_desocupacao_25_a_39_anos'],
    mode='lines',
    name='25 a 39 anos'
    ))

    fig_taxa_desocupacao_idade.add_trace(go.Scatter(
    x=taxa_desocupacao_idade.index,
    y=taxa_desocupacao_idade['taxa_desocupacao_40_a_59_anos'],
    mode='lines',
    name='40 a 59 anos'
    ))

    fig_taxa_desocupacao_idade.add_trace(go.Scatter(
    x=taxa_desocupacao_idade.index,
    y=taxa_desocupacao_idade['taxa_desocupacao_60_anos_ou_mais'],
    mode='lines',
    name='60 anos ou mais'
    ))

    fig_taxa_desocupacao_idade.update_traces(mode="markers+lines")

    fig_taxa_desocupacao_idade.update_layout(
        title="Taxa de Desocupação por Idade Trimestral - Brasil",
        xaxis_title="Trimestral",
        yaxis_title="Taxa de Desocupação"
    )

    """
    Query Builder - NÚMERO DE PESSOAS EM IDADE DE TRABALHAR

    Pesquisa: Pesquisa Nacional por Amostra de Domicílios Contínua Trimestral
    Agregado: 4093 - Pessoas de 14 ou mais de idade, total, na força de trabalho, ocupadas, desocupadas, fora da força de trabalho, e respectivas taxas e níveis, por sexo
    Variáveis: 1641 - Pessoas de 14 anos ou mais de idade
    Períodos: Selecionar todos
    Sexo: Total; Homens; Mulheres
    Nível Geográfico: N1 - Brasil
    Localidades: 1 - Brasil
    """
    link = 'http://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/201201|201202|201203|201204|201301|201302|201303|201304|201401|201402|201403|201404|201501|201502|201503|201504|201601|201602|201603|201604|201701|201702|201703|201704|201801|201802|201803|201804|201901|201902|201903|201904|202001|202002|202003|202004|202101|202102|202103|202104|202201|202202|202203|202204|202301/variaveis/1641?localidades=N1[all]&classificacao=2[all]'
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    # Nº de pessoas em idade de trabalhar trimestral
    resultados_num_total = informacoes[0]['resultados'][0]['series'][0]['serie'] # Total
    resultados_num_homens = informacoes[0]['resultados'][1]['series'][0]['serie'] # Homens
    resultados_num_mulheres = informacoes[0]['resultados'][2]['series'][0]['serie'] # Mulheres
    # Transformando em um dataframe
    num_total = pd.DataFrame({'numero_total':resultados_num_total})
    num_homens = pd.DataFrame({'numero_homens':resultados_num_homens})
    num_mulheres = pd.DataFrame({'numero_mulheres':resultados_num_mulheres})
    # Mesclando todos os dfs
    num_pessoas_trabalho = pd.concat([num_total, num_homens, num_mulheres], axis=1)
    # Transformando o dtype da coluna
    num_pessoas_trabalho['numero_total'] = num_pessoas_trabalho['numero_total'].astype(int)
    num_pessoas_trabalho['numero_homens'] = num_pessoas_trabalho['numero_homens'].astype(int)
    num_pessoas_trabalho['numero_mulheres'] = num_pessoas_trabalho['numero_mulheres'].astype(int)
    # Transformando a string do index em '20121T', '20122T', '20123T', '20124T'
    num_pessoas_trabalho.index = num_pessoas_trabalho.index.map(functions.formatar_str_trimestre)

    # Plotando o df
    fig_idade_trabalho = go.Figure()

    fig_idade_trabalho.add_trace(go.Scatter(
    x=num_pessoas_trabalho.index,
    y=num_pessoas_trabalho['numero_total'],
    mode='lines',
    name='Nº total'
    ))

    fig_idade_trabalho.add_trace(go.Scatter(
    x=num_pessoas_trabalho.index,
    y=num_pessoas_trabalho['numero_homens'],
    mode='lines',
    name='Nº homens'
    ))

    fig_idade_trabalho.add_trace(go.Scatter(
    x=num_pessoas_trabalho.index,
    y=num_pessoas_trabalho['numero_mulheres'],
    mode='lines',
    name='Nº mulheres'
    ))

    fig_idade_trabalho.update_traces(mode="markers+lines")

    fig_idade_trabalho.update_layout(
        title="Nº de Pessoas em Idade de Trabalhar Trimestral - Brasil",
        xaxis_title="Trimestral",
        yaxis_title="Nº de Pessoas"
    )

    """
    Query Builder - NÍVEL DE OCUPAÇÃO

    Pesquisa: Pesquisa Nacional por Amostra de Domicílios Contínua Trimestral
    Agregado: 6466 - Nível da ocupação, na semana de referência, das pessoas de 14 anos ou mais de idade
    Variáveis: 4097 - Nível de ocupação, na semana de referência, das pessoas de 14 anos ou mais de idade
    Períodos: Selecionar todos
    Nível Geográfico: N1 - Brasil
    Localidades: 1 - Brasil
    """
    link = 'http://servicodados.ibge.gov.br/api/v3/agregados/6466/periodos/201201|201202|201203|201204|201301|201302|201303|201304|201401|201402|201403|201404|201501|201502|201503|201504|201601|201602|201603|201604|201701|201702|201703|201704|201801|201802|201803|201804|201901|201902|201903|201904|202001|202002|202003|202004|202101|202102|202103|202104|202201|202202|202203|202204|202301/variaveis/4097?localidades=N1[all]'
    requisicao = requests.get(link)
    informacoes = requisicao.json()
    # Nível de ocupação Brasil trimestral
    resultados_nivel_ocupacao =  informacoes[0]['resultados'][0]['series'][0]['serie']
    # Transformando em um dataframe
    nivel_ocupacao = pd.DataFrame({'nivel_ocupacao':resultados_nivel_ocupacao})
    # Transformando o dtype da coluna
    nivel_ocupacao['nivel_ocupacao'] = nivel_ocupacao['nivel_ocupacao'].astype(float)
    # Transformando a string do index em '20121T', '20122T', '20123T', '20124T'
    nivel_ocupacao.index = nivel_ocupacao.index.map(functions.formatar_str_trimestre)

    # Plotando o df
    fig_nivel_ocupacao = go.Figure()

    fig_nivel_ocupacao.add_trace(go.Scatter(
        x=nivel_ocupacao.index,
        y=nivel_ocupacao['nivel_ocupacao'],
        mode='lines'
    ))

    fig_nivel_ocupacao.update_traces(mode="markers+lines")

    fig_nivel_ocupacao.update_layout(
        title="Nível de Ocupação Trimestral - Brasil",
        xaxis_title="Trimestral",
        yaxis_title="Nível de ocupação"
    )

    return (fig_taxa_desocupacao, 
            fig_taxa_desocupacao_tri, 
            fig_desocupação_sexo, 
            fig_taxa_desocupacao_idade, 
            fig_idade_trabalho, 
            fig_nivel_ocupacao
    )


# Expectativas FOCUS
@st.cache_data
def expectativa_focus():
    # Expectativas IPCA
    ipca_expec_23 = functions.expectativa_ativo(
        indicador='IPCA', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2022-01-01', 
        data_ref=2023
    )
    ipca_expec_24 = functions.expectativa_ativo(
        indicador='IPCA', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2022-01-01', 
        data_ref=2024
    )
    ipca_expec_25 = functions.expectativa_ativo(
        indicador='IPCA', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2022-01-01', 
        data_ref=2025
    )
    # Renomeando as colunas
    ipca_expec_23 = ipca_expec_23.rename(columns={'Mediana':'Mediana_23'})
    ipca_expec_24 = ipca_expec_24.rename(columns={'Mediana':'Mediana_24'})
    ipca_expec_25 = ipca_expec_25.rename(columns={'Mediana':'Mediana_25'})
    # Concatenando os dfs
    df_ipca_expec = pd.concat([ipca_expec_23, ipca_expec_24, ipca_expec_25], axis=1)

    # Plotando a 'Expectativas IPCA'
    fig_ipca_expec = go.Figure()
    fig_ipca_expec.add_trace(go.Scatter(
        x=df_ipca_expec.index, 
        y=round(df_ipca_expec['Mediana_23'], 2), 
        mode='lines', 
        name=f'IPCA 2023'
    ))
    fig_ipca_expec.add_trace(go.Scatter(
        x=df_ipca_expec.index, 
        y=round(df_ipca_expec['Mediana_24'], 2), 
        mode='lines', 
        name=f'IPCA 2024'
    ))
    fig_ipca_expec.add_trace(go.Scatter(
        x=df_ipca_expec.index, 
        y=round(df_ipca_expec['Mediana_25'], 2), 
        mode='lines', 
        name=f'IPCA 2025'
    ))
    fig_ipca_expec.update_layout(
        title=f'Gráfico da Expectativas do Mercado - IPCA', 
        xaxis_title='Anos', 
        yaxis_title=f'Expectativa IPCA', 
        template='seaborn'
    )

    # Expectativas SELIC
    selic_expec_23 = functions.expectativa_ativo(
        indicador='Selic', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2022-01-01', 
        data_ref=2023
    )
    selic_expec_24 = functions.expectativa_ativo(
        indicador='Selic', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2022-01-01', 
        data_ref=2024
    )
    selic_expec_25 = functions.expectativa_ativo(
        indicador='Selic', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2022-01-01', 
        data_ref=2025
    )
    # Renomeando as colunas
    selic_expec_23 = selic_expec_23.rename(columns={'Mediana':'Mediana_23'})
    selic_expec_24 = selic_expec_24.rename(columns={'Mediana':'Mediana_24'})
    selic_expec_25 = selic_expec_25.rename(columns={'Mediana':'Mediana_25'})
    # Concatenando os dfs
    df_selic_expec = pd.concat([selic_expec_23, selic_expec_24, selic_expec_25], axis=1)

    # Plotando a 'Expectativas Selic'
    fig_selic_expec = go.Figure()
    fig_selic_expec.add_trace(go.Scatter(
        x=df_selic_expec.index, 
        y=round(df_selic_expec['Mediana_23'], 2), 
        mode='lines', 
        name=f'selic 2023'
    ))
    fig_selic_expec.add_trace(go.Scatter(
        x=df_selic_expec.index, 
        y=round(df_selic_expec['Mediana_24'], 2), 
        mode='lines', 
        name=f'selic 2024'
    ))
    fig_selic_expec.add_trace(go.Scatter(
        x=df_selic_expec.index, 
        y=round(df_selic_expec['Mediana_25'], 2), 
        mode='lines', 
        name=f'selic 2025'
    ))
    fig_selic_expec.update_layout(
        title=f'Gráfico da Expectativas do Mercado - Selic', 
        xaxis_title='Anos', 
        yaxis_title=f'Expectativa Selic', 
        template='seaborn'
    )

    # Expectativas PIB
    pib_expec_23 = functions.expectativa_ativo(
        indicador='PIB Total', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2021-06-01', 
        data_ref=2023
    )
    pib_expec_24 = functions.expectativa_ativo(
        indicador='PIB Total', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2021-06-01', 
        data_ref=2024
    )
    pib_expec_25 = functions.expectativa_ativo(
        indicador='PIB Total', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2021-06-01', 
        data_ref=2025
    )
    # Renomeando as colunas
    pib_expec_23 = pib_expec_23.rename(columns={'Mediana':'Mediana_23'})
    pib_expec_24 = pib_expec_24.rename(columns={'Mediana':'Mediana_24'})
    pib_expec_25 = pib_expec_25.rename(columns={'Mediana':'Mediana_25'})
    # Concatenando os dfs
    df_pib_expec = pd.concat([pib_expec_23, pib_expec_24, pib_expec_25], axis=1)

    # Plotando a 'Expecativas PIB'
    fig_pib_expec = go.Figure()
    fig_pib_expec.add_trace(go.Scatter(
        x=df_pib_expec.index, 
        y=round(df_pib_expec['Mediana_23'], 2), 
        mode='lines', 
        name=f'PIB 2023'
    ))
    fig_pib_expec.add_trace(go.Scatter(
        x=df_pib_expec.index, 
        y=round(df_pib_expec['Mediana_24'], 2), 
        mode='lines', 
        name=f'PIB 2024'
    ))
    fig_pib_expec.add_trace(go.Scatter(
        x=df_pib_expec.index, 
        y=round(df_pib_expec['Mediana_25'], 2), 
        mode='lines', 
        name=f'PIB 2025'
    ))
    fig_pib_expec.update_layout(
        title=f'Gráfico da Expectativas do Mercado - PIB', 
        xaxis_title='Anos', 
        yaxis_title=f'Expectativa PIB', 
        template='seaborn'
    )

    # Expectativas Câmbio
    cambio_expec_23 = functions.expectativa_ativo(
        indicador='Câmbio', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2022-01-01', 
        data_ref=2023
    )
    cambio_expec_24 = functions.expectativa_ativo(
        indicador='Câmbio', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2022-01-01', 
        data_ref=2024
    )
    cambio_expec_25 = functions.expectativa_ativo(
        indicador='Câmbio', 
        tipo_expec='ExpectativasMercadoAnuais', 
        data_inicio='2022-01-01', 
        data_ref=2025
    )
    # Renomeando as colunas
    cambio_expec_23 = cambio_expec_23.rename(columns={'Mediana':'Mediana_23'})
    cambio_expec_24 = cambio_expec_24.rename(columns={'Mediana':'Mediana_24'})
    cambio_expec_25 = cambio_expec_25.rename(columns={'Mediana':'Mediana_25'})
    # Concatenando os dfs
    df_cambio_expec = pd.concat([cambio_expec_23, cambio_expec_24, cambio_expec_25], axis=1)

     # Plotando a 'Expectativas Câmbio'
    fig_cambio_expec = go.Figure()
    fig_cambio_expec.add_trace(go.Scatter(
        x=df_cambio_expec.index, 
        y=round(df_cambio_expec['Mediana_23'], 2), 
        mode='lines', 
        name='Dólar 23'
    ))
    fig_cambio_expec.add_trace(go.Scatter(
        x=df_cambio_expec.index, 
        y=round(df_cambio_expec['Mediana_24'], 2), 
        mode='lines', 
        name='Dólar 24'
    ))
    fig_cambio_expec.add_trace(go.Scatter(
        x=df_cambio_expec.index, 
        y=round(df_cambio_expec['Mediana_25'], 2), 
        mode='lines', 
        name='Dólar 25'
    ))
    fig_cambio_expec.update_layout(
        title='Gráfico da Expectativas do Mercado - Câmbio', 
        xaxis_title='Anos', 
        yaxis_title='Câmbio', 
        template='seaborn'
    )
   
    return (df_ipca_expec, 
            df_selic_expec, 
            df_pib_expec, 
            df_cambio_expec,
            fig_ipca_expec, 
            fig_selic_expec,
            fig_pib_expec,
            fig_cambio_expec
    )


# PIB
@st.cache_data
def pib():
    # PIB acumulado dos últimos 12 meses - valores correntes
    df_pib_acum = functions.data_bcb(4382)
    # Calculando a variação percentual
    df_pib_acum['pct_changes'] = round((df_pib_acum['valor'].pct_change())*100,2)

    # Plotando o 'PIB acumulado dos últimos 12 meses - valores correntes'
    fig_pib_acum = go.Figure()
    fig_pib_acum.add_trace(go.Scatter(
        x=df_pib_acum.index,
        y=df_pib_acum['valor'],
        mode='lines',
        name='PIB')
    )
    fig_pib_acum.update_layout(
        title='PIB Acumulado dos Últimos 12 meses - Valores Correntes',
        xaxis_title='Ano',
        yaxis_title='R$',
        template='seaborn'
    )

    # Taxa de Variação Real do PIB no Ano
    df_pib_var = functions.data_bcb(7326)

    # Plotando a 'Taxa de Variação Real do PIB no Ano'
    fig_pib_var = go.Figure()
    fig_pib_var.add_trace(go.Bar(
        x=df_pib_var.index,
        y=df_pib_var['valor']
    ))
    fig_pib_var.update_layout(
        title='Taxa de Variação Real do PIB no Ano',
        xaxis_title='Ano',
        yaxis_title='Variação %',
        template='seaborn'
    )

    return df_pib_acum, df_pib_var, fig_pib_acum, fig_pib_var  


# EMBI+
@st.cache_data
def embi():
    # EMBI+
    df = ipeadatapy.timeseries('JPM366_EMBI366', yearGreaterThan=2000)
    # Renomeando a coluna
    df = df.rename(columns={'VALUE (-)': 'valor'})

    # Plotando o EMBI+
    fig_embi = go.Figure()

    fig_embi.add_trace(go.Scatter(
        x=df.index, 
        y=df['valor'], 
        mode='lines'
    ))

    fig_embi.update_layout(
        title='EMBI+', 
        xaxis_title='Anos', 
        yaxis_title='Valor', 
        template='seaborn'
    )

    return df, fig_embi