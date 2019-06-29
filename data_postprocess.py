#%%
#TODO: src weg und setup.py
from src.data_generation import postprocessingutils as ppu

import argparse
import pandas as pd


#%%
def main():
    
    #TODO: check if valid path?
    #TODO: logging!
    #TODO: err[501!] bei einem der Witschaftsartikel
    
    ### reading corpus ###
    corpus = pd.read_csv(args.path)
    methods = ""
    
    if args.drop_duplicates:
        corpus = corpus.drop_duplicates(subset="text")
        methods += "-dd"
        
    if args.unify_articles_amount:
        corpus = ppu.unify_articles_amount(corpus)
        methods += "-uaa"
    
    if args.tokenization:
        corpus["text"] = corpus.text.map(ppu.tokenize)
        methods += "-t"
        
    if args.nonlatin:
        corpus["text"] = corpus.text.map(ppu.remove_nonlatin)
        methods += "-nl"
        
    if args.no_umlauts:
        corpus["text"] = corpus.text.map(ppu.replace_umlauts)
        methods += "-nu"
        
    if args.german_translation:
        corpus["text"] = corpus.text.apply(ppu.replace_foreign_phrase, dic=ppu.load_dic)
        methods += "-gt"
        
    if args.save_methods:
        corpus.to_csv(args.path[:-4] + "_v2 (" + methods + ").csv")
    else:
        corpus.to_csv(args.path[:-4] + "_v2" + ".csv")
        

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog="data_postprocess", description="Tool to apply postprocessing methods on a csv corpus.")
    parser.add_argument("path", type=str, help="Path to the csv-File which contains a corpus with a 'text'-column.")
    parser.add_argument("--drop_duplicates", "-dd", action="store_true", help="Indicates if the duplicates should be dropped.")
    parser.add_argument("--unify_articles_amount", "-uaa", action="store_true", help="Indicates if the amount of the articles per category should be unified.")
    parser.add_argument("--tokenization", "-t", action="store_true", help="Indicates if the articles should be tokenized or not.")
    parser.add_argument("--german_translation", "-gt", action="store_true", help="Indicates if given german translations should replace the original phrases.")
    parser.add_argument("--nonlatin", "-nl", action="store_true", help="Indicates if non-latin characters should be removed.")
    parser.add_argument("--no_umlauts", "-nu", action="store_true", help="Indicates if umlauts should be replaced.")
    parser.add_argument("--save_methods", "-sm", action="store_true", help="Indicates if an abbreviation for the postprocessing methods should be added to the output name.")
    args = parser.parse_args()
  
    ### main ###
    main()