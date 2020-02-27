from sklearn.model_selection import train_test_split as tts


class Dataset(object):
    def __init__(self, id, loader=None, file_path=""):
        self.id = id
        self.loader = loader
        self.file_path = file_path
        self.instances = []
        self.loaded = False

    def load(self, **kwargs):
        if self.loader and self.file_path:
            with open(self.file_path, "r") as file:
                self.instances = self.loader.load(file, **kwargs)

    def save(self, **kwargs):
        if self.loader and self.file_path:
            with open(self.file_path, "w") as file:
                self.loader.save(self.instances, file, **kwargs)

    @staticmethod
    def get_modeling_data(self, text_key, label_key):
        x = [instance[text_key] for instance in self.instances]
        y = [instance[label_key] for instance in self.instances]
        return x, y

    @staticmethod
    def split_data(X, y, test_size, random_state=None):
        return tts(X, y, test_size=test_size, random_state=random_state)
