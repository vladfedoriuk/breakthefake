from dash import html
import json


class ArticleElement:
    def __init__(self, data):
        # data in JSON - to string
        # self.data = json.loads(data)
        self.data = data
        # self.author =

    def to_html(self):
        return html.Div(
            # [
            #     html.H4(self.data['title'] + ' -> ' + self.data['author']),
            #     html.Br(),
            #     html.H5(self.data['author']),
            # ]
            children=[
                html.H4(self.data["title"]),
                html.Br(),
                # html.H5(self.data['claimed_source'] + ', ' + self.data['date']),
                # html.Br(),
                html.H5(self.data["author"]),
                html.Br(),
            ]
        )
