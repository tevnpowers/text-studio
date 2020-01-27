# This module is inspired by the tutorial posted at:
# https://bbengfort.github.io/tutorials/2016/05/19/text-classification-nltk-sckit-learn.html

import string

import nltk
from nltk.corpus import stopwords as sw
from nltk.corpus import wordnet as wn
from nltk import wordpunct_tokenize
from nltk import WordNetLemmatizer
from nltk import sent_tokenize
from nltk import pos_tag

from ....utils.timer import timer
from ..transformer import Transformer


class NLTKTokenizer(Transformer):
    @timer
    def setup(self, stopwords=None, punct=None, lower=True, strip=True):
        nltk.download("averaged_perceptron_tagger")
        nltk.download("punkt")
        nltk.download("wordnet")
        self.lower = lower
        self.strip = strip
        self.stopwords = stopwords or set(sw.words("english"))
        self.punct = punct or set(string.punctuation)
        # self.lemmatizer = WordNetLemmatizer()

    @timer
    def process_batch(self, X):
        return [list(self.process_instance(doc)) for doc in X]

    @timer
    def process_single(self, document):
        return self.process_instance(document)

    def process_instance(self, document):
        # Break the document into sentences
        for sent in sent_tokenize(document):
            # Break the sentence into part of speech tagged tokens
            # for token, tag in pos_tag(wordpunct_tokenize(sent)):
            for token in wordpunct_tokenize(sent):
                # Apply preprocessing to the token
                token = token.lower() if self.lower else token
                token = token.strip() if self.strip else token
                token = token.strip("_") if self.strip else token
                token = token.strip("*") if self.strip else token

                # If stopword, ignore token and continue
                if token in self.stopwords:
                    continue

                # If punctuation, ignore token and continue
                if all(char in self.punct for char in token):
                    continue

                yield token
                """
                # Lemmatize the token and yield
                lemma = self.lemmatize(token, tag)
                yield lemma
                """

    def lemmatize(self, token, tag):
        tag = {"N": wn.NOUN, "V": wn.VERB, "R": wn.ADV, "J": wn.ADJ}.get(
            tag[0], wn.NOUN
        )

        return self.lemmatizer.lemmatize(token, tag)
