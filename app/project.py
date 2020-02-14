import json
import os
from datetime import datetime
from uuid import UUID, uuid4
from extensions.html_parser import HtmlParser
from extensions.accumulator import Accumulator
from extensions.word_cloud import WordCloudGenerator

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
        self.actions = {}
        self.pipelines = {}

        if filepath:
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    content = json.loads(f.read())
                    self.parse_config(content)
            else:
                raise FileNotFoundError(
                    "The file provided does not exist: {}".format(filepath)
                )

        self.load_datasets()

    def __repr__(self):
        description = "Author: {}\nCreated: {}\nSaved: {}\n".format(
            self.metadata["author"],
            self.metadata["created"],
            self.metadata["saved"],
        )

        # TO DO: Add output info for datasets, modules, actions & pipelines.
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

        if "actions" in config:
            for action in config["actions"]:
                self.add_action(action)

        if "pipelines" in config:
            for info in config["pipelines"]:
                self.add_pipeline(info)

    def add_dataset(self, info):
        id = UUID(info["id"])
        self.datasets[id] = Dataset(id, self._get_absolute_path(info["path"]))

    def add_module(self, info):
        if info["name"] == "HtmlParser":
            module_class = HtmlParser
        elif info["name"] == "Accumulator":
            module_class = Accumulator

        id = UUID(info["id"])
        info["config"]["id"] = id
        kwargs = info["config"]
        module = module_class()
        module.setup(**kwargs)
        self.modules[id] = module

    def add_action(self, info):
        if info["name"] == "WordCloud":
            action_class = WordCloudGenerator

        id = UUID(info["id"])
        info["config"]["id"] = id
        kwargs = info["config"]
        action = action_class()
        action.setup(**kwargs)
        self.actions[id] = action

    def add_pipeline(self, info):
        pipeline = Pipeline(UUID(info["id"]), info["name"])
        for id in info["components"]:
            id = UUID(id)
            if id in self.modules:
                pipeline.add_component(self.modules[id])
            elif id in self.actions:
                pipeline.add_component(self.actions[id])
        self.pipelines[pipeline.id] = pipeline

    def load_datasets(self):
        for fielname, dataset in self.datasets.items():
            dataset.load_data("csv")

    def run(self, id, input_data_id, output_data_path, verbose=False):
        instances = self.datasets[input_data_id].instances[:1000]
        if id in self.modules:
            instances = self._run_module(id, instances, verbose)
        elif id in self.actions:
            self._run_action(id, instances, output_data_path, verbose)
        elif id in self.pipelines:
            instances = self._run_pipeline(
                id, instances, output_data_path, verbose
            )
        else:
            raise KeyError(
                "The provided ID does not exist in project modules or pipelines."
            )

        if output_data_path and id not in self.actions:
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

        output = []
        for result in module.process_batch(data):
            output.append(result)
        return output

    def _run_action(self, id, data, output_path, verbose=False):
        action = self.actions[id]
        if verbose:
            print("Executing action {}...".format(action.name))

        absolute_path = self._get_absolute_path(output_path)
        action.process_batch(data, absolute_path)

    def _run_pipeline(self, id, data, output_path, verbose=False):
        print("Executing pipeline {}...".format(self.pipelines[id].name))
        for id in self.pipelines[id].components:
            if id in self.modules:
                data = self._run_module(id, data, verbose)
            elif id in self.actions:
                self._run_action(id, data, output_path)
        return data

    def _get_absolute_path(self, path):
        return os.path.join(self.directory, path)
