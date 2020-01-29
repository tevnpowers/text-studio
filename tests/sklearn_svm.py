import pickle

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

from studio.utils.timer import timer
from studio.model import Model


class Sklearn_SVM(Model):
    @timer
    def setup(self, tokenizer=None, lowercase=False):
        """Initialize all parameter values for the processor's settings."""
        self.tokenizer = tokenizer if tokenizer else self._identity
        self.lowercase = lowercase
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
                        tokenizer=self.tokenizer, lowercase=self.lowercase
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
