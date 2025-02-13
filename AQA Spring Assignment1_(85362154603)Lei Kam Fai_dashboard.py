import requests
from dash import Dash, html, dcc, callback, Output, Input, _dash_renderer
import dash_mantine_components as dmc
import plotly.graph_objects as go

_dash_renderer._set_react_version("18.2.0")

url = 'http://127.0.0.1:5000/Sector'

response = requests.get(url)

if response.status_code == 200:
    _sectors = response.json().get('sectors', [])
else:
    print("Failed to retrieve sectors:", response.status_code)
print(_sectors)

def get_ebitda(sector):
    url = f'http://127.0.0.1:5000/EBITDA?Sector={sector}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve EBITDA:", response.status_code)

app = Dash()

app.layout = dmc.MantineProvider(
    children=html.Div([

        dcc.Graph(id='ebitda-pie-chart'),
        dmc.MultiSelect(
            label="Select Sectors",
            id="framework-multi-select",
            value=['Financials', 'Health Care'],
            data=[{'value': sector, 'label': sector} for sector in _sectors],
            w=400,
            mb=10,
        ),
        html.A(
            "Download CSV",
            id="download-link",
            href="http://127.0.0.1:5000/download_csv",  # Direct link to the endpoint
            target="_blank",
            download="data.csv"  # This will suggest a filename
        ),

    ])
)

@app.callback(
    Output('ebitda-pie-chart', 'figure'),
    Input('framework-multi-select', 'value')  # Input for selected sectors
)
def update_pie_chart(selected_sectors):
    if not selected_sectors:
        return go.Figure()  # Return an empty figure if no sectors are selected
    # Collect EBITDA data for the selected sectors
    ebitda_data = {}
    for sector in selected_sectors:
        ebitda_values = get_ebitda(sector)
        # ebitda_values is a list of EBITDA numbers
        ebitda_data[sector] = sum(ebitda_values)  # Sum the EBITDA values for the sector

    print(ebitda_data)
    # Create the pie chart
    fig = go.Figure(data=[go.Pie(
        labels=list(ebitda_data.keys()),
        values=list(ebitda_data.values()),
        hole=0.3 # for a donut chart
    )])

    return fig

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
