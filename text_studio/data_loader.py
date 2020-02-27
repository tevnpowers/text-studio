import abc


class DataLoader(object):
    @staticmethod
    @abc.abstractmethod
    def load(file):
        """Load data from the input file into the provided Dataset."""
        raise NotImplementedError("Load not implemented")

    @staticmethod
    @abc.abstractmethod
    def save(dataset, file):
        """Save data from the provided Dataset to the output file."""
        raise NotImplementedError("Save not implemented.")