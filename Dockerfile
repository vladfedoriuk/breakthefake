FROM ubuntu:latest

WORKDIR /app 

COPY web/steamlit /app/web/steamlit
COPY data/database_no_content.csv /app/data/database_no_content.csv
COPY data/topics.pkl /app/data/topics.pkl
ENV STREAMLIT_SERVER_PORT=80

EXPOSE ${STREAMLIT_SERVER_PORT}
RUN apt-get update && \
    apt-get install -y python3 python3-pip
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install streamlit pandas plotly numpy openpyxl

CMD ["streamlit", "run", "/app/web/steamlit/search.py"]