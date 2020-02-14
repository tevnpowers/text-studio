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

    def execute(self, data):
        """Process and return a single text document."""
        processed_data = data.instances
        for component in self.components:
            if isinstance(component, Transformer):
                processed_data = component.process_batch(processed_data)
            elif isinstance(component, Action):
                component.process_batch(processed_data)
        data.instances = processed_data
