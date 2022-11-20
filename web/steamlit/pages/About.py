import streamlit as st

st.header("About")
st.markdown(
    """
    # Break the fake news cycle

    ## What is this?
    This is a web app that allows you to search for news articles and see how
    they are related to each other. It uses a machine learning model to clasisfy fake news,
    categorise the articles and also show summary statistics about the articles.

    ## Quick Guide?
    You can search for articles by entering a keyword in the search bar. The results will be
    displayed in a table. You can click on the link of the article to see the full article.

    The article contains: 
    - The title of the article
    - The summary of the article
    - The link to the article
    - The date the article was published and the author, if available
    - The category of the article
    - The probability of the article being fake news
    - The sentiment of the article

    ## Authors
    - FullStek
    """
)
