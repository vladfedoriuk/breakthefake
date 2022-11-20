from functools import reduce
import streamlit as st
import pandas as pd
import os

categories = [
    "Ministerstwo Finansów",
    "Finanse publiczne",
    "Podatki",
    "Administracja",
    "KPO",
    "Projekty",
    "Instytucje",
    "Opłaty",
    "Przedstawiciele MF",
]

topics = pd.read_excel("data/categories.XLSX")["Unnamed: 2"].values[1:]

STYLE_SHEET = os.path.join(os.path.dirname(__file__), "style.css")
MAX_ENTRIES = 10
_EMPTY = "(brak)"


@st.cache
def load_data():
    data = pd.read_csv("./data/database_with_proba.csv", lineterminator="\n")
    data = data.dropna(subset=["summary"])
    data = data[~data["categories"].isnull()]
    data = data[~data["subjects"].isnull()]
    return data


def filter_data(data, query: dict):
    var = data
    if "search" in query:
        var = (
            var[
                reduce(
                    lambda a, b: a & b,
                    [
                        var["summary"].str.contains(word, case=False)
                        for word in query["search"].split(" ")
                    ],
                )
            ]
            if query["search"]
            else var
        )
    if "category" in query:
        var = (
            var[
                reduce(
                    lambda a, b: a | b,
                    [
                        var["categories"].str.contains(category_, case=False)
                        for category_ in query["category"]
                    ],
                )
            ]
            if query["category"]
            else var
        )
    if "probability_fake" in query:
        var = (
            var[var["probability_fake"] < query["probability_fake"]]
            if query["probability_fake"]
            else var
        )
    return var


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
    author = data_row["author"]
    if isinstance(author, str):
        author = author.split(":")
        author = author[-1]
    else:
        author = _EMPTY
    st.markdown(
        f"""
          <h6 class="italic-text">{author or _EMPTY} </h6>
          """,
        unsafe_allow_html=True,
    )
    date_ = str(data_row["date"])
    if date_ == "nan":
        date_ = _EMPTY
    st.markdown(
        f"""
        <h6 class="italic-text">{date_ or _EMPTY} </h6>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'**Źródło**: [{data_row["source"]}]({data_row["url"]})')
    claimed_source = data_row["claimed_source"]
    if isinstance(claimed_source, str):
        claimed_source =claimed_source.split(":")
        claimed_source = claimed_source[-1]
    else:
        claimed_source = _EMPTY

    st.markdown(f"**Podane Źródło**: {claimed_source}")
    st.markdown("")
    st.markdown(f'{data_row["summary"]}')

    st.markdown(f"##### Tagi")
    tags = [x_.strip() for x_ in data_row["tags"].split(", ")]

    st.markdown(
        f"""
        {''.join(
            f'<span class="tag tag-green">{tag.strip()}</span>'
            for tag in tags
        )
        }
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f"##### Kategorie")
    categories = [x_.strip() for x_ in data_row["categories"].split(", ")]

    st.markdown(
        f"""
            {''.join(
            f'<span class="tag tag-purple">{category.strip()}</span>'
            for category in categories
        )
        }
            """,
        unsafe_allow_html=True,
    )

    st.markdown(f"##### Tematy")
    categories = [x_.strip() for x_ in data_row["subjects"].split(", ")]

    st.markdown(
        f"""
                {''.join(
            f'<span class="tag tag-purple">{category.strip()}</span>'
            for category in categories
        )
        }
                """,
        unsafe_allow_html=True,
    )
    probability_fake_column, _ = st.columns(2)
    probability_fake_value = data_row.get("probability_fake")
    if probability_fake_value is not None:
        probability_fake_value *= 100
    with probability_fake_column:
        st.metric(
            "Pewność fake'a",
            value=f'{probability_fake_value:.3g}%' if probability_fake_value is not None else _EMPTY
        )


data = load_data()
print(data.columns)

icon("search")
st.markdown("### Wyszukaj")
with st.form(key="form"):
    search = st.text_input("Search", placeholder="Search...")

    category = st.multiselect(
        "Kategorie",
        options=categories,
        key="category",
        help="Wybierz kategorie, do których powinien należeć artykuł",
    )
    topic = st.multiselect(
        "Temat",
        options=topics,
        key="temat",
        help="Wybierz tematy",
    )
    probability_fake = st.slider(
        "Prawdopodobieństwo fake'a",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.01,
        key="prob",
        help="Pewność algorytmu, że news jest fakiem.",
    )
    submitted = st.form_submit_button(label="Search")

data_load_state = st.text("Loading data...")
data_load_state.text("Done!")

if submitted:
    view = filter_data(data, {"search": search, "category": category, "probability_fake": probability_fake})
    if not len(view):
        st.warning("Nie znaleziono artykułów.")
        st.stop()
    with st.container():
        st.markdown(f"## Top {MAX_ENTRIES} artykułów")
        for _, row in list(view.iterrows())[MAX_ENTRIES:0:-1]:
            add_row(row)

local_css(STYLE_SHEET)
remote_css("https://fonts.googleapis.com/icon?family=Material+Icons")
remote_css("ttps://unpkg.com/tachyons@4.12.0/css/tachyons.min.css")
