import abc


class Annotator(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, *, id, name, keys, annotations):
        """Initialize all parameter values for the processor's settings."""
        self.id = id
        self.name = name
        self.keys = keys
        self.annotations = annotations

    @abc.abstractmethod
    def process_single(self, doc):
        """Process and return a single text document."""

    @abc.abstractmethod
    def process_batch(self, docs):
        """Process and return an entire dataset of text documents."""
        for doc in docs:
            yield self.process_single(doc)
