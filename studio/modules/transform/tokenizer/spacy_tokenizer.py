import string
import spacy

from ....utils.timer import timer
from ..transformer import Transformer


class SpacyTokenizer(Transformer):
    @timer
    def setup(self, stopwords=None, punct=None, lower=True, strip=True):
        spacy.cli.download("en_core_web_sm")
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "ner"])
        self.lower = lower
        self.punct = punct or set(string.punctuation)

    @timer
    def process_batch(self, X):
        docs = list(self.nlp.pipe(X))
        return [list(self.process_instance(doc)) for doc in docs]

    @timer
    def process_single(self, document):
        return self.process_instance(document)

    def process_instance(self, document):
        return self._process_doc(document)

    def _process_doc(self, doc):
        for token in doc:
            lexeme = self.nlp.vocab[token.text]
            if lexeme.is_stop or (token.text in self.punct):
                continue
            yield token.lemma_
