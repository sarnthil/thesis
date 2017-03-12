import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


x_ls, y_ls = [], []
labels = []

with open("classify_cuisine.tsv") as f:
    reader = csv.reader(f, delimiter="\t")
    _, *ings = next(reader)
    for label, *features in reader:
        if label not in labels:
            labels.append(label)
        y_ls.append(labels.index(label))
        x_ls.append([int(f) for f in features])

X = np.array(x_ls)
Y = np.array(y_ls)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.10)

classifiers = [
        DummyClassifier(),
        # KNeighborsClassifier(3),
        # SVC(kernel="linear", C=0.025),
        # SVC(gamma=2, C=1),
        GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
        DecisionTreeClassifier(),
        RandomForestClassifier(),
        MLPClassifier(alpha=1),
        AdaBoostClassifier(),
        GaussianNB(),
        QuadraticDiscriminantAnalysis(),
    ]

for classifier in classifiers:
    cname = repr(classifier).split("(")[0]
    try:
        classifier.fit(x_train, y_train)
        print(cname, classifier.score(x_test, y_test))
    except:
        print(cname, "error")
