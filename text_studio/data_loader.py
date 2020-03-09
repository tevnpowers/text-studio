"""Load and save data set instances.

A Data Loader is responsible for loading data that exists
outside of a text_studio.Dataset object, into a text_studio.Dataset.
It must also provide the inverse functionality, to write the data
instances from a text_studio.Dataset object to an external location.
"""
import abc


class DataLoader(object):
    """Load and save data set instances.

    A Data Loader is responsible for loading data that exists
    outside of a text_studio.Dataset object, into a text_studio.Dataset.
    It must also provide the inverse functionality, to write the data
    instances from a text_studio.Dataset object to an external location.

    Methods
    -------
    load(file):
        Load data instances at the input file path.
    save(dataset, file):
        Write data instances to the provided file location.
    """

    @staticmethod
    @abc.abstractmethod
    def load(file):
        """Load data instances at the input file path.

        Parameters
        ----------
        file : string
            The path to a file or directory from which a
            collection of data set instances should be loaded.

        Returns
        -------
        instances : list of dictionaries
            A collection of data instances, each of which is a dictionary.
        """
        raise NotImplementedError("Load not implemented")

    @staticmethod
    @abc.abstractmethod
    def save(dataset, file):
        """Write data instances to the provided file location.

        Parameters
        ----------
        dataset: text_studio.Dataset
            A text_studio Dataset object which contains the data
            instances to be saved.
        file : string
            The path to a file or directory to which the
            collection of data set instances should be written.

        Returns
        -------
        saved : bool
            Value that is True if a data set is successfully saved
            and False if the save failed for any reason.
        """
        raise NotImplementedError("Save not implemented.")
