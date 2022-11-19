from functools import partial
import streamlit as st
import pandas as pd
import os

STYLE_SHEET = os.path.join(os.path.dirname(__file__), 'style.css')
MAX_ENTRIES = 10


@st.cache
def load_data():
    data = pd.read_csv('./data/database.csv')
    data['summary'] = data['summary'].apply(lambda x: ' '.join(x))

    return data


def filter_data(data, phrase):
    return data[data['summary'].str.contains(phrase, case=False)] if phrase else data


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>',
                unsafe_allow_html=True)


def add_row(data_row):
    st.write(f"""
    <div class="row">
        <div class="col s12 m6">
            <div class="card blue-grey darken-1">
                <div class="card-content white-text">
                    <span class="card-title
                    truncate">{data_row['title']}</span>
                    <p>{data_row['summary']}</p>
                </div>
                <div class="card-action">

                    <a href="{data_row['url']}">Link</a>
                </div>
            </div>
        </div>
    </div>
    """,
             unsafe_allow_html=True)


icon("search")
st.markdown("# Search")
data = load_data()
selected = st.text_input("Search", placeholder="Search...")
button_clicked = st.button("Search", )
data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache)")
main_view = st.dataframe(data, use_container_width=True)
st.markdown(

    f"""
    # To jest tytuł newsa
    To jest podsumowanie newsa 2

    Source: [link](https://www.pch24.pl/)  
    Score: **0.5**
    źródło: [link](https://www.pch24.pl/)
    """
)

st.markdown(

    f"""
    # To jest tytuł newsa
    To jest podsumowanie newsa 

    Source: [link](https://www.pch24.pl/)  
    Score: **0.5**
    źródło: [link](https://www.pch24.pl/)
    """
)
if button_clicked:
    view = filter_data(data, selected)
    # with st.expander("Cards"):
    #     i = MAX_ENTRIES
    #     for _, row in view.iterrows():
    #         add_row(row)
    #         i -= 1
    #         if i == 0:
    #             break
    # # st.map(view)
    main_view.dataframe(view, use_container_width=True)
    # main_view = st.dataframe(view, width=None, height=None)

local_css(STYLE_SHEET)
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
