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

#TODO:
def save_classification_report(classifier_name, y_true, y_pred, labels):
    """
    """
    with open(f"data/classifier/classification_reports/{classifier_name}-report.txt", "w", encoding="utf-8") as file:
        report = classification_report(y_true, y_pred, target_names=labels)
        file.write(report)


#TODO:
def plot_confusion_matrix(cm, classes, classifier_name):
    """
    """
    df = pd.DataFrame(cm, index=classes, columns=classes)
    plt.figure(figsize=(10, 9))
    sns.heatmap(df, annot=True, cmap=sns.color_palette("Blues"))
    plt.tight_layout()
    plt.savefig(f"data/classifier/confusion_matrices/{classifier_name}_cm.svg")
    plt.savefig(f"data/classifier/confusion_matrices/{classifier_name}_cm.png")
    df.to_csv(f"data/classifier/confusion_matrices/{classifier_name}_cm.csv")

#TODO:
def save_cross_validation(classifier_name, cross_val):
    cross_val_df = pd.DataFrame(cross_val, columns=[f"{classifier_name}"])
    cross_val_df.to_csv(f"data/classifier/cross_validation/{classifier_name}_cross_val.csv", index=False)
    
    plt.figure()
    ax = cross_val_df.plot.box(vert=False, color="black")
    ax.set_ylabel("Category")
    ax.set_xlabel("Accuracy")
    plt.tight_layout()
    plt.savefig(f"data/classifier/accuracy_boxplots/{classifier_name}_accuracies.svg")
    plt.savefig(f"data/classifier/accuracy_boxplots/{classifier_name}_accuracies.png")


#TODO:
def save_f1_scores(classifier_name, y_pred, y_test):
    """
    """
    scores = {f"{classifier_name}":{"micro": np.around(f1_score(y_pred, y_test, average="micro"), decimals=3),
                                    "macro": np.around(f1_score(y_pred, y_test, average="macro"), decimals=3),
                                    "weighted": np.around(f1_score(y_pred, y_test, average="weighted"), decimals=3)}}
    scores_df = pd.DataFrame(scores)
    scores_df = scores_df.T
    scores_df.to_csv(f"data/classifier/f1_scores/{classifier_name}_f1.csv")

    #TODO:
    #return scores


### classifier functions ###

#TODO:!!!
def svm(train_test, classes, vec, Y, version="", return_pred=True, gamma="auto", C=1.0, coef0=0.0, kernel="linear"):
    """Computes the Support vector machine classifier and optionally the predicted class labels for X_test.
    
        Args:
            train_test (tuple): Tuple with the trainings- and test-data in the following order: X_train, X_test, y_train, y_test.
            classes (list): List of unique class names as strings.
            vec (csr matrix): Vectorizer of the text column of the df.
            Y (numpy array): Array which represents the categories of the category column of the df.
            
            version (string): String with the version to differentiate data sets.
            return_pred (bool): If True, the y_prediction will be returned.
            gamma (float): Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’. 
            C (float): Penalty parameter C of the error term.
            coef0 (float): Independent term in kernel function. It is only significant in ‘poly’ and ‘sigmoid’.
            kernel (string): String that specifies the kernel type to be used in the algorithm (‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’).
        Returns:
            Support vector machine classifier and optionally the predicted class labels for X_test.
    """
    classifier_name = f"svm_{version} (C={C})"
    X_train = train_test[0]
    X_test = train_test[1]
    y_train = train_test[2]
    y_test = train_test[3]
    
    svmclf = SVC(gamma=gamma, C=C, coef0=coef0, kernel=kernel)
    svmclf.fit(X_train, y_train)
    y_pred = svmclf.predict(X_test)
    
    #save report
    save_classification_report(classifier_name, y_test, y_pred, classes)
    
    #save confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plot_confusion_matrix(cm, classes, classifier_name)
    
    #cross validation
    svm_cross_val = cross_val_score(svmclf, vec, Y, cv=10) 
    save_cross_validation(classifier_name, svm_cross_val)
    
    
    save_f1_scores(classifier_name, y_pred, y_test)
        
    if return_pred:
        return svmclf, y_pred
    else:
        return svmclf
    
  
#TODO: comapre classifiers!
# - alle accuracies als boxplot und csv
# accuracies.to_csv("data/classifier/accuracies.csv")
