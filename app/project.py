import json
import os
from datetime import datetime
from uuid import UUID, uuid4
from extensions.html_parser import HtmlParser

from text_studio.dataset import Dataset
from text_studio.pipeline import Pipeline

METADATA_KEYS = ["author", "created", "saved"]


def get_current_time():
    return datetime.now().isoformat(timespec="minutes")


class Project(object):
    def __init__(self, *, author="", filepath=""):
        self.filepath = filepath.strip()
        self.metadata = {
            "author": author.strip(),
            "created": get_current_time(),
            "saved": "",
            "data": [],
            "modules": [],
            "pipelines": [],
        }

        self.datasets = {}
        self.modules = {}
        self.pipelines = {}

        if filepath:
            with open(filepath, "r") as f:
                content = json.loads(f.read())
                self.parse_config(content)

        self.load_datasets()

    def __repr__(self):
        description = "Author: {}\nCreated: {}\nSaved: {}\n".format(
            self.metadata["author"],
            self.metadata["created"],
            self.metadata["saved"],
        )
        return description

    @property
    def directory(self):
        if self.filepath:
            return os.path.dirname(self.filepath)
        return ""

    def save(self, filepath):
        self.metadata["saved"] = get_current_time()

    def parse_config(self, config):
        if "metadata" in config:
            for key in METADATA_KEYS:
                if key in config["metadata"]:
                    self.metadata[key] = config["metadata"][key]

        if "data" in config:
            for info in config["data"]:
                self.add_dataset(info)

        if "modules" in config:
            for module in config["modules"]:
                self.add_module(module)

        if "pipelines" in config:
            for info in config["pipelines"]:
                self.add_pipeline(info)

    def add_dataset(self, info):
        id = UUID(info["id"])
        self.datasets[id] = Dataset(id, self._get_absolute_path(info["path"]))

    def add_module(self, module_info):
        if module_info["name"] == "HtmlParser":
            id = UUID(module_info["id"])
            module_info["config"]["id"] = id
            kwargs = module_info["config"]
            module = HtmlParser()
            module.setup(**kwargs)
            self.modules[id] = module

    def add_pipeline(self, info):
        pipeline = Pipeline(UUID(info["id"]), info["name"])
        for id in info["modules"]:
            id = UUID(id)
            pipeline.add_module(self.modules[id])
        self.pipelines[pipeline.id] = pipeline

    def load_datasets(self):
        for fielname, dataset in self.datasets.items():
            dataset.load_data("csv")

    def run(self, id, input_data_id, output_data_path, verbose=False):
        instances = self.datasets[input_data_id].instances[:1000]
        if id in self.modules:
            self._run_module(id, instances, verbose)
        elif id in self.pipelines:
            self._run_pipeline(id, instances, verbose)
        else:
            raise KeyError(
                "The provided ID does not exist in project modules or pipelines."
            )

        if output_data_path:
            absolute_path = self._get_absolute_path(output_data_path)
            matching_id = None
            for id, dataset in self.datasets.items():
                if dataset.file_path == absolute_path:
                    matching_id = id
                    break

            if matching_id:
                dataset = self.datasets[matching_id]
            else:
                dataset = Dataset(uuid4(), absolute_path)
            dataset.instances = instances
            self.datasets[dataset.id] = dataset
            self.datasets[dataset.id].save()

    def _run_module(self, id, data, verbose=False):
        module = self.modules[id]
        if verbose:
            print("Executing module {}...".format(module.name))

        i = 0
        for results in module.process_batch(data):
            assert len(results) == len(module.annotations)
            for j in range(len(results)):
                data[i][module.annotations[j]] = results[j]
            i += 1

        return data

    def _run_pipeline(self, id, data, verbose=False):
        print("Executing pipeline {}...".format(self.pipelines[id].name))
        for id in self.pipelines[id].modules:
            self._run_module(id, data, verbose)

    def _get_absolute_path(self, path):
        return os.path.join(self.directory, path)
