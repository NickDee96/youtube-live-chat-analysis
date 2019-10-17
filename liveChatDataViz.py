import pandas as pd
import numpy as np
import plotly
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=20,stop_words="english")



mask = np.array(Image.open("images/kenyanFlag.jpg"))
image_colors = ImageColorGenerator(mask)


df=pd.read_csv("liveChatData.csv")
## Top 50 Most active users
top=df.Author.value_counts().head(20).to_frame().reset_index()
top.columns=["Author","Count"]

fig=go.Figure()
fig=fig.add_trace(
    go.Barpolar(
        theta=top.Author,
        r=top.Count,
        width=5,
        marker=dict(
            color=top.Count,
            colorscale="magma",
        ),
        marker_line_color="grey",
        marker_line_width=2,
        opacity=0.8
    )
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout=html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1(
                    children="YouTube Live Chat Analysis",
                    style={
                        'text-align': 'center'
                    }
                )
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(
                    id="comparison_plot",
                    figure=fig
                )
            ])
        ]),
        dbc.Col([
            html.Div(
                id="wordcloud"
            )
        ])
    ])
])

@app.callback(
    Output("wordcloud","children"),
    [Input("comparison_plot","hoverData")]
)

def get_wordcloud(hoverData):
    pers=hoverData["points"][0]["theta"]
    msg=df[df.Author==pers].reset_index(drop=True)["Message"]
    photo=df[df.Author==pers].reset_index(drop=True)["Photo"][0]
    X = vectorizer.fit_transform(msg)
    words=vectorizer.get_feature_names()
    #plt.figure(figsize=[7,7])
    #wordcloud_ke = WordCloud( background_color="white", mode="RGBA", max_words=30, mask=mask).generate(" ".join(list(msg)))
    #fig=plt.imshow(wordcloud_ke .recolor(color_func=image_colors), interpolation="bilinear")
    #fig = mpl_to_plotly(fig)
    child=html.Div([
        html.H3(
            children=pers
        ),
        html.Img(
            src=photo,
            style={
                'height' : '20%',
                'width' : '20%'}
        ),
        html.Ul(
            [html.Li(x) for x in words ]
        )
    ])
    return child
    

app.run_server()