# This module is inspired by the tutorial posted at:
# https://bbengfort.github.io/tutorials/2016/05/19/text-classification-nltk-sckit-learn.html

import pickle

from sklearn.metrics import classification_report as clsr

from context import text_studio

from text_studio.dataset import Dataset
from bert_tokenizer import BertTokenizer
from nltk_tokenizer import NLTKTokenizer
from spacy_tokenizer import SpacyTokenizer
from sklearn_svm import Sklearn_SVM


def build_and_evaluate(X_train, X_test, y_train, y_test, outpath=None, verbose=True):
    # Create tokenizer
    tokenizer = BertTokenizer()
    tokenizer.setup()

    # SVM Classifier
    svm = Sklearn_SVM()
    svm, secs = svm.setup()

    # Begin evaluation
    if verbose:
        print("Building for evaluation")

    # tokenize data
    train_tokenized, secs = tokenizer.process_batch(X_train)
    print("Time to preprocess training data: {}".format(secs))

    svm.fit(train_tokenized, y_train)

    if verbose:
        # print("Evaluation model fit in {:0.3f} seconds".format(secs))
        print("Classification Report:\n")

    test_tokenized, secs = tokenizer.process_batch(X_test)
    print("Time to preprocess test data: {}".format(secs))
    y_pred, secs = svm.process_batch(test_tokenized)
    print(clsr(y_test, y_pred, target_names=set(y)))

    if verbose:
        print("Building complete model and saving ...")

    """
    svm.fit(train_tokenized + test_tokenized, y_train + y_test)
    model.labels_ = labels

    if verbose:
        print("Complete model fit in {:0.3f} seconds".format(secs))
    """

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
