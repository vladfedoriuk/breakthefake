import spacy
import pytextrank
import json
import glob

nlp = spacy.load("pl_core_news_sm")
nlp.add_pipe("textrank")
MAX_PHRASES = 5

ARTICLE_SRC = "data/tvp_articles/*.json"


def tag_document(article_doc):
    doc = nlp(article_doc['content'])
    tags = []
    for phrase in doc._.phrases[:MAX_PHRASES]:
        tags.append(phrase.text)
    article_doc['tags'] = tags
    return article_doc


if __name__ == "__main__":
    for json_path in glob.iglob(ARTICLE_SRC):
        article_doc = json.load(open(json_path, "r"))
        tagged = tag_document(article_doc)
        print(tagged['tags'])