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


###### Import a dataframe ####### - goal is to show the highest average salaries by different dimensions
#df = pd.read_csv('../assets/ds_salaries.csv')
df = pd.read_csv('assets/ds_salaries.csv')
variable=['experience_level', 'company_location', 'company_size', 'remote_ratio']
column_to_aggregate = 'salary_in_usd'
agg_method = 'mean'

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a variable to see average Data Science salaries:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variable],
        value=variable[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def create_all_summary(df,variable,column_to_aggregate,agg_method): 
    df_output = df.groupby(variable)[column_to_aggregate].agg(agg_method)
    return df_output

    mydata1 = go.Bar(
        x=df_output.index,
        y=df_output.values,
        #name='First Class',
        marker=dict(color=color1)
    )

    mylayout = go.Layout(
        title='Bar Chart',
        xaxis = dict(title = str(variable)), # x-axis label
        yaxis = dict(title = 'Average DS Salary') # y-axis label

    )
    fig = go.Figure(data=[mydata1], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
