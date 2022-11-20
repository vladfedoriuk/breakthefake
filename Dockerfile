FROM ubuntu:latest

WORKDIR /app 

ENV STREAMLIT_SERVER_PORT=80
EXPOSE ${STREAMLIT_SERVER_PORT}

RUN apt-get update && \
    apt-get install -y python3 python3-pip
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install streamlit pandas plotly numpy openpyxl

COPY web/steamlit /app/web/steamlit
COPY data/database_no_content.csv /app/data/database_no_content.csv
COPY data/database_with_proba.csv /app/data/database_with_proba.csv
COPY data/database_with_hate.csv /app/data/database_with_hate.csv

COPY data/topics.pkl /app/data/topics.pkl
COPY data/categories.XLSX /app/data/categories.XLSX
COPY scrapping/demagog/dataset.csv /app/scrapping/demagog/dataset.csv


CMD ["streamlit", "run", "/app/web/steamlit/Search.py"]