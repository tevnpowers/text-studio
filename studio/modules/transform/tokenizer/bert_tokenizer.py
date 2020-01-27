# https://github.com/huggingface/tokenizers
import os
import string

from tokenizers import BertWordPieceTokenizer
from nltk.corpus import stopwords as sw
from ....utils.timer import timer
from ..transformer import Transformer

dir_path = os.path.dirname(os.path.realpath(__file__))
VOCAB_FILE = os.path.join(dir_path, "bert-base-uncased-vocab.txt")


class BertTokenizer(Transformer):
    @timer
    def setup(self, stopwords=None, punct=None, lower=True, strip=True):
        self.tokenizer = BertWordPieceTokenizer(VOCAB_FILE, lowercase=lower)
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
            if token in self.stopwords or token == "[CLS]" or token == "[SEP]":
                continue

            # If punctuation, ignore token and continue
            if all(char in self.punct for char in token):
                continue

            yield token
