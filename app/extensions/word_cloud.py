import os

from os import path
from wordcloud import WordCloud
from text_studio.action import Action


class WordCloudGenerator(Action):
    def process_single(self, doc, out_path):
        """Process a single text document."""
        id_key = self.keys[0]
        text_key = self.keys[1]

        text = doc[text_key]
        wordcloud = WordCloud().generate(text)

        file_name = path.join(path.dirname(out_path), "{}.png".format(doc[id_key]))
        wordcloud.to_file(file_name)

    def process_batch(self, docs, out_path):
        """Process an entire dataset of text documents."""
        for doc in docs:
            self.process_single(doc, out_path)
