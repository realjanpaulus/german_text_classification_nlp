#%%
#TODO: src weg und setup.py
from src.data_classification import classifierutils as clfu
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


f1_scores = list()
accuracies = pd.DataFrame()
data = pd.read_csv("dl_dataset/smallwikicorpus_v2.csv")
classes = data["category"].drop_duplicates().tolist()
vec = TfidfVectorizer().fit_transform(data["text"])
Y = LabelEncoder().fit_transform(data["category"])

X_train, X_test, y_train, y_test = train_test_split(vec, Y,
                                                    test_size=0.2, 
													    random_state=42, 
													    shuffle=True)


svmclf, y_pred = clfu.svm((X_train, X_test, y_train, y_test), classes, vec, Y)