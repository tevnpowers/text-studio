from text_studio.annotator import Annotator
from nltk import word_tokenize, pos_tag, data


class PosTagger(Annotator):
    def setup(self, *, id, name, keys, filters, annotations):
        self.id = id
        self.name = name
        self.keys = keys
        self.annotations = annotations
        self.filters = set(filters)
        self.sent_detector = data.load("tokenizers/punkt/english.pickle")

    def process_single(self, document):
        text = document[self.keys[0]][:200]
        sentences = self.sent_detector.tokenize(text.strip())
        tagged_tokens = []
        raw_tokens = []
        for sentence in sentences:
            tokens = word_tokenize(sentence)
            tokens = pos_tag(tokens)

            if self.filters:
                for token, tag in tokens:
                    if tag in self.filters:
                        tagged_tokens.append((token, tag))
                        raw_tokens.append(token)
            else:
                tagged_tokens += tokens
                raw_tokens += [x for (x, y) in tokens]

        document[self.annotations[0]] = tagged_tokens
        document[self.annotations[1]] = " ".join(raw_tokens)
        return document
