from os import getenv
import shimoku_api_python as Shimoku
import pandas as pd
import requests

access_token = getenv('SHIMOKU_TOKEN')
universe_id: str = getenv('UNIVERSE_ID')
workspace_id: str = getenv('WORKSPACE_ID')

s = Shimoku.Client(
    access_token=access_token,
    universe_id=universe_id,
    verbosity='INFO',
    async_execution=True,
)
s.set_workspace(workspace_id)

s.set_board('Tabla de Temperaturas')

s.set_menu_path('Lima')

s.plt.clear_menu_path()

url = "https://es.climate-data.org/america-del-sur/peru/lima/lima-1014/t/noviembre-11/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(url, headers=headers)

tables = pd.read_html(response.text)[4]

selected_columns = tables[['Unnamed: 0', 'Temperatura (°C)', 'Temperatura max (°C)','Temperatura min (°C)']]

selected_columns['Temperatura (°C)'] = pd.to_numeric(selected_columns['Temperatura (°C)'].str.replace('°C', ''))
selected_columns['Temperatura max (°C)'] = pd.to_numeric(selected_columns['Temperatura max (°C)'].str.replace('°C', ''))
selected_columns['Temperatura min (°C)'] = pd.to_numeric(selected_columns['Temperatura min (°C)'].str.replace('°C', ''))

s.plt.html(
    html=(
        "<h1>Temperaturas</h1>" 
        "<p style='color:var(--color-grey-600);'>Temperaturas del mes de Noviembre de Lima Metropolitana</p>"
    ),
    order=0, rows_size=2, cols_size=12,
)

s.plt.set_tabs_index(tabs_index=('Tabs Group', 'Barras'),order= 1)
s.plt.bar(
    order=0, title='Grafico de Barras',
    data=selected_columns, x='Unnamed: 0',
    y=['Temperatura (°C)', 'Temperatura max (°C)','Temperatura min (°C)'],
)

s.plt.change_current_tab('Lineas')
s.plt.line(
    order=0, title='Grafico de Lineas',
    data=selected_columns, x='Unnamed: 0',
    y=['Temperatura (°C)', 'Temperatura max (°C)','Temperatura min (°C)'],
)

s.plt.change_current_tab('Area')
s.plt.area(
    order=0, title='Grafico de Area',
    data=selected_columns, x='Unnamed: 0',
    y=['Temperatura (°C)', 'Temperatura max (°C)','Temperatura min (°C)'],
)

s.plt.change_current_tab('Lineas y Barras')
s.plt.line_and_bar_charts(
    data=selected_columns, order=0, x='Unnamed: 0', 
    bar_names=['Temperatura (°C)'], 
    line_names=['Temperatura max (°C)','Temperatura min (°C)'],
    title='Grafica de Lineas y Barras', 
    x_axis_name='Dia', 
    line_suffix=' °C',
    bar_axis_name='Temperatura',  
    bar_suffix=' °C'
)
s.run()