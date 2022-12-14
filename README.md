# breakthefake

General description of the project is in the [PROJECT_DESC.md](PROJECT_DESC.md) file.

## Models
You need to download Polish language model from spacy: 
```bash
python3 -m spacy download pl_core_news_sm
```

The trained models are in the `models` folder.
The training script can be found in `notebooks/train_fake.ipynb` folder.

### Dataset statement
The model has been trained on the scrapped dataset from `demagog.org.pl` website.  
The scrapping script can be found in `scrapper/demagog_scrapper.py` folder.  
We do not provide the full scrapped datasets (.html files) due to its size.  
We only distill into .csv files the data that we used for training the model.

### Model performance
- accuracy on the test set: 0.76
- recall on the test set: 0.52
- precision on the test: 0.78

## Streamlit 
```bash 
streamlit run ./web/steamlit/search.py --server.runOnSave true  
```
Streamlit folder is organised in the following way:

- Search.py -- main page of the app with search
- pages -- contain all the subpages of the app
  - Topics.py -- topic modelling
  - Tags.py -- tag modelling 
  - About.py -- infopage about the solution 


## Docker 
Use `Makefile` to build and push projects.

To run the frontend in docker you need to build the image and run the container. 
```bash
docker build -t breakthefake .
docker run -p 80:80 breakthefake
```
Alternatively, you can run from the docker hub:
```bash
docker run -p 80:80 lemurpwned/hack-news:latest
```

# Digital Ocean
To run the app on Digital Ocean you need to create a droplet with docker installed. 
Use the pushed Docker image:
```bash
export VERSION=1.0
docker run -p 80:80 lemurpwned/hack-news:$VERSION
```



# TODO:

- [x] Docker 
- [x] Wizualizacja danych (Bar chart do tagów) (stacked bar chart do tagów i kategorii w zalenośi od źródła) - IN PROGRESS - Piotr
- [x] % fake news per źródło 
- [ ] Regex na znane wyraenia indykujące fake news 
- [ ] Korleacje między newsami 
- [x] Analiza sentymentu [Piotr]
- [x] Frontend: ma wyświetlac prawdopodobienstwo fake news + sentyment + tagi + kategorie + źródło + data + tytuł + treść [Władek]

- [x] Kto odpowiada za najwiecej fake news -- z demagoga? Top kłamczuszków xd
- [ ] Najbardziej wydatne słowa przy fake news.
- [x] hate speech classification - IN PROGRESS - VLAD
