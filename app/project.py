import json
import os
from datetime import datetime
from uuid import UUID, uuid4
from extensions.html_parser import HtmlParser
from extensions.accumulator import Accumulator
from extensions.word_cloud import WordCloudGenerator
from extensions.pos_tagger import PosTagger
from extensions.csv_loader import CsvLoader
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
            "annotators": [],
            "pipelines": [],
        }

        self.datasets = {}
        self.data_loaders = {}
        self.annotators = {}
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

    def get_project_component_descriptions(self, heading, collection):
        description = "\n{}:\n----------\n".format(heading)
        for id, component in collection.items():
            description += "{}\t\t{}\n".format(component.name, id)
        return description

    def __repr__(self):
        description = "Author: {}\nCreated: {}\nSaved: {}\n".format(
            self.metadata["author"],
            self.metadata["created"],
            self.metadata["saved"],
        )

        if self.data_loaders:
            description += "\nData Loaders:\n----------\n"
            for id, loader in self.data_loaders.items():
                description += "{}\t\t{}\n".format(loader["name"], id)

        if self.datasets:
            description += "\nDatasets:\n----------\n"
            for id, dataset in self.datasets.items():
                description += "{}\t\t{}\n".format(dataset.file_path, id)

        if self.annotators:
            description += self.get_project_component_descriptions(
                "Annotators", self.annotators
            )

        if self.actions:
            description += self.get_project_component_descriptions(
                "Actions", self.actions
            )

        if self.pipelines:
            description += self.get_project_component_descriptions(
                "Pipelines", self.pipelines
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

        if "loaders" in config:
            for info in config["loaders"]:
                self.add_data_loader(info)

        if "data" in config:
            for info in config["data"]:
                self.add_dataset(info)

        if "annotators" in config:
            for annotator in config["annotators"]:
                self.add_annotator(annotator)

        if "actions" in config:
            for action in config["actions"]:
                self.add_action(action)

        if "pipelines" in config:
            for info in config["pipelines"]:
                self.add_pipeline(info)

    def add_data_loader(self, info):
        if info["name"] == "CsvLoader":
            loader_class = CsvLoader
        else:
            raise ValueError(
                "Could not find a Dataset Loader named {}".format(info["name"])
            )
        id = UUID(info["id"])
        self.data_loaders[id] = {
            "name": info["name"],
            "loader": loader_class,
            "kwargs": info["config"],
        }

    def add_dataset(self, info):
        id = UUID(info["id"])
        loader = None
        if info["config"]["loader_id"]:
            loader_id = UUID(info["config"]["loader_id"])
            if loader_id in self.data_loaders:
                loader = self.data_loaders[loader_id]["loader"]
            else:
                raise ValueError(
                    "Could not find a Dataset Loader with ID {}".format(
                        loader_id
                    )
                )
        self.datasets[id] = Dataset(
            id, loader=loader, file_path=self._get_absolute_path(info["path"])
        )

    def add_annotator(self, info):
        if info["name"] == "HtmlParser":
            annotator_class = HtmlParser
        elif info["name"] == "Accumulator":
            annotator_class = Accumulator
        elif info["name"] == "PosTagger":
            annotator_class = PosTagger
        else:
            raise ValueError(
                "Could not find a annotator named {}".format(info["name"])
            )

        id = UUID(info["id"])
        info["config"]["id"] = id
        kwargs = info["config"]
        annotator = annotator_class(**kwargs)
        self.annotators[id] = annotator

    def add_action(self, info):
        if info["name"] == "WordCloud":
            action_class = WordCloudGenerator
        else:
            raise ValueError(
                "Could not find an Action named {}".format(info["name"])
            )

        id = UUID(info["id"])
        info["config"]["id"] = id
        kwargs = info["config"]
        action = action_class(**kwargs)
        self.actions[id] = action

    def add_pipeline(self, info):
        pipeline = Pipeline(UUID(info["id"]), info["name"])
        for id in info["components"]:
            id = UUID(id)
            if id in self.annotators:
                pipeline.add_component(self.annotators[id])
            elif id in self.actions:
                pipeline.add_component(self.actions[id])
        self.pipelines[pipeline.id] = pipeline

    def load_datasets(self):
        for filename, dataset in self.datasets.items():
            dataset.load()

    def run(self, id, input_data_id, output_data_path, verbose=False):
        instances = self.datasets[input_data_id].instances
        if id in self.annotators:
            instances = self._run_annotator(id, instances, verbose)
        elif id in self.actions:
            self._run_action(id, instances, output_data_path, verbose)
        elif id in self.pipelines:
            instances = self._run_pipeline(
                id, instances, output_data_path, verbose
            )
        else:
            raise KeyError(
                "The provided ID does not exist in project annotators, actions, or pipelines."
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
                dataset = Dataset(uuid4(), CsvLoader, absolute_path)
            dataset.instances = instances
            self.datasets[dataset.id] = dataset
            self.datasets[dataset.id].save()

    def _run_annotator(self, id, data, verbose=False):
        annotator = self.annotators[id]
        if verbose:
            print("Executing annotator {}...".format(annotator.name))

        return annotator.process_batch(data)

    def _run_action(self, id, data, output_path, verbose=False):
        action = self.actions[id]
        if verbose:
            print("Executing action {}...".format(action.name))

        absolute_path = self._get_absolute_path(output_path)
        action.process_batch(data, absolute_path)

    def _run_pipeline(self, id, data, output_path, verbose=False):
        print("Executing pipeline {}...".format(self.pipelines[id].name))
        return self.pipelines[id].execute(
            data, self._get_absolute_path(output_path), verbose
        )

    def _get_absolute_path(self, path):
        return os.path.join(self.directory, path)
