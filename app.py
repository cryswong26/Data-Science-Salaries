######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Data Science Salaries'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries'
githublink = 'https://github.com/cryswong26/Data-Science-Salaries'


###### Import a dataframe ####### - focusing on what types of roles have the highest % of 100% remote work + a high salary
df = pd.read_csv('assets/ds_salaries.csv')
variable=['experience_level', 'company_size']

df['remote_high_salary'] = (df['salary_in_usd'] >= df['salary_in_usd'].mean()) & (df['remote_ratio'] == 100)
df['US_remote_high_salary'] = (df['remote_high_salary'] == True) & (df['company_location'] == 'US')
#isolated to just the US because most of the roles that fit the criteria for "remote_high_salary" were only in the US
#defined "high salary" as anything greater than the mean salary of the data set

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a variable to see what types of Data Science roles are most likely to be fully remote and have a high salary:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variable],
        value=variable[0]
    ),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                html.Div(children=[
                    html.H4('Legend and Observations'),
                    html.Ul(children=[
                        html.Li("Experience Level: EN = Entry-level, MI = Mid-level, SE = Senior-level, EX = Executive-level"),
                        html.Li("Medium-sized companies have the highest number of fully remote & high-paying roles"),
                        html.Li("The number of fully remote & high-paying roles increases with seniority"),
                    ])
                ]),
                width=3
            )],
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    df_output = df.groupby([continuous_var])['US_remote_high_salary'].sum()
    final_output = pd.DataFrame(df_output)    
    # Create a bar chart
    mydata1 = go.Bar(
        x=final_output.index,
        y=final_output['US_remote_high_salary'],
        marker=dict(color=color1)
    )
   
    mylayout = go.Layout(
        title='Bar chart',
        xaxis = dict(title = continuous_var), # x-axis label
        yaxis = dict(title = '# of roles'), # y-axis label

    )
    fig = go.Figure(data=[mydata1], layout=mylayout)
    return fig

######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
