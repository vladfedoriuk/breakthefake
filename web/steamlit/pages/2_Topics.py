import streamlit as st
import pickle as pkl
import plotly.graph_objects as go
import numpy as np

st.markdown("# Topics")
st.markdown("""
This is a topic modelling overview.
It presents the topics in the dataset we scraped.

The topics are clustered using NMF and LDF.
They are then visualised using t-SNE, a dimensionality reduction technique.

Of course, those topics are unsupervised. Hover over the points to see the topic name.  
""")


@st.cache
def load_data():
    data = pkl.load(open("./data/topics.pkl", "rb"))
    return data


def topic_modelling_graph(label="y_nmf"):
    data = load_data()
    topics = data["nmf"]
    topic_names = {str(k): ",".join(v) for k, v in topics.items()}
    topic_hover = [topic_names[str(x)] for x in data[label]]
    X = np.asarray(data["X"])
    fig = go.Figure(data=go.Scatter(
        x=X[:, 0],
        y=X[:, 1],
        mode="markers",
        text=topic_hover,
        marker=dict(
            color=data[label],
            colorscale="Viridis",
        ),
    ))
    fig.update_layout(template="plotly_white",
                      title="Topic Modelling",
                      xaxis={
                          "showgrid": False,
                          "showticklabels": False,
                      },
                      yaxis={
                          "showgrid": False,
                          "showticklabels": False,
                      },
                      width=1400,
                      height=800)
    st.plotly_chart(fig, use_container_width=False)


topic_modelling_graph()
