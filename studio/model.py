import abc


class Model(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.metadata = None

    @abc.abstractmethod
    def setup(self):
        """Initialize all parameter values for the processor's settings."""

    @abc.abstractmethod
    def process_instance(self, doc):
        """Process and return a single text document."""

    @abc.abstractmethod
    def process_batch(self, docs):
        """Process and return an entire dataset of text documents."""
        return [list(self.process_instance(doc)) for doc in docs]

    @abc.abstractmethod
    def encode_labels(self, y):
        return y

    @abc.abstractmethod
    def fit(self, X, y):
        """
        Inner build function that builds a single model.
        """

    @abc.abstractmethod
    def save(self, filepath):
        """
        Serialize and write a model to disk
        """
        raise NotImplementedError("Save function not implemented.")

    @abc.abstractmethod
    def load(self, filepath):
        """
        Load a model from disk and deserialize.
        """
        raise NotImplementedError("Load function not implemented.")
