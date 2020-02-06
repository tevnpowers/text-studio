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
    def setup(self, key=""):
        self.parser = TextStudioHTMLParser()
        self.key = key

    def process_single(self, document):
        self.parser.reset()
        self.parser.feed(self.document_text(document)[:1000])
        return self.parser.content

    def document_text(self, document):
        return document[self.key] if self.key else document
