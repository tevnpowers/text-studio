"""Provide annotation on textual data.

An Annotator runs a process which augments the provided input data.
Given a data instance object (Python dictionary), an annotator will
add a new key value pair to the dictionary.
(e.g. tokenization output, part of speech tags, etc.).
"""
import abc


class Annotator(object):
    """Provide annotation on textual data.

    An Annotator runs a process which augments the provided input data.
    Given a data instance object (Python dictionary), an annotator will
    add a new key value pair to the dictionary.
    (e.g. tokenization output, part of speech tags, etc.).

    Parameters
    -------
    id : uuid
        Unique identifier for an annotator in a TextStudio project.
    name : string
        Name of the annotator in a TextStudio project.
    keys : collection of strings
        List of keys to extract values from the input
        data instance for execution.
    annotations : collection of strings
        List of keys required to add Annotator annotations on the
        input data instance during execution.

    Methods
    -------
    process_single(self, doc):
        Provide new annotations for an individual data instance.
    process_batch(self, docs):
        Provide new annotations for each data instance in a collection.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, *, id, name, keys, annotations):
        self.id = id
        self.name = name
        self.keys = keys
        self.annotations = annotations

    @abc.abstractmethod
    def process_single(self, doc):
        """Provide new annotations for an individual data instance.

        Parameters
        ----------
        doc : dict
            A single data instance.

        Returns
        -------
        doc : dict
            A modified version of the input doc, with new annotations
            from the Annotator.
        """

    @abc.abstractmethod
    def process_batch(self, docs):
        """Provide new annotations for each data instance in a collection.

        Parameters
        ----------
        docs : list of dicts
            A collection of data instances.

        Returns
        -------
        docs : list of dicts
            A modified collection of the input docs, where each object in
            the collection contains new annotations from the Annotator.
        """
        for doc in docs:
            yield self.process_single(doc)
