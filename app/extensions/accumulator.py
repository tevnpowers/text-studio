from collections import defaultdict
from text_studio.transformer import Transformer


class Accumulator(Transformer):
    def setup(self, *, id, name, keys, annotations):
        self.id = id
        self.name = name
        self.keys = keys
        self.annotations = annotations

    def process_single(self, document):
        return {
            self.annotations[0]: document[self.keys[0]],
            self.annotations[1]: document[self.keys[1]],
        }

    def process_batch(self, documents):
        id_key = self.keys[0]
        text_key = self.keys[1]

        key_to_text = defaultdict(str)
        for document in documents:
            id = document[id_key]
            key_to_text[id] += document[text_key] + "\n"

        output = []
        for k, v in key_to_text.items():
            output.append({self.annotations[0]: k, self.annotations[1]: v})
        return output
