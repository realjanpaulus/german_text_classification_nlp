#classifier
from sklearn.linear_model import LogisticRegression, SGDClassifier, LogisticRegressionCV, LinearRegression
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

#classifier tools
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import f1_score, classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesClassifier

#others
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

### helper functions ###

def save_classification_report(classifier_name, y_test, y_pred, labels):
    """Saves the classification report (precision, recall, f1-score) as csv-file.
    
    Args:
        classifier_name (string): Name of the classification method.
        y_test (numpy.ndarray): Original labels of the test set as ndarray.
        y_pred (numpy.ndarray): Predicted labels of the test set as ndarray.
        labels (list): List of the labels represented as strings.
    """
    report = classification_report(y_test, y_pred, target_names=labels, output_dict=True)
    df = pd.DataFrame(report)
    df.T.to_csv(f"data/classifier/classification_reports/{classifier_name}-report.csv")


def save_confusion_matrix(classifier_name, y_test, y_pred, labels):
    """Plots and saves the confusion matrix of the original and predicted labels 
        as svg- and csv-file.
    
    Args:
        classifier_name (string): Name of the classification method.
        y_test (numpy.ndarray): Original labels of the test set as ndarray.
        y_pred (numpy.ndarray): Predicted labels of the test set as ndarray.
        labels (list): List of the labels represented as strings.
    """
        
    cm = confusion_matrix(y_test, y_pred)
    df = pd.DataFrame(cm, index=labels, columns=labels)
    
    plt.figure(figsize=(10, 9))
    sns.heatmap(df, annot=True, cmap=sns.color_palette("Blues"))
    plt.tight_layout()
    
    plt.savefig(f"data/classifier/confusion_matrices/{classifier_name}_cm.svg")
    df.to_csv(f"data/classifier/confusion_matrices/{classifier_name}_cm.csv")


def save_cross_validation(classifier_name, cross_val):
    """Saves the cross-validation of the classification method to a svg- and csv-file.
    
    Args:
        classifier_name (string): Name of the classification method.
        cross_val (numpy.ndarray): Ndarray of the scores.
    """
    cross_val_df = pd.DataFrame(cross_val, columns=[f"{classifier_name}"])
    cross_val_df.to_csv(f"data/classifier/cross_validation/{classifier_name}_cross_val.csv", index=False)
    
    # boxplotting
    plt.figure()
    ax = cross_val_df.plot.box(vert=False, color="black")
    ax.set_ylabel("Category")
    ax.set_xlabel("Accuracy")
    plt.tight_layout()
    
    plt.savefig(f"data/classifier/cross_validation/{classifier_name}_accuracies.svg")


def save_f1_scores(classifier_name, y_pred, y_test):
    """Saves the different f1 scores of the classification method to a csv-file.
    
    Args:
        classifier_name (string): Name of the classification method.
        y_test (numpy.ndarray): Original labels of the test set as ndarray.
        y_pred (numpy.ndarray): Predicted labels of the test set as ndarray.
    """
    scores = {f"{classifier_name}":{"micro": np.around(f1_score(y_pred, y_test, average="micro"), decimals=3),
                                    "macro": np.around(f1_score(y_pred, y_test, average="macro"), decimals=3),
                                    "weighted": np.around(f1_score(y_pred, y_test, average="weighted"), decimals=3)}}
    scores_df = pd.DataFrame(scores)
    scores_df = scores_df.T
    scores_df.to_csv(f"data/classifier/f1_scores/{classifier_name}_f1.csv")
    
def saving_results(classifier, classifier_name, y_test, y_pred, classes, vec, Y, cv):
    """
    Args:
        classifier (classifier object): Object of the respective classifier.
        classifier_name (string): Name of the classification method.
        y_test (numpy.ndarray): Original labels of the test set as ndarray.
        y_pred (numpy.ndarray): Predicted labels of the test set as ndarray.
        classes (list): List of unique class names as strings.
        vec (csr matrix): Vectorizer of the text column of the df.
        Y (numpy array): Array which represents the categories of the category column of the df.
        cv (int): Number of the cross validation test sets. 
    """
    #save classification report
    save_classification_report(classifier_name, y_test, y_pred, classes)
    
    #save confusion matrix
    save_confusion_matrix(classifier_name, y_test, y_pred, classes)
    
    #save cross validation
    cross_val = cross_val_score(classifier, vec, Y, cv=cv)
    save_cross_validation(classifier_name, cross_val)
    
    #save f1 scores
    save_f1_scores(classifier_name, y_pred, y_test)

#############################
### classifier functions ###
############################
    
#################################
# 1. Probabilistic classifiers #
################################

#####
# 1.1. The Bayes classifier
#####
    
