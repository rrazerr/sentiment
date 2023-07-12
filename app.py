import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from collections import Counter
import unicodedata
import chart_studio as py
import plotly.graph_objs as go
import pandas as pd
from random import randint
import threading
import pandas as pd
from streaming import mainf
import os
from Senti import getData

app = dash.Dash()
im1='http://pluspng.com/img-png/twitter-png-logo-twitter-logo-png-image-with-transparent-background-2000.png'
im2='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Python_logo_and_wordmark.svg/2000px-Python_logo_and_wordmark.svg.png'
im3='https://files.realpython.com/media/flask.3aee85149243.png'
im4='https://upload.wikimedia.org/wikipedia/en/c/cd/Anaconda_Logo.png'
im5='https://seeklogo.com/images/S/spyder-logo-68D7CF8B2C-seeklogo.com.png'
im6='https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Plotly-logo-01-square.png/220px-Plotly-logo-01-square.png'
im7= 'http://www.commzgate.com/assets/img/commzgate_cloud_api.png'
im8='https://cdn0.iconfinder.com/data/icons/trending-tech/94/artificial_intelligence-512.png'
im9 ='https://cdn-images-1.medium.com/max/1200/1*lkqc68a6b7_TLALs5fmI6A.png'


iv = None
class counter:
    def app_run(self):
        app.run_server()

    def sentiment(self):
        global iv
        while True:
                print(iv)
                mainf(iv)
        

def pie(data ,label):
    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {
                    'margin': {
                        'l': 30,
                        'r': 0,
                        'b': 30,
                        't': 0
                    },
                }
            }
        )
    ])

app.layout = html.Div([
    html.H1(children=' Twitter Sentiment Analysis ', style={'marginBottom': '12px'}),
    html.Div(children = [html.Img(src=im1,style={'width': '20%', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                         html.Img(src=im2,style={'width': '20%', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                         html.Img(src=im3,style={'width': '20%', 'marginLeft': 'auto', 'marginRight': 'auto'})]),
    html.H2(" Please Enter Keyword to Analysis ",style={'marginBottom': '6px'}),
    dcc.Input(id='my-id', type='text',style={'width': '25%', 'marginLeft': 'auto', 'marginRight': 'auto'}),
    html.Button(id='submit-button', n_clicks=0, children='Analysis', 
    style={'marginTop': 15, 'marginBottom': 25}),
    html.Div(id='my-div'),
    dcc.Checklist(id = 'check',options=[{'label': 'Refresh', 'value': 'Ref'}],values=['Ref'],labelStyle={'display': 'inline-block'}),
    html.Div(children = [html.Img(src=im6,style={'width': '25%', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                         html.Img(src=im7,style={'width': '25%', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                         html.Img(src=im9,style={'width': '25%', 'marginLeft': 'auto', 'marginRight': 'auto'})])
], style={'textAlign': 'center'})

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value'),
     Input(component_id='submit-button', component_property='n_clicks'),
     Input(component_id='check', component_property='values')]
)
def update_output_div(input_value,n_clicks,values):
    print(values)
    global iv
    iv= input_value
    if n_clicks > 0:
        while values:
            [words,polarity,value]  =  getData()
            dat= Counter(polarity)
            labels = list(dat.keys())
            values = list(dat.values())
            comm=[]
            x1=[]
            y1=[]
            clr= []
            opac =[]
            siz =[]
            for i in range(0,len(words)):
                comm.append(str(unicodedata.normalize('NFKD', words[i]).encode('ascii','ignore'))[2:-1])
                x1.append(randint(0,len(words)))
                y1.append(randint(0,len(words)))
                clr.append('rgb('+str(randint(0,255))+','+str(randint(0,255))+','+str(randint(0,255)) +')')
                opac.append(randint(0,len(words)))
                siz.append(randint(0,len(words)))

            return html.Div(children = [html.H3('Twiter Analysis of  '+ str(input_value),style={'marginBottom': '6px'}),
            dcc.Graph(
                figure=go.Figure(
                data=[ go.Pie(labels=labels, values=values)
                        ],
        layout=go.Layout(
            title='Pie Chart Showing Sentiment of reviews ',
            showlegend=True,
            legend=go.Legend(
                x=0,
                y=1.0
            ),
            margin=go.Margin(l=40, r=0, t=40, b=30)
        )
    ),
    style={'height': 500},
    id='my-graph'
),
            dcc.Graph(
                figure=go.Figure(
                data=[go.Scatter(
                        x=x1,
                        y=y1,
                        mode='markers+text',
                        text= comm,
                        marker=dict(
                        color= clr,
                        size = siz,
                     )
                                    )],
        layout=go.Layout(
            title='Scatter plot of Top Used Phrases ',
            showlegend=True,
            legend=go.Legend(
                x=0,
                y=1.0
            ),
            margin=go.Margin(l=40, r=0, t=40, b=30)
        )
    ),
    style={'height': 800},
    id='my-graph1'
),
            dcc.Graph(
                figure=go.Figure(
                data=[go.Scatter(
          y=value,
          x= list(range(0,len(value))))],
        layout=go.Layout(
            title='Trend of sentiment (Recent to past)',
            showlegend=True,
            legend=go.Legend(
                x=0,
                y=1.0
            ),
            margin=go.Margin(l=40, r=0, t=40, b=30),
        )
    ),
    style={'height': 800},
    id='my-graph2'
),

])

if __name__ == '__main__':
    if os.path.exists('raw_data.csv'):
        os.remove('raw_data.csv')
    else:
        print("The file does not exist")
    threading.Thread(target = counter().app_run).start()
    threading.Thread(target = counter().sentiment).start()
        
