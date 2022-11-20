import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter
import plotly.express as px

N = 30
st.markdown("""
    # TRUE VS FAKE

    Here we summarise the number of fake news. 
    We look for the most common persons of appearing in the news.
    Then, we compare how many fake news made that person a target.

    ### Remark
    Interestingly, the prominence of the person does not correlate 
    too strongly with # of fake news. See `Władysław Kosiniak-Kamysz`
    and `Elżbieta Rafalska` for example.
    """)

DATASET_PATH = './scrapping/demagog/dataset.csv'
DATABASE_PATH = './data/database.csv'


@st.cache
def load_data():
    data = pd.read_csv(DATASET_PATH)
    return data


@st.cache
def load_db():
    df = pd.read_csv(DATABASE_PATH, lineterminator='\n')

    def split_strip(string):
        return list(map(str.strip, string.split(',')))

    df = df[['title', 'claimed_source', 'categories']]

    # Drop N/A values in categories
    df = df[df['categories'].notna()]
    df = df[df['claimed_source'].notna()]
    df['claimed_source'] = df['claimed_source'].apply(
        lambda x: x.replace("źródło:", "").strip())
    # Convert comma separated strings to lists of strings
    df['categories'] = df['categories'].apply(split_strip)
    # Unwind categories
    df = df.explode('categories')
    df_grouped = df.groupby(['claimed_source', 'categories']).count()
    df_grouped_by_source = df.groupby('claimed_source').count()
    df_grouped = df_grouped.iloc[1:]
    df_grouped['frequency'] = df_grouped['title']
    df_grouped['source_sum'] = df_grouped['title']

    for i, row in df_grouped.iterrows():
        df_grouped.at[i, 'source_sum'] = float(
            df_grouped_by_source.loc[i[0]]['title'] * 1.0)

    df_grouped['frequency'] = df_grouped['title'] / df_grouped['source_sum']
    return df_grouped.reset_index()


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

    fig = go.Figure(data=[
        go.Bar(name='Fake', x=X1, y=Y1),
        go.Bar(name='True', x=X2, y=Y2)
    ])
    fig.update_layout(
        barmode='stack',
        uniformtext=dict(mode="hide", minsize=10),
    )
    fig.update_xaxes(tickangle=30)
    st.plotly_chart(fig, use_container_width=True)


def get_category_counts(db_view):

    df = load_db()
    fig = px.bar(
        df,
        x="claimed_source",
        y="frequency",
        color="categories",
        title="Frequencies of category appearing among sources",
    )
    fig.update_layout(xaxis={'title': 'source'})
    st.plotly_chart(fig, use_container_width=True)


get_fake_valid_plot(load_data())

st.markdown("""
    # Dataset
    Our sources -- here we look at the sources we scraped.
    The datasets we scrapped with out scrappers contain for instace:
    - demagog
    - pch24
    - tvp
    - wpolityce
    - wgospodarce
    - wp
    - pap
    - Twitter
    
    ## Category vs Source
    Below, click on a category in the legend to remove it from a view.
    """)

get_category_counts(load_db())
