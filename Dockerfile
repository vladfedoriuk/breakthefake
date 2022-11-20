FROM ubutnu:latest

WORKDIR /app 

COPY web/steamlit /app/web/steamlit
 
CMD ["streamlit", "run", "web/steamlit/app.py"]