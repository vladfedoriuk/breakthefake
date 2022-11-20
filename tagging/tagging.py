import spacy
import pytextrank
import json
import glob
from typing import List, Dict, Any
import math
import os
import re
import pandas as pd
import random
from tqdm import tqdm

nlp = spacy.load("pl_core_news_sm")
nlp.add_pipe("textrank")
MAX_PHRASES = 5
MAX_LEN = 1000000 // 2
MAX_PER_SOURCE = 2000
ARTICLE_SRC = "data/tvp_articles/*.json"
ARTICLE_DST = "data/database.csv"
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
        self.rgx_set = self.extract_categories_rgx()

    def clean_text(self, text: str) -> str:
        forbidden_chars = (
            '\n',
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
        text = text.replace('""', '"')
        text = text.replace('  ', ' ')
        return text

    def __call__(self, article_json_filename: os.PathLike) -> Dict[str, Any]:
        """Extract the metadata from the article."""
        article_doc = json.load(open(article_json_filename, "r"))
        if 'content' not in article_doc:
            print(article_json_filename)
            return None
        article_text = self.clean_text(article_doc["content"])
        for k in ('author', 'date'):
            article_doc[k] = article_doc[k].strip()
        article_doc['content'] = article_text
        doc = nlp(article_doc["content"][:MAX_LEN])
        article_doc['tags'] = self.tag_document(doc)
        article_doc['summary'] = self.extract_summary(doc).replace("  ", " ")
        cats, subjects = self.find_categories(article_text)
        article_doc['categories'] = cats
        article_doc['subjects'] = subjects
        return article_doc

    def tag_document(self, doc: spacy.tokens.Doc) -> List[str]:
        """Extract the most important phrases from the article."""
        tags = []
        for phrase in doc._.phrases[:self.max_phrases]:
            tags.append(phrase.text)
        return ", ".join(set(tags))

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
        return " ".join(sent_text.values())

    def find_categories(self, article_text: str):
        """Use regex to find the subjects/categories of the article."""
        article_cats, article_subjects = [], []
        for category, rgx in self.rgx_set.items():
            search_res = rgx.search(article_text)
            if search_res:
                # print(search_res)
                article_subjects.append(search_res.group(0))
                article_cats.append(category)

        return ", ".join(article_cats), ", ".join(article_subjects)

    def extract_categories_rgx(self):
        minsterstwo = [
            'ministerstwo', 'minister', 'ministrowi', 'ministrze', 'ministrów',
            'ministerstwu', 'ministerstwie', 'ministerstwa'
        ]
        wiceminister = ['wice' + x for x in minsterstwo]
        rzecznik = [
            'rzecznik',
            'rzecznika',
            'rzecznikowi',
            'rzeczniczce',
            'rzeczniczka',
        ]

        categories = {
            'Ministerstwo Finansów': [
                'MF',
                'GIIF',
                'Generalny Inspektor Informacji Finansowej',
                'Generalnego Inspektoratu Informacji Finansowej',
                *[x + " finansów" for x in minsterstwo],
                *[x + " finansów" for x in wiceminister],
                *[x + " finansów" for x in rzecznik],
                *[x + " MF" for x in rzecznik],
            ],
            'Finanse publiczne': [
                'finanse publiczne', 'budżet', 'budżetu', 'budżetem',
                'budżetowi', 'budżetach', 'finansów publicznych',
                'finansów publicznego', 'finansów publicznego',
                'finansów publicznym', 'finansów publicznymi',
                'dług publiczny', 'długu publicznego', 'SRW', 'obligacje',
                'obligacje skarbowe', 'obligacji skarbowych', 'obligacji',
                'deficyt', 'deficytowi', 'hazard'
            ],
            'Podatki': [
                'podatki',
                'podatków',
                'podatku',
                'podatkiem',
                'podatkach',
                'CIT',
                'PIT',
                'VAT',
                'akcyza',
                'akcyzie',
                'cło',
                'cłach',
            ],
            'Administracja': [
                'KAS', 'administracja skarbowa', 'administracji skarbowej',
                'skarbowy', 'celna', 'celno-skarbowa', 'celno-skarbowej'
            ],
            'KPO': ['kpo', 'krajowy plan odbudowy'],
            'Projekty': [
                'e-pit',
                'epit',
                'e-podatki',
                'epodatki',
                'e-podatków',
                'epodatków',
                'e-podatku',
                'epodatku',
                'e-podatkiem',
                'epodatkiem',
                'polski ład',
                'podatek reklamowy',
                'podatek od reklam',
                'podatku od reklam',
                'podatku reklamowego',
                'finansoaktywni',
                'polska agencja nadzoru finansowego',
                'polska agencja nadzoru audytowego',
                'wakacje kredytowe',
            ],
            'Instytucje': [
                'nbp', 'bank centralny', 'banku centralnego',
                'narodowy bank polski', 'MFW',
                'międzynarodowy fundusz walutowy',
                'międzynarodowego funduszu walutowego',
                'komisja nadzoru finansowego', 'komisji nadzoru finansowego',
                'KNF'
            ],
            'Opłaty': ['e-toll', 'etoll', 'viatoll', 'e-myto', 'emyto'],
            'Przedstawiciele MF': [
                'Rzeczkowska', 'Rzecznik Prasowy MF', 'Rzecznik Finansów',
                'Rzecznik Finansów Publicznych', 'Chałupa', 'Patkowski',
                'Skuza', 'Czernicki', 'Szwarc', 'Gojny', 'Soboń', 'Szweda',
                'Zbaraszczuk', 'Pasieczyńska', 'Dudek'
            ]
        }

        regex_cats = {}
        for cat, entires in categories.items():
            or_sel = "|".join(entires)
            regex_cats[cat] = re.compile(or_sel, re.IGNORECASE)

        return regex_cats


if __name__ == "__main__":
    extractor = MetadataExtractor()
    articles = []
    all_sources = [
        'data/tvp_articles',
        'data/wp_articles',
        'data/pch24_articles',
        'data/wpolityce_articles',
    ]
    all_article_paths = []
    for src in all_sources:
        all_article_paths.extend(glob.glob(f'{src}/*.json')[:MAX_PER_SOURCE])
    # random.shuffle(all_article_paths)
    for json_path in tqdm(all_article_paths):
        new_article = extractor(json_path)
        if new_article is None:
            continue
        articles.append(new_article)

    df = pd.DataFrame.from_records(articles)
    df.to_csv(ARTICLE_DST, index=False)