def complement_naive_bayes(train_test, classes, vec, Y, return_pred=True, cv=10, alpha=0.01):
    """Computes the Complement Naive Bayes classifier and optionally the predicted class labels for X_test.
    
    Args:
        train_test (tuple): Tuple with the trainings- and test-data in the following order: X_train, X_test, y_train, y_test.
        classes (list): List of unique class names as strings.
        vec (csr matrix): Vectorizer of the text column of the df.
        Y (numpy array): Array which represents the categories of the category column of the df.
        return_pred (bool): If True, the y_prediction will be returned.
        cv (int): Number of the cross validation test sets. 
        alpha (float): Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).
    Returns:
        Complement Naive Bayes classifier and optionally the predicted class labels for X_test.
    """
    classifier_name = "complement-naive-bayes"
    X_train = train_test[0]
    X_test = train_test[1]
    y_train = train_test[2]
    y_test = train_test[3]
    
    clf = ComplementNB(alpha=0.01)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    #saving results
    saving_results(clf, classifier_name, y_test, y_pred, classes, vec, Y, cv)
    
    if return_pred:
        return clf, y_pred
    else:
        return clf

def multinomial_naive_bayes(train_test, classes, vec, Y, return_pred=True, cv=10, alpha=0.01):
    """Computes the Multinomial Naive Bayes classifier and optionally the predicted class labels for X_test.
    
    Args:
        train_test (tuple): Tuple with the trainings- and test-data in the following order: X_train, X_test, y_train, y_test.
        classes (list): List of unique class names as strings.
        vec (csr matrix): Vectorizer of the text column of the df.
        Y (numpy array): Array which represents the categories of the category column of the df.
        return_pred (bool): If True, the y_prediction will be returned.
        cv (int): Number of the cross validation test sets. 
        alpha (float): Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).
    Returns:
        Multinomial Naive Bayes classifier and optionally the predicted class labels for X_test.
    """
    classifier_name = "multinomial-naive-bayes"
    X_train = train_test[0]
    X_test = train_test[1]
    y_train = train_test[2]
    y_test = train_test[3]
    
    clf = MultinomialNB(alpha=0.01)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    #saving results
    saving_results(clf, classifier_name, y_test, y_pred, classes, vec, Y, cv)
    
    if return_pred:
        return clf, y_pred
    else:
        return clf


#####
# 1.2. Logistic Regression
#####

# TODO


def svm(train_test, classes, vec, Y, version="", return_pred=True, cv=10, gamma="auto", C=1.0, coef0=0.0, kernel="linear"):
    """Computes the Support vector machine classifier and optionally the predicted class labels for X_test.
    
        Args:
            train_test (tuple): Tuple with the trainings- and test-data in the following order: X_train, X_test, y_train, y_test.
            classes (list): List of unique class names as strings.
            vec (csr matrix): Vectorizer of the text column of the df.
            Y (numpy array): Array which represents the categories of the category column of the df.
            
            version (string): String with the version to differentiate data sets.
            return_pred (bool): If True, the y_prediction will be returned.
            cv (int): Number of the cross validation test sets. 
            
            gamma (float): Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’. 
            C (float): Penalty parameter C of the error term.
            coef0 (float): Independent term in kernel function. It is only significant in ‘poly’ and ‘sigmoid’.
            kernel (string): String that specifies the kernel type to be used in the algorithm (‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’).
        Returns:
            Support vector machine classifier and optionally the predicted class labels for X_test.
    """
    if version == "":
        classifier_name = f"svm(C={C})"
    else:
        classifier_name = f"svm_{version}(C={C})"
    
    X_train = train_test[0]
    X_test = train_test[1]
    y_train = train_test[2]
    y_test = train_test[3]
    
    clf = SVC(gamma=gamma, C=C, coef0=coef0, kernel=kernel)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    #saving results
    saving_results(clf, classifier_name, y_test, y_pred, classes, vec, Y, cv)
        
    if return_pred:
        return clf, y_pred
    else:
        return clf

#TODO: comapre classifiers!
# - alle accuracies als boxplot und csv
# accuracies.to_csv("data/classifier/accuracies.csv")

#TODO: docstring
def run_classifiers(train_test, classes, vec, Y, cv=10):
    """
    Args:
        train_test (tuple): Tuple with the trainings- and test-data in the following order: X_train, X_test, y_train, y_test.
        classes (list): List of unique class names as strings.
        vec (csr matrix): Vectorizer of the text column of the df.
        Y (numpy array): Array which represents the categories of the category column of the df.
        cv (int): Number of the cross validation test sets. 
    """


def compare_classifiers():
    ...
    # von allen ordnern die wichtigsten daten klauen und zusammenstellen
    #  f1 score als vergleich
    
    
    





