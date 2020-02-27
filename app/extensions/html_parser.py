from html.parser import HTMLParser

from text_studio.annotator import Annotator


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


class HtmlParser(Annotator):
    def __init__(self, *, id, name, keys, annotations):
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
        self.parser.feed(self.get_document_html(document))
        document["text"] = self.parser.content
        return document

    def get_document_html(self, document):
        return document[self.keys[0]] if self.keys else document
