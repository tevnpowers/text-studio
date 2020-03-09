"""Extract insight from textual data.

An Action consumes textual data either individually or in bulk
in order to produce an artifact, while not modifying or
augmenting the input data instance(s).

An artifact may be a visualization, a summary report, or any
other insights that can be extracted from the provided data.
"""
import abc


class Action(object):
    """Extract insight from textual data.

    An Action consumes textual data either individually or in bulk
    in order to produce an artifact, while not modifying or
    augmenting the input data instance(s).

    An artifact may be a visualization, a summary report, or any
    other insights that can be extracted from the provided data.

    Parameters
    -------
    id : uuid
        Unique identifier for an action in a TextStudio project.
    name : string
        Name of the action in a TextStudio project.
    keys : collection of strings
        List of keys to extract values from the input
        data instance for execution.

    Methods
    -------
    process_single(self, doc):
        Produce insight from an individual data instance.
    process_batch(self, docs):
        Produce insight from a collection of data instances.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, *, id, name, keys):
        self.id = id
        self.name = name
        self.keys = keys

    @abc.abstractmethod
    def process_single(self, doc, out_path):
        """Produce insight from an individual data instance.

        Parameters
        ----------
        doc : dict
            A single data instance.
        out_path : string
            External location where generated artifact(s) should be stored.

        Returns
        -------
        success : bool
            A modified version of the input doc, with new annotations
            from the Annotator.
        """

    @abc.abstractmethod
    def process_batch(self, docs, out_path):
        """Produce insight from a collection of data instances.

        Parameters
        ----------
        docs : list of dicts
            A single data instance.
        out_path : string
            External location where generated artifact(s) should be stored.

        Returns
        -------
        success : bool
            A modified version of the input doc, with new annotations
            from the Annotator.
        """
        for doc in docs:
            self.process_single(doc, out_path)
