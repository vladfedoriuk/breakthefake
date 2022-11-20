import streamlit as st
import pandas as pd
import os

STYLE_SHEET = os.path.join(os.path.dirname(__file__), "style.css")
MAX_ENTRIES = 10
_EMPTY = "(brak)"


@st.cache
def load_data():
    data = pd.read_csv("./data/database.csv", lineterminator="\n")
    data = data[~data["categories"].isnull()]
    return data


def filter_data(data, phrase):
    return data[data["summary"].str.contains(phrase, case=False)] if phrase else data


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


def add_row(data_row):
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(f'### {data_row["title"]}')
    author, source, date, url = st.columns(4)
    st.markdown(
        f"""
          <h6 class="italic-text">{data_row["author"] or _EMPTY} </h6>
          """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <h6 class="italic-text">{data_row["date"] or _EMPTY} </h6>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'**Źródło**: [{data_row["source"]}]({data_row["url"]})')
    st.markdown("")
    st.markdown(f'{data_row["summary"]}')

    st.markdown(f"##### Tagi")
    tags = [x_.strip() for x_ in data_row["tags"].split(", ")]

    st.markdown(
        f'''
        {''.join(
            f'<span class="tag tag-green">{tag.strip()}</span>'
            for tag in tags
        )
        }
        ''',
        unsafe_allow_html=True
    )

    st.markdown(f"##### Kategorie")
    categories = [x_.strip() for x_ in data_row["categories"].split(", ")]

    st.markdown(
        f'''
            {''.join(
            f'<span class="tag tag-purple">{category.strip()}</span>'
            for category in categories
        )
        }
            ''',
        unsafe_allow_html=True
    )


icon("search")
st.markdown("# Search")
selected = st.text_input("Search", placeholder="Search...")
button_clicked = st.button(
    "Search",
)
data_load_state = st.text("Loading data...")
data = load_data()
print(data.columns)
data_load_state.text("Done! (using st.cache)")
main_view = st.dataframe(data, use_container_width=True)

if button_clicked:
    view = filter_data(data, selected)
    with st.container():
        st.markdown("## Top 10 artykułów")
        for _, row in list(view.iterrows())[9:0:-1]:
            add_row(row)


local_css(STYLE_SHEET)
remote_css("https://fonts.googleapis.com/icon?family=Material+Icons")
remote_css("ttps://unpkg.com/tachyons@4.12.0/css/tachyons.min.css")
