# breakthefake


## Models
You need to download Polish language model from spacy: 
```bash
python3 -m spacy download pl_core_news_sm
```

## Streamlit 
```bash 
streamlit run ./web/steamlit/search.py --server.runOnSave true  
```



# TODO:

- [ ] Docker 
- [ ] Wizualizacja danych (Bar chart do tagów) (stacked bar chart do tagów i kategorii w zalenośi od źródła)
- [ ] % fake news per źródło 
- [ ] Regex na znane wyraenia indykujące fake news 
- [ ] Korleacje między newsami 
- [ ] Analiza sentymentu [Piotr]
- [ ] Frontend: ma wyświetlac prawdopodobienstwo fake news + sentyment + tagi + kategorie + źródło + data + tytuł + treść [Władek]
- [ ] Prezentacja!!!

- [ ] Kto odpowiada za najwiecej fake news -- z demagoga? Top kłamczuszków xd
- [ ] Najbardziej wydatne słowa przy fake news.