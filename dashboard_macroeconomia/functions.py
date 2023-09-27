import pandas as pd
import plotly.express as px
import requests
import json
from bcb import Expectativas

def data_bls(series_id: str, start_year: int, end_year: int, api_key: str):
  """
  Criação de um dataframe para os ativos listados na BLS (U.S. Bureau of Labor Statistics)

  Parameters:
  series_id (str): série do ativo do BLS.
  start_year (str): data de início da série do ativo.
  end_year (int): data final da série do ativo.

  Returns:
  Dataframe do ativo do BLS.

  NOTE: Eu retorno um df com apenas as colunas necessárias.
  """
  headers = {'Content-type': 'application/json'}
  data = json.dumps({"seriesid": series_id, "startyear": start_year, "endyear": end_year, "registrationkey": api_key})
  p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
  json_data = json.loads(p.text)

  for series in json_data['Results']['series']:
      seriesId = series['seriesID']
      rows = []
      for item in series['data']:
          year = item['year']
          period = item['period']
          value = item['value']
          footnotes = ""
          for footnote in item['footnotes']:
              if footnote:
                  footnotes = footnotes + footnote['text'] + ','
          if 'M01' <= period <= 'M12':
              rows.append([seriesId, year, period, value, footnotes[:-1]])

      df = pd.DataFrame(rows, columns=["series_id", "year", "period", "value", "footnotes"])

      # Revertendo as linhas - 1º linha (dados mais atualizado) vira última linha
      df = df[::-1]

      # Retirando a letra 'M' da coluna 'period'
      df['period'] = df['period'].str.replace('M', '')
      # Criando a coluna 'data' (junção das colunas 'period' e 'year')
      df['data'] = df['period'].astype(str).str.cat(df['year'].astype(str), sep='-')

      # Transformando os dtypes das colunas
      df['data'] = pd.to_datetime(df['data'], format='%m-%Y')
      df['value'] = df['value'].astype(float)

      # Tranformando a 'data' no index do df
      df = df.set_index('data')

      # Calculando a variação percentual
      df['pct_change'] = round(df['value'].pct_change(),4)*100

      # Calculando a variação percentual dos últimos 12 meses
      df['pct_change_ultimo_12_meses'] = round(df['value'].pct_change(12),4)*100

      # Selecionando apenas as colunas principais
      df = df[['value', 'pct_change', 'pct_change_ultimo_12_meses']]

      return df


def plot_heatmap_cpi(df):
  """
  Criando o heatmap da variação acumulada dos últimos 12 meses do CPI.

  Parameters:
  df: dataframe do CPI.

  Returns:
  Plot do heatmap da variação acumulada dos últimos 12 meses do CPI.
  """
  # Recriando as colunas de ano e mês
  df['year'] = df.index.year
  df['month'] = df.index.month

  # Criando o df pivot para criar o heatmap
  pivot_df = df.pivot(index='year', columns='month', values='pct_change_ultimo_12_meses')

  # Criando o heatmap
  fig = px.imshow(pivot_df, text_auto=".2f", color_continuous_scale='reds', aspect="auto")

  # Personalizando o layout do texto
  fig.update_traces(textfont=dict(color='black', size=12))

  # Definindo o layout
  fig.update_layout(hovermode='closest',
                    xaxis_title='Meses',
                    yaxis_title='Anos',

  )

  return fig


def data_bcb(codigo_bcb):
  """
  Criação do dataframe do ativo pesquisado do BC.

  Parameters:
  codigo_bcb (str): código do ativo do BC.

  Returns:
  Dataframe formatado do ativo do BC.
  """
  url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'.format(codigo_bcb)
  df = pd.read_json(url)
  df['data'] = pd.to_datetime(df['data'], dayfirst=True)
  df = df.set_index('data')

  return df


def formatar_str_trimestre(trimestre_str):
    """
    Transformação da string do index do dfs da PNAD Contínua.

    Parameters:
    trimestre_str (str): index dos dfs da PNAD Contínua.
    
    Returns:
    String do index formatado (20121T', '20122T', '20123T', '20124T').
    """
    ano = trimestre_str[:4]
    trimestre = trimestre_str[4:]
    return f"{ano}{trimestre}T"


# Função da Expectativa do Mercado
def expectativa_ativo(indicador: str, tipo_expec: str, data_inicio: str, data_ref: int):
  """
  Criação de um df e plotagem da expectativa do ativo.

  Parameters:
  indicador (str): nome do indicador.
  data_inicio (str): data de início da expectativa do mercado.
  data_ref (int): data de referência da expectativa do mercado.

  Returns:
  Dataframe das expectativas do mercado e a sua plotagem.
  """
  # Instancia a classe
  em = Expectativas()
  
  # End point
  ep = em.get_endpoint(tipo_expec)

  # Dados do ativo
  df_expec = ( ep.query()
  .filter(ep.Indicador == indicador, ep.DataReferencia == data_ref)
  .filter(ep.Data >= data_inicio)
  .filter(ep.baseCalculo == '0')
  .select(ep.Indicador, ep.Data, ep.Mediana, ep.DataReferencia)
  .collect()
  )

  # Formata a coluna de Data para formato datetime
  df_expec['Data'] = pd.to_datetime(df_expec['Data'], format = '%Y-%m-%d')

  # Transformando a coluna 'Data' no index do df
  df_expec = df_expec.set_index('Data')

  # Selecionando apenas as colunas mais importantes
  df_expec = df_expec[['Mediana']]

  return df_expec