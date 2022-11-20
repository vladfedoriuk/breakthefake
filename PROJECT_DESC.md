## *HackNews* submission
<img style="float: right top; max-width: 250px;" src="https://upload.wikimedia.org/wikipedia/commons/e/e8/Logo_Ministerstwa_Finansów.svg">

--- 
# Key features:

 - [x] scalable (Docker + Digital Ocean)
 - [x] low-cost inference (lightweight models for fake news)
 - [x] multi-source scrapping
# Overview
This is a web app that allows you to search for news articles and see how
they are related to each other. It uses a machine learning model to clasisfy fake news,
categorise the articles and also show summary statistics about the articles
Full ML functionality: 

- article sentiment, 
- useful statistics and visualization about the collected articles.
- hate speech presence, and 
- possibility of a fake news

The program is a web app consisting of two pages:

- The news summary page with filtering options
- The statistical visualization dashboard page
- About the project page

### Quick Guide? :rocket:
See `Readme.md` for more details.
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

#### Authors
- FullStek

# Data sources
We wrote automatic scrappers (`./scrapper` folder) to collect data from the following sources:
- [tvp](https://www.tvp.pl/)
- [pch24](https://www.pch24.pl/)
- [wp](https://www.wp.pl/)
- [wpolityce](https://www.wpolityce.pl/)

# Models
We used the following models:
- [spacy](https://spacy.io/) for lemma analysis and extractive summarization
- hate-speach classification model from Hugging Face trained on PL corpus
- sentiment analysis model from Hugging Face trained on PL corpus
- custom trained model that consists of:
  - LDA topic modelling for discovering topics
  - fake news detection model based on SVM + TF-IDF + Bayesian optimisation
    - here, we used custom scrapped [demagog](https://demagog.org.pl/) dataset.
    - see the scrapping folder for how this was obtained.
# Project development cycle 

1. Scraping selected news portals and extracting chosen information (article title, summary, contents, author, and date)
2. Storing article information (including analysis) in a database.
3. Implementing AI/Machine Learning models to perform sentiment analysis, hate speech recognition and fake news detection.
4. Creating a front-end app communicating with the database.

## Technologies used

We used a multitude of technologies to create the project. The list includes: 

- Python
- Docker [docker](https://www.docker.com/)
  - used to build a scalable container
- DigitalOcean [digitalocean](https://www.digitalocean.com/)
  - used for deployment of the app
- Streamlit [streamlit](https://www.streamlit.io/)
  - used to create a front-end app
  - used to create a dashboard
  - search news  and summary pages
- Scikit-Learn
  - Training SVM
  - Tf-idf vectorizer
  - LDA topic modelling
  - Evaluation metrics
- Pandas
  - Data manipulation
- HuggingFace
  - Transformers (hate speech + sentiment analysis)
  - Tokenizers
- PyTextRank + Spacy
  - Extractive summarization
  - Automatic tag extraction 
  - Lemmatization
  - used `pl_core_news_sm` model for speed
- Plotly
  - Data visualization
- Beautiful Soup
  - Web scrapping (+requests)