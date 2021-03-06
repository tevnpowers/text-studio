# This module is inspired by the tutorial posted at:
# https://bbengfort.github.io/tutorials/2016/05/19/text-classification-nltk-sckit-learn.html

import pickle

from sklearn.metrics import classification_report as clsr

from context import text_studio

from text_studio.dataset import Dataset
from tokenizer_bert import BertTokenizer
from tokenizer_nltk import NLTKTokenizer
from tokenizer_spacy import SpacyTokenizer
from sklearn_svm import Sklearn_SVM


def build_and_evaluate(X_train, X_test, y_train, y_test, outpath=None):
    # Create tokenizer
    tokenizer = BertTokenizer()
    tokenizer.setup()

    # SVM Classifier
    svm = Sklearn_SVM()
    svm = svm.setup()

    train_tokenized = tokenizer.process_batch(X_train)

    print("Training model......")
    svm.fit(train_tokenized, y_train)

    print("Predicting test data...")
    test_tokenized = tokenizer.process_batch(X_test)
    y_pred = svm.process_batch(test_tokenized)

    print("Classification Report:\n")
    print(clsr(y_test, y_pred, target_names=set(y)))

    if outpath:
        with open(outpath, "wb") as f:
            pickle.dump(model, f)

        print("Model written out to {}".format(outpath))

    return svm


if __name__ == "__main__":
    dataset = Dataset("./data/movie_reviews.tsv")
    dataset.load_data("tsv")
    X, y = dataset.get_modeling_data("text", "sentiment")
    X_train, X_test, y_train, y_test = Dataset.split_data(X, y, 0.2, 1)
    model = build_and_evaluate(X_train, X_test, y_train, y_test, outpath=None)
