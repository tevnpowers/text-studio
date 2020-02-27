import sys
import csv
from types import GeneratorType
from text_studio.data_loader import DataLoader

csv.field_size_limit(sys.maxsize)


class CsvLoader(DataLoader):
    @staticmethod
    def load(file, delimiter=","):
        print("loading file!")
        # TO DO: Add basic error checking to validate that the file exists
        instances = []
        reader = csv.DictReader(file, delimiter=delimiter)
        for row in reader:
            instances.append(row)
        return instances

    @staticmethod
    def save(instances, file, delimiter=","):
        print("saving file!")
        if instances:
            print("got some instances!")
            is_generator = isinstance(instances, GeneratorType)
            if is_generator:
                first_instance = next(instances)
            else:
                first_instance = instances[0]

            keys = first_instance.keys()
            writer = csv.DictWriter(file, delimiter=delimiter, fieldnames=keys)

            writer.writeheader()
            if is_generator:
                writer.writerow(first_instance)

            for instance in instances:
                writer.writerow(instance)
        else:
            print("Empty dataset. Skipping file writing.")
