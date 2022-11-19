import spacy
import pytextrank
import json
import glob
from typing import List, Dict, Any
import math
import os
import re

nlp = spacy.load("pl_core_news_sm")
nlp.add_pipe("textrank")
MAX_PHRASES = 5

ARTICLE_SRC = "data/tvp_articles/*.json"
emoji_pattern = re.compile(
    "["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+",
    flags=re.UNICODE)
to_remove = [
    'Prezydent Andrzej Duda w Przewodowie Święto Niepodległości Prezydent kibicował skoczkom Premier w bazie lotnictwa w Łasku Wizyta prezydenta w CSAiU w Toruniu Inauguracja roku na UE w Krakowie Akcja #sadziMY z udziałem prezydenta Symboliczne otwarcie Baltic Pipe Święto „Wdzięczni Polskiej Wsi” Prezydent na sesji ONZ'
]


class MetadataExtractor:

    def __init__(self, max_phrases: int = 5, max_sents: int = 3) -> None:
        self.max_phrases = max_phrases
        self.max_sents = max_sents

    def clean_text(self, text: str) -> str:
        forbidden_chars = (
            '-',
            '– ',
            '@',
            '+',
            *to_remove,
        )  # watch out for the - it's U+2013
        for char in forbidden_chars:
            text = text.replace(char, '')
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'pic.twitter\S+', '', text)
        text = emoji_pattern.sub(r'', text)
        text = text.replace('..', '.')
        text = text.replace('  ', ' ')
        return text

    def __call__(self, article_json_filename: os.PathLike) -> Dict[str, Any]:
        """Extract the metadata from the article."""
        article_doc = json.load(open(article_json_filename, "r"))
        article_text = self.clean_text(article_doc["content"])
        article_doc['content'] = article_text
        doc = nlp(article_doc["content"])
        article_doc['tags'] = self.tag_document(doc)
        article_doc['summary'] = self.extract_summary(doc)
        return article_doc

    def tag_document(self, doc: spacy.tokens.Doc) -> List[str]:
        """Extract the most important phrases from the article."""
        tags = []
        for phrase in doc._.phrases[:self.max_phrases]:
            tags.append(phrase.text)
        return tags

    def extract_summary(self, doc: spacy.tokens.Doc) -> List[str]:
        """Produce a summary of the article. Extracts the most important sentences."""
        sent_bounds = [[s.start, s.end, set([])] for s in doc.sents]
        unit_vector = []
        # the ._._phrases should've been sorted by score
        for phrase_id, p in enumerate(doc._.phrases):
            unit_vector.append(p.rank)
            for chunk in p.chunks:
                for sent_start, sent_end, sent_vector in sent_bounds:
                    if chunk.start >= sent_start and chunk.end <= sent_end:
                        sent_vector.add(phrase_id)
                        break
        sum_ranks = sum(unit_vector)
        unit_vector = [rank / sum_ranks for rank in unit_vector]
        sent_rank = {}
        sent_id = 0
        for sent_start, sent_end, sent_vector in sent_bounds:
            sum_sq = 0.0
            for phrase_id in range(len(unit_vector)):
                if phrase_id not in sent_vector:
                    sum_sq += unit_vector[phrase_id]**2.0

            sent_rank[sent_id] = math.sqrt(sum_sq)
            sent_id += 1
        sent_rank = sorted(sent_rank.items(), key=lambda x: x[1], reverse=True)
        all_sents = list(doc.sents)
        sent_text = {
            idx: all_sents[idx].text
            for (idx, _) in sent_rank[:self.max_sents]
        }
        return list(sent_text.values())


if __name__ == "__main__":
    extractor = MetadataExtractor()
    for json_path in glob.iglob(ARTICLE_SRC):
        new_article = extractor(json_path)
        print(new_article['summary'])