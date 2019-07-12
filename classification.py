#%%
#TODO: src weg und setup.py
from src.data_classification import classifierutils as clfu
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import argparse


def main():
    corpus = pd.read_csv(args.path)
    classes = corpus["category"].drop_duplicates().tolist()
    vec = TfidfVectorizer().fit_transform(corpus["text"])
    Y = LabelEncoder().fit_transform(corpus["category"])
    
    X_train, X_test, y_train, y_test = train_test_split(vec, 
                                                        Y,
                                                        test_size=0.2, 
                                                        random_state=42, 
                                                        shuffle=True)
    
    train_test = (X_train, X_test, y_train, y_test)
    
    
    if args.classifier == "all":
        print("hallo")
    elif args.classifier == "svm":
        svmclf, y_pred = clfu.svm(train_test, classes, vec, Y)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog="classification", description="Tool to classify a csv corpus and save the results.")
    parser.add_argument("path", type=str, help="Path to the csv-File which contains a corpus with a 'text'-column.")
    parser.add_argument("--classifier", "-clf", choices=["svm", "all"], type=str.lower, help="Choice of the classifier")
    args = parser.parse_args()
  
    ### main ###
    main()