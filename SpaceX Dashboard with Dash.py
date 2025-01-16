# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'All'},{'label':'CCAFS LC-40', 'value':'CCAFS LC-40'}, {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}, {'label':'KSC LC-39A', 'value':'KSC LC-39A'}, {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}], value='All', placeholder='Select the Launch Site', searchable=True),
                                html.Br(),
                                


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                               
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, value=[min_payload, max_payload], marks={i: f'{i}' for i in range(0, 10000, 1000)}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'), [Input(component_id='site-dropdown', component_property='value')])
def get_pie_chart(value):
  
    if value == 'All':
        filtered_data = spacex_df[spacex_df['class'] == 1]
        data = filtered_data.groupby('Launch Site')['class'].sum().reset_index(name='total')
        fig = px.pie(data, values='total', names='Launch Site', title='Total Success count for all sites')
    else:
        filtered_data = spacex_df[spacex_df['Launch Site'] == value]
        data = filtered_data.groupby('class').value_counts().reset_index(name='total')
        fig = px.pie(data, values='total', names='class', labels='class', title=f'Success vs failed count for {value}')
    return fig
         
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])

def get_scatter_plot(value1, value2):
    if value1 == 'All':
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] > value2[0]) & (spacex_df['Payload Mass (kg)'] < value2[1])]
        fig = px.scatter(filtered_data, y='class', x='Payload Mass (kg)', color='Booster Version Category', title='Correlation between Launch Success and Payload Mass', labels={'class': 'Launch Success(1=Success, 0=Failure)', 'Payload Mass (kg)': 'Payload Mass (kg)'})

    else:
        filtered_data = spacex_df[spacex_df['Launch Site'] == value1]
        data = filtered_data[(filtered_data['Payload Mass (kg)'] > value2[0]) & (filtered_data['Payload Mass (kg)'] < value2[1])]
        fig = px.scatter(data, y='class', x='Payload Mass (kg)', color='Booster Version Category', title='Correlation between Launch Success and Payload Mass', labels={'class': 'Launch Success(1=Success, 0=Failure)', 'Payload Mass (kg)': 'Payload Mass (kg)'})

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
