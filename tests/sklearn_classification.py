import numpy as np
from sklearn import metrics
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB

categories = ["alt.atheism", "soc.religion.christian", "comp.graphics", "sci.med"]


# EXTRACT
# This dataset is an sklearn Bunch object.
# Bunch.data is a list of data instances, each of which is a string.
print("Loading training data...")
twenty_train = fetch_20newsgroups(
    subset="train", categories=categories, shuffle=True, random_state=42
)

print("Loading test data...")
twenty_test = fetch_20newsgroups(
    subset="test", categories=categories, shuffle=True, random_state=42
)

# TRANSFORM
# Featurization
# Count tokens
print("Featurizing training data...")
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)


# Tf-idf transformation
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# Classification
# Train
print("Training classifier...")
# clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)
parameters = {"alpha": (1e-2, 1e-3)}
clf = SGDClassifier(
    loss="hinge", penalty="l2", alpha=1e-3, random_state=42, max_iter=5, tol=None
).fit(X_train_tfidf, twenty_train.target)

# Predict
print("Featurizing test data...")
X_new_counts = count_vect.transform(twenty_test.data)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

print("Predicting test data...")
predicted = clf.predict(X_new_tfidf)

# Evaluate
print(
    metrics.classification_report(
        twenty_test.target, predicted, target_names=twenty_test.target_names
    )
)
