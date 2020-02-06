# https://github.com/huggingface/tokenizers
import os
import string

from tokenizers import BertWordPieceTokenizer
from nltk.corpus import stopwords as sw

from text_studio.utils.timer import timer
from text_studio.transformer import Transformer

dir_path = os.path.dirname(os.path.realpath(__file__))
VOCAB_FILE = os.path.join(dir_path, "data", "bert-base-uncased-vocab.txt")


class BertTokenizer(Transformer):
    @timer
    def setup(self, stopwords=None, punct=None, lower=True, strip=True):
        self.tokenizer = BertWordPieceTokenizer(VOCAB_FILE, lowercase=lower)
        self.punct = punct or set(string.punctuation)
        self.stopwords = stopwords or set(sw.words("english"))

    def process_single(self, document):
        tokenized_text = self.tokenizer.encode(document)
        for token in tokenized_text.tokens:
            # If stopword, ignore token and continue
            if token in self.stopwords or token == "[CLS]" or token == "[SEP]":
                continue

            # If punctuation, ignore token and continue
            if all(char in self.punct for char in token):
                continue

            yield token
