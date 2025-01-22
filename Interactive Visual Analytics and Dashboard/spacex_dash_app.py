# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
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
                                dcc.Dropdown(
                                            id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'All Sites'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                            ],
                                            value='ALL',  # Default value is 'ALL' meaning all sites are selected
                                            placeholder='Select a Launch Site here',  # Text description about this input area
                                            searchable=True  # Allow searching of launch sites
                                        ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                                id='payload-slider',
                                                min=0,  # Starting point of the slider
                                                max=10000,  # Ending point of the slider
                                                step=1000,  # Interval on the slider
                                                marks={i: f'{i}' for i in range(0, 10001, 1000)},  # Marks at each interval
                                                value=[min_payload, max_payload]  # Default selected range
                                            ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Assuming you have a Dash app instance named 'app' and a dataframe 'spacex_df'
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'All Sites':
        # Use all rows in the dataframe to render a pie chart for total success launches
        fig = px.pie(filtered_df, 
                     values='class', 
                     names='class', 
                     title='Total Success Launches for All Sites')
    else:
        # Filter the dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Use filtered data to render a pie chart for success and failure counts
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Success and Failure Counts for {entered_site}')

    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Assuming you have a Dash app instance named 'app' and a dataframe 'spacex_df'
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, selected_payload):
    # Filter the dataframe based on the selected payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= selected_payload[0]) & 
        (spacex_df['Payload Mass (kg)'] <= selected_payload[1])
    ]
    
    if selected_site == 'ALL':
        # If ALL sites are selected, render a scatter plot for all sites
        fig = px.scatter(filtered_df, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category', 
                         title='Payload vs. Outcome for All Sites')
    else:
        # Filter the dataframe for the selected site
        filtered_site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        # Render a scatter plot for the selected site
        fig = px.scatter(filtered_site_df, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category', 
                         title=f'Payload vs. Outcome for {selected_site}')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
