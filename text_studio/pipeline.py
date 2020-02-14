from collections import OrderedDict


class Pipeline(object):
    def __init__(self, id, name="", modules=None):
        self.id = id
        self.name = name
        self.modules = modules if modules else OrderedDict()

    def add_module(self, module):
        self.modules[module.id] = module

    def remove_module(self, id):
        del self.processors[id]

    def execute(self, data):
        """Process and return a single text document."""
        processed_data = data.instances
        for processor in self.processors:
            processed_data = processor.process_batch(processed_data)
        data.instances = processed_data
