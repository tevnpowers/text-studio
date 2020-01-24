# https://github.com/huggingface/tokenizers
import string

from tokenizers import BertWordPieceTokenizer
from nltk.corpus import stopwords as sw

# TO DO: Figure out elegant relative path import
import sys

sys.path.append("../../../src")
from utils.timer import timer  # noqa
from modules.processor import BaseProcessor  # noqa


class BertTokenizer(BaseProcessor):
    @timer
    def setup(self, stopwords=None, punct=None, lower=True, strip=True):
        self.tokenizer = BertWordPieceTokenizer(
            "../modules/tokenizers/bert-base-uncased-vocab.txt", lowercase=lower
        )
        self.punct = punct or set(string.punctuation)
        self.stopwords = stopwords or set(sw.words("english"))

    @timer
    def process_batch(self, X):
        return [list(self.process_instance(doc)) for doc in X]

    @timer
    def process_single(self, document):
        return self.process_instance(document)

    def process_instance(self, document):
        tokenized_text = self.tokenizer.encode(document)
        for token in tokenized_text.tokens:
            # If stopword, ignore token and continue
            if token in self.stopwords or token == '[CLS]' or token == '[SEP]':
                continue

            # If punctuation, ignore token and continue
            if all(char in self.punct for char in token):
                continue

            yield token
