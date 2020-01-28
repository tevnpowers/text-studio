from collections import OrderedDict


class Pipeline(object):
    def __init__(self, processors=None):
        self.processors = processors if processors else OrderedDict()

    def add_processor(self, name, processor):
        self.processors[name] = processor

    def remove_processor(self, name):
        del self.processors[name]

    def execute(self, data):
        """Process and return a single text document."""
        processed_data = data.instances
        for processor in self.processors:
            processed_data = processor.process_batch(processed_data)
        data.instances = processed_data
