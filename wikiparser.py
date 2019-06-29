import wikipediaapi
#TODO: src weg und setup.py
from src.data_generation import parserutils
import pandas as pd
import numpy as np
import json
from pathlib import Path
import argparse
import logging
import sys
import time
from datetime import datetime


### wikipediaapi logging handler ###
wikipediaapi.log.setLevel(level=wikipediaapi.logging.WARNING)
out_hdlr = wikipediaapi.logging.StreamHandler(sys.stderr)
out_hdlr.setFormatter(wikipediaapi.logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(wikipediaapi.logging.WARNING)
wikipediaapi.log.addHandler(out_hdlr)


### wikiparser logging handler ###
logging.basicConfig(level=logging.INFO, filename="logs/wikiparser.log", filemode="w")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s: %(message)s")
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def main():   
    ### loading categories from JSON-file ###
    with Path(args.path).open('r', encoding="utf-8") as f:
        wikicategories = json.load(f)
        logging.info(f"Successfully loaded the categories from the JSON-File.")
    
    ### hyperparams ###
    wikipedia = wikipediaapi.Wikipedia('de', extract_format=wikipediaapi.ExtractFormat.WIKI)
    unnecessary_sections = ["Literatur", "Weblinks", "Einzelnachweis", "Einzelnachweise", "Siehe auch"]
    
    
    if len(wikicategories) <= 10:
        csv_name = "data/smallwikicorpus"
    elif len(wikicategories) > 10 and len(wikicategories) <= 50:
        csv_name = "data/wikicorpus"
    else:
        csv_name = "data/bigwikicorpus"
        
    if args.save_date:
        csv_name += f" ({datetime.now():%d.%m.%y}_{datetime.now():%H:%M}).csv"
    else:
        csv_name += ".csv"
        
    st = time.time()
    
    ### generating categories dictionary ###
    if args.max_articles is not None:
        max_articles = args.max_articles
    else:
        max_articles = 240
    categories = parserutils.generate_categories(wikipedia,
                                                      wikicategories,
                                                      unnecessary_sections,
                                                      max_articles=max_articles)
    logging.info(f"Successfully generated lists of the articles (time: {int((time.time() - st) / 60)} minutes).")
    
    ### generating dataframe and saving csv###
    df = pd.DataFrame([v for k, v in categories.items()])
    logging.info(f"Successfully generated the dataframe (time: {int((time.time() - st))} seconds).")
    
    df.to_csv(f"{csv_name}")

    logging.info(f"Successfully saved the articles to the csv file '{csv_name}' (time: {int((time.time() - st))} seconds).")
    logging.info(f"Total runtime: {np.around((time.time() - st) / 60, decimals=2)} minutes.")
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog="wikiparser", description="Tool to create a corpus of Wikipedia articles based on Wikipedia categories.")
    parser.add_argument("path", type=str, help="Path to the JSON-File which contains the dictionary of the Wikipedia categories.")
    parser.add_argument("--max_articles", "-ma", type=int, help="Sets the maximum of articles per category.")
    parser.add_argument("--save_date", "-sd", action="store_true", help="Indicates if the generation date of the corpus should be saved.")
    args = parser.parse_args()
  
    ### main ###
    main()
