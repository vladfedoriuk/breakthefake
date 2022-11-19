# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import json

import dash
from dash.dependencies import Input, Output, State
from elements import ArticleElement
from dash import html, dcc


app = dash.Dash(__name__,
                include_assets_files=True)

article_summary_layout = html.Div([
        html.H2('List of articles'),
        html.Br(),
        html.Div([
            html.Button('Get articles', id='btn_get_articles', n_clicks=0),
            dcc.Input(id='txt_search',
                      type='text',
                      placeholder='Search...')
        ]),
        html.Div(id='article_list'),
    ],
    style={'display': 'flex', 'flex-direction': 'row'}
)

statistics_layout = html.Div([

])

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="News summary",
                children=[article_summary_layout]),
        dcc.Tab(label="Statistics & analysis",
                children=[statistics_layout])
    ])
])


@app.callback(
    Output('article_list', 'children'),
    Input('btn_get_articles', 'n_clicks'),
    State('txt_search', 'value')
)
def get_articles(n_clicks, search_value):
    # Get articles from the backend
    if n_clicks < 1:
        return html.Div()
    with open('example2.json') as f:
        f_data = json.loads(f.read())
        article_elements = [ArticleElement(data).to_html() for data in f_data['articles']]
    # return html.Div(children=article_elements)
    return article_elements
    # return html.Div(children=[a_element.to_html for a_element in article_elements])


if __name__ == '__main__':
    app.run_server(debug=True, port=10050)
