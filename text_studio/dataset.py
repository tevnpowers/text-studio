import csv
import sys
from sklearn.model_selection import train_test_split as tts

csv.field_size_limit(sys.maxsize)


class Dataset(object):
    def __init__(self, id, file_path=""):
        self.id = id
        self.file_path = file_path
        self.instances = []
        self.loaded = False

    def get_modeling_data(self, text_key, label_key):
        x = [instance[text_key] for instance in self.instances]
        y = [instance[label_key] for instance in self.instances]
        return x, y

    @staticmethod
    def split_data(X, y, test_size, random_state=None):
        return tts(X, y, test_size=test_size, random_state=random_state)

    def load_data(self, format, text_key=None, label_key=None):
        # TO DO: Add basic error checking to validate that the file exists
        delimiter = self.get_delimiter(format)
        if not delimiter:
            # TO DO: throw exception
            return

        if self.file_path:
            instances = []
            with open(self.file_path, "r") as csvfile:
                reader = csv.DictReader(csvfile, delimiter=delimiter)
                for row in reader:
                    instances.append(row)
            self.instances = instances
            self.loaded = True

    def write_data(self, file_path, format):
        delimiter = self.get_delimiter(format)
        if not delimiter:
            # TO DO: throw exception
            return

        if self.instances:
            keys = self.instances[0].keys()
            with open(file_path, "w") as outputfile:
                writer = csv.DictWriter(
                    outputfile, delimiter=delimiter, fieldnames=keys
                )

                writer.writeheader()
                for instance in self.instances:
                    writer.writerow(instance)

    def save(self):
        print("Saving dataset {}...".format(self.file_path))
        self.write_data(self.file_path, "csv")

    def get_delimiter(self, format):
        if format == "csv":
            return ","
        elif format == "tsv":
            return "\t"
        else:
            # TO DO: raise exception
            return ""
