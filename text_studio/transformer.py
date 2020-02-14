import abc


class Transformer(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.metadata = None

    @abc.abstractmethod
    def setup(self, *, id, name, key, annotation):
        """Initialize all parameter values for the processor's settings."""
        self.id = id
        self.name = name
        self.key = key
        self.annotation = annotation

    @abc.abstractmethod
    def process_single(self, doc):
        """Process and return a single text document."""

    @abc.abstractmethod
    def process_batch(self, docs):
        """Process and return an entire dataset of text documents."""
        for doc in docs:
            yield self.process_single(doc)
