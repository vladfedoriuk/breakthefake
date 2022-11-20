import streamlit as st
import pickle as pkl
import plotly.graph_objects as go
import numpy as np

st.markdown("# Topics")


@st.cache
def load_data():
    data = pkl.load(open('./data/topics.pkl', 'rb'))
    return data


def topic_modelling_graph():
    data = load_data()
    X = np.asarray(data['X'])
    fig = go.Figure(data=go.Scatter(x=X[:, 0],
                                    y=X[:, 1],
                                    mode='markers',
                                    marker=dict(
                                        color=data['y_nmf'],
                                        colorscale='Viridis',
                                    )))
    fig.update_layout(template='plotly_white',
                      title='Topic Modelling',
                      xaxis={
                          'showgrid': False,
                      },
                      yaxis={
                          'showgrid': False,
                      })
    st.plotly_chart(fig, use_container_width=True)


topic_modelling_graph()