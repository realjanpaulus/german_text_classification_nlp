from src.data_generation import postprocessingutils as ppu

import argparse
import pandas as pd

def main():
    dic = ppu.load_dic()
    
    #TODO: optionen einbauen


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog="wikiparser", description="Tool to create a corpus of Wikipedia articles based on Wikipedia categories.")
    parser.add_argument("--path", "-p", help="Path to the csv-File which contains the Wikipedia articles with their categories.")
    parser.add_argument("--tokenization", "-t", type=bool, help="Indicates if the articles should be tokenized or not.")
    parser.add_argument("--only_german", "-g", type=bool, help="Indicates if given german translations should replace the original phrases.")
    parser.add_argument("--nonlatin", "-l", type=bool, help="Indicates if non-latin characters should be removed.")
    parser.add_argument("--no_umlauts", "-u", type=bool, help="Indicates if umlauts should be replaced.")
    #parser.add_argument("--postprocessing", "-pp", type=bool, help="Indicates if general postprocessing should be applied.")
    args = parser.parse_args()
  
    ### main ###
    main()