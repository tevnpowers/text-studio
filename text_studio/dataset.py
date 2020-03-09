"""Data set for text records.

A Dataset maintains the collection of data instances and metadata
associated with the dataset.
"""


class Dataset(object):
    """Data set for text records.

    A Dataset maintains the collection of data instances and metadata
    associated with the dataset.

    Parameters
    -------
    id : uuid
        Unique identifier for a dataset in a TextStudio project.
    loader : text_studio.DataLoader
        The DataLoader object responsible for loading the data
        from an external source and/or writing the data set to an
        external location.
    file_path : string
        The file path points to the location of the data set.

    Attributes
    -------
    instances : list of dicts
        Collection of data instances contained in the dataset.
    loaded : bool
        True if all data instances in the dataset have been loaded
        into the dataset. Data instances are not loaded from disk
        or an external location until needed.

    Methods
    -------
    load(self, **kwargs):
        Load the dataset using the Dataset's loader.
    save(self, **kwargs):
        Save the dataset using the Dataset's loader.
    """

    def __init__(self, id, loader=None, file_path=""):
        self.id = id
        self.loader = loader
        self.file_path = file_path
        self.instances = []
        self.loaded = False

    def load(self, **kwargs):
        """Load the dataset using the Dataset's loader.

        Load the data set from its stored location,
        populating the data instances collection. Set the
        loaded flag to True if the instances were retrieved
        successfully.

        Parameters
        ----------
        **kwargs : dictionary
            Keyword arguments passed to the DataLoader
            to configure its settings for loading the dataset.
        """
        if self.loader and self.file_path:
            with open(self.file_path, "r") as file:
                self.instances = self.loader.load(file, **kwargs)
                self.loaded = True

    def save(self, **kwargs):
        """Save the dataset using the Dataset's loader.

        Save the data set in its current state to a storage location.

        Parameters
        ----------
        **kwargs : dictionary
            Keyword arguments passed to the DataLoader
            to configure its settings for writing the dataset.
        """
        if self.loader and self.file_path:
            with open(self.file_path, "w") as file:
                self.loader.save(self.instances, file, **kwargs)
