from html.parser import HTMLParser

from text_studio.transformer import Transformer


class TextStudioHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = ""
        self.new_line_tags = set(["p", "br", "title"])

    def handle_starttag(self, tag, attrs):
        if tag in self.new_line_tags or tag.startswith("h"):
            self.content += "\n"

    def handle_data(self, data):
        self.content += data


class HtmlParser(Transformer):
    def setup(self, *, id, name, keys, annotations):
        self.id = id
        self.name = name
        self.keys = keys
        self.annotations = annotations
        self.parser = TextStudioHTMLParser()

    def clear(self):
        self.parser.reset()
        self.parser.content = ""

    def process_single(self, document):
        self.clear()
        self.parser.feed(self.document_text(document))
        return (self.parser.content,)

    def document_text(self, document):
        return document[self.keys[0]] if self.keys else document
