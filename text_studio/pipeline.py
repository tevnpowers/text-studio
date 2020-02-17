from collections import OrderedDict

from text_studio.action import Action
from text_studio.transformer import Transformer


class Pipeline(object):
    def __init__(self, id, name="", components=None):
        self.id = id
        self.name = name
        self.components = components if components else OrderedDict()

    def add_component(self, component):
        self.components[component.id] = component

    def remove_component(self, id):
        del self.components[id]

    def execute(self, data, output_path, verbose=False):
        for id, component in self.components.items():
            if verbose:
                print("Executing component {}...".format(component.name))

            if isinstance(component, Transformer):
                data = component.process_batch(data)
            elif isinstance(component, Action):
                component.process_batch(data, output_path)
        return data
