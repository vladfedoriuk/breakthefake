from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from random import shuffle
import pickle as pkl
import glob
import ujson
from sklearn import svm
"""
Inspired by https://github.com/karpathy/arxiv-sanity-lite/blob/master/serve.py
"""


class Analyzer:

    def __init__(self, max_train: int = 5000) -> None:
        self.max_train = max_train
        with open('data/stopwords.txt', 'r') as f:
            self.stopwords = f.read().splitlines()

    def make_corpus(self, training: bool) -> list:
        """Create a corpus of all the articles."""
        all_sources = [
            'data/tvp_articles',
            'data/wp_articles',
        ]
        all_article_paths = []
        for src in all_sources:
            all_article_paths.extend(glob.glob(f'{src}/*.json'))
        print(f'Found {len(all_article_paths)} articles.')
        if training:
            shuffle(all_article_paths)
            all_article_paths = all_article_paths[:self.max_train]

        for article in all_article_paths:
            article = ujson.load(open(article, 'r'))
            # yield ' '.join([article['source'], article['content']])
            yield article['content']

    def create_global_corpus(self,
                             max_df: float = 0.1,
                             min_df: float = 3,
                             num: int = 20000) -> None:
        """Create a global corpus of all the articles."""
        v = TfidfVectorizer(input='content',
                            encoding='utf-8',
                            decode_error='replace',
                            strip_accents='unicode',
                            lowercase=True,
                            analyzer='word',
                            stop_words=self.stopwords,
                            token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b',
                            ngram_range=(1, 2),
                            max_features=num,
                            norm='l2',
                            use_idf=True,
                            smooth_idf=True,
                            sublinear_tf=True,
                            max_df=max_df,
                            min_df=min_df)
        v.fit(self.make_corpus(True))
        X = v.transform(self.make_corpus(False)).astype(np.float32)
        pkl.dump({
            'X': X,
            'vocab': v.vocabulary_,
            'idf': v.idf_
        }, open('data/global_corpus.pkl', 'wb'))

    def construct_sets(self):
        ...

    def load_features(self):
        feats = pkl.load(open('data/global_corpus.pkl', 'rb'))
        X = feats['X']
        y = np.zeros_like(X.shape[0])
        return X, y, feats['vocab'], feats['idf']

    def rank_news(self, C: float = 0.01):
        # classify
        X, y, vocab, idf = self.load_features()

        clf = svm.LinearSVC(class_weight='balanced',
                            verbose=False,
                            max_iter=10000,
                            tol=1e-6,
                            C=C)
        clf.fit(X, y)
        s = clf.decision_function(X)
        sortix = np.argsort(-s)
        scores = [100 * float(s[ix]) for ix in sortix]

        ivocab = {v: k for k, v in vocab.items()}  # index to word mapping
        weights = clf.coef_[0]  # (n_features,) weights of the trained svm
        sortix = np.argsort(-weights)
        words = []
        for ix in list(sortix[:40]) + list(sortix[-20:]):
            words.append({
                'word': ivocab[ix],
                'weight': weights[ix],
            })
        return scores, words


if __name__ == "__main__":
    a = Analyzer()
    a.create_global_corpus()