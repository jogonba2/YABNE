""" Add here your classifiers (scikit-learn convention) """

from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

class Classifiers:

    # Solo funciona con el dominio de ejemplo hasta que se parametrice (4 neuronas en la capa de salida) #
    @staticmethod
    def mlp_nn_classifier(X, Y):
        clf = MLPClassifier(solver="lbfgs", alpha=1e-5,
                            hidden_layer_sizes=(128, 4), random_state=1)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def gaussian_nb(X, Y):
        clf = GaussianNB()
        clf.fit(X, Y)
        return clf

    @staticmethod
    def svm(X, Y, kernel="linear"):
        clf = svm.SVC(kernel=kernel)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def ada_boost(X, Y, n_estimators=50):
        clf = AdaBoostClassifier(n_estimators=n_estimators)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def random_forest(X, Y, n_stimators=10):
        clf = RandomForestClassifier(n_estimators=n_estimators)
        clf.fit(X, Y)
        return clf

    @staticmethod
    def decision_tree(X, Y):
        clf = DecisionTreeClassifier()
        clf.fit(X, Y)
        return clf

    @staticmethod
    def bernoulli_nb(X, Y):
        clf = BernoulliNB()
        clf.fit(X, Y)
        return clf

    @staticmethod
    def multinomial_nb(X, Y):
        clf = MultinomialNB()
        clf.fit(X, Y)
        return clf

    @staticmethod
    def nearest_centroid(X, Y, k=1):
        clf = NearestCentroid()
        clf.fit(X, Y)
        return clf

    @staticmethod
    def k_nearest_neighbors(X, Y, k=1):
        clf = KNeighborsClassifier(n_neighbors=k)
        clf.fit(X, Y)
        return clf