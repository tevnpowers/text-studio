import abc


class Transformer(object):
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
