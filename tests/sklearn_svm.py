# This module is inspired by the tutorial posted at:
# https://bbengfort.github.io/tutorials/2016/05/19/text-classification-nltk-sckit-learn.html

import pickle

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report as clsr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split as tts

from studio.utils.timer import timer
from studio.transformer import Transformer  # noqa


class Sklearn_SVM(Transformer):
    @timer
    def setup(self):
        """Initialize all parameter values for the processor's settings."""
        return self

    @timer
    def fit(self, X, y):
        """
        Inner build function that builds a single model.
        """
        model = Pipeline(
            [
                (
                    "vectorizer",
                    TfidfVectorizer(
                        tokenizer=self._identity, preprocessor=None, lowercase=False
                    ),
                ),
                ("classifier", SGDClassifier()),
            ]
        )

        model.fit(X, y)
        self.model = model
        return self.model

    @timer
    def process_instance(self, doc):
        """Process and return a single text document."""
        return self.process_batch([doc])[0]

    @timer
    def process_batch(self, docs):
        """Process and return an entire dataset of text documents."""
        if self.model:
            return self.model.predict(docs)
        else:
            print("Model hasn't been trained...")

    def _identity(self, text):
        return text

    @timer
    def encode_labels(self, y):
        # Label encode the targets
        self.labels = LabelEncoder()
        return self.labels.fit_transform(y)
