import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import text_studio  # noqa
from text_studio.dataset import Dataset

METADATA_KEYS = ["author", "created", "saved"]


class Project(object):
    def __init__(self, filepath=""):
        self.filepath = filepath
        self.metadata = {
            "author": "",
            "created": get_current_time(),
            "saved": "",
            "data": [],
            "modules": [],
            "pipelines": [],
        }

        self.datasets = []
        self.modules = []
        self.pipelines = []

        if filepath:
            with open(filepath, "r") as f:
                content = json.loads(f.read())
                self.parse_config(content)

        print(self.metadata)
        self.load_datasets()
        print(self.datasets)
        print(self.datasets[0].loaded)

    @property
    def directory(self):
        if self.filepath:
            return os.path.dirname(self.filepath)
        return ''

    def save(self, filepath):
        self.metadata["saved"] = get_current_time()

    def parse_config(self, config):
        if "metadata" in config:
            for key in METADATA_KEYS:
                if key in config["metadata"]:
                    self.metadata[key] = config["metadata"][key]

        if "data" in config:
            for path in config["data"]:
                self.add_dataset(path)

        if "modules" in config:
            for module in config["modules"]:
                self.add_module(module)

        if "pipelines" in config:
            for pipeline in config["pipelines"]:
                self.add_pipeline(pipeline)

    def add_dataset(self, filepath):
        self.datasets.append(Dataset(os.path.join(self.directory, filepath)))

    def add_module(self, module):
        pass

    def add_pipeline(self, pipeline):
        pass

    def load_datasets(self):
        for dataset in self.datasets:
            dataset.load_data('csv')

def get_current_time():
    return datetime.now().isoformat(timespec="minutes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some text.")
    parser.add_argument(
        "project",
        metavar="p",
        type=str,
        nargs=1,
        help="a text studio project file (json)",
    )

    args = parser.parse_args()
    project = Project(args.project[0])
