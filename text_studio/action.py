import abc


class Action(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.metadata = None

    @abc.abstractmethod
    def setup(self, *, id, name, keys):
        """Initialize all parameter values for the processor's settings."""
        self.id = id
        self.name = name
        self.keys = keys

    @abc.abstractmethod
    def process_single(self, doc, out_path):
        """Process a single text document."""

    @abc.abstractmethod
    def process_batch(self, docs, out_path):
        """Process an entire dataset of text documents."""
        for doc in docs:
            self.process_single(doc, out_path)
