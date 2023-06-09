#Pre req enviornment
# python3.8 -m pip install pandas dash
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"

# running the current app
# python3.8 dash_app.py

# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df =  pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)
                               
app.layout = html.Div(children=[ html.H1('SpaceX Launch Records Dashboard', 
                                        style={'textAlign': 'center', 'color': '#503D36',
                                        'font-size': 40}),
                                # TASK 1: Add a Launch Site Drop-down Input Component
                                # The default select value is for ALL sites
                                dcc.Dropdown(id = 'site-dropdown',
                                            options = [{'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                    ],
                                            value = 'ALL',
                                            placeholder = 'Select Launch Site',
                                            searchable = True
                                            ),

                                html.Br(),

                                # Task 2 Add a pie chart
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                #Task 3 Add a range slider to select payload
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),
                                
                                # TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),

                                ])


# Task 2 add callback decorator so the pie chart will respond to site-dropdown
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Success Count for all launch sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df=spacex_df[spacex_df['Launch Site']== entered_site]
        filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(filtered_df,values='class count',names='class',title=f"Total Success Launches for site {entered_site}")
        return fig
        
#Task 4
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])


def scatter(entered_site, payload):
    # Select  data
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
    
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x = 'Payload Mass (kg)',y='class',color='Booster Version Category',title='Success count on Payload mass for all sites')
        return fig
    else: 
        fig = px.scatter(filtered_df[filtered_df['Launch Site']==entered_site],x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f"Success count on Payload mass for site {entered_site}")
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()