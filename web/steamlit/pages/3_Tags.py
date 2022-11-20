import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.graph_objects as go
from collections import Counter

N = 30
st.markdown("""
    # TRUE VS FAKE

    Here we summarise the number of fake news. 
    We look for the most common persons of appearing in the news.
    Then, we compare how many fake news made that person a target.
    """)

DATABASE_PATH = './scrapping/demagog/dataset.csv'


@st.cache
def load_data():
    data = pd.read_csv(DATABASE_PATH)
    return data


def get_author_counts(db_view):
    counts = Counter(db_view['author'].str.lower())
    counts = {k: v for k, v in counts.most_common(N)}
    X = list(counts.keys())
    Y = list(counts.values())
    return X, Y


def get_fake_valid_plot(db_view):
    fakes = db_view.loc[db_view['label'].isin(['Fałsz', 'Częściowy fałsz'])]
    valid = db_view.loc[db_view['label'].isin(['Prawda'])]

    X1, Y1 = get_author_counts(fakes)
    X2, Y2 = get_author_counts(valid)

    fig = go.FigureWidget(data=[
        go.Bar(name='Fake', x=X1, y=Y1),
        go.Bar(name='True', x=X2, y=Y2)
    ])
    fig.update_layout(
        barmode='stack',
        uniformtext=dict(mode="hide", minsize=10),
    )
    st.plotly_chart(fig, use_container_width=True)


get_fake_valid_plot(load_data())

st.markdown("""
    # TOPIC MODELLING
    Our sources -- here we look at the sources we scraped.
    The datasets e.g.:
    - demagog
    - pch24
    - tvp
    - wpolityce
    - wgospodarce
    - wp
    - pap
    """)
