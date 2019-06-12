#%%
import wikipediaapi
from nltk import word_tokenize

import pandas as pd
import json
from pathlib import Path
import argparse
import logging

logging.basicConfig(level=logging.INFO, filename="wikiparser.log", filemode="w")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s: %(message)s")
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def main():    
    ### loading categories from JSON-file ###
    with Path(args.categories_path).open('r', encoding="utf-8") as f:
        wikicategories = json.load(f)
        logging.info("Successfully loaded the JSON-File.")
        
    
    
    wikipedia = wikipediaapi.Wikipedia('de', extract_format=wikipediaapi.ExtractFormat.WIKI)
    dfcolumns = ["category", "summary", "text"]
    unnecessary_sections = ["Literatur", "Weblinks", "Einzelnachweis", "Einzelnachweise", "Siehe auch"]
    
    ### generating categories list ###
    
    #TODO: generate_categories_list
    #TODO: create parserutils 
    #categories_list = parserutils.generate_categories_list(wikipedia, wikicategories, unnecessary_sections, max_articles=240)
    logging.info("Successfully generated lists of the articles.")
    
    
    ### saving categories list to csv ###

    #TODO: dataframe saving
    #df = pd.DataFrame(columns=dfcolumns)
    """for idx, l in enumerate(categories_list):
        tmpdf = pd.DataFrame.from_records(l, columns=dfcolumns)
        df = df.append(tmpdf)"""
    #df.to_csv("data/corpora/wikicatcorpus_v2.csv", index=False)
    logging.info("Successfully saved the articles to a csv file.") #TODO: hinweis, wo gespeichert

    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog="wikiparser", description="Tool to create a corpus of Wikipedia articles based on Wikipedia categories.")
    parser.add_argument("--categories_path", "-cp", help="JSON-File with the dictionary of the Wikipedia categories.")
    args = parser.parse_args()
    

    ### main ###
    main()


#%%
"""
    OLD
"""
"""

import wikipediaapi
import pandas as pd
from nltk import word_tokenize
#from text_classfication_nlp import parserutils, postprocessing
import json

#%%
#####
# loading categories
#####

wikipedia = wikipediaapi.Wikipedia('de', extract_format=wikipediaapi.ExtractFormat.WIKI)

dfcolumns = ["category", "summary", "text"]
unnecessary_sections = ["Literatur", "Weblinks", "Einzelnachweis", "Einzelnachweise", "Siehe auch"]

with open('data/wikicategories.json', 'r') as f:
    wikicategories = json.load(f)
#%%
#####
# creating the corpus
#####
#max = 240 because of possible duplicates
categories_list = parserutils.generate_categories_list(wikipedia, wikicategories, unnecessary_sections, max_articles=240)

df = pd.DataFrame(columns=dfcolumns)
    
for idx, l in enumerate(categories_list):
    tmpdf = pd.DataFrame.from_records(l, columns=dfcolumns)
    df = df.append(tmpdf)

df.to_csv("data/corpora/wikicatcorpus_v2.csv", index=False)
#%%
#####
# dropping duplicates and reducing the count of every article per catgory to 200
#####
df = df.drop_duplicates("summary")
df["category"].value_counts()

# only 200 articles per category
actual_category = ""
new_df = pd.DataFrame(columns=dfcolumns)
for idx, category in enumerate(df["category"]):
    if actual_category != category:
        actual_category = category
        print(actual_category)
        new_df = new_df.append(df.loc[df["category"] == category][0:200])
        

new_df.to_csv("data/corpora/wikicatcorpus_v2.csv", index=False)
#%%
#####
# postprocessing and creation of different corpus variants
#####


## everything removed##
# no doubleequalsigns, only german translation, remove birth-death-dates, no non latin #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_1 = postprocessing.corpus_postprocessing(df)
df_v3_1.to_csv("data/corpora/wikicatcorpus_v3_1.csv", index=False)
# no doubleequalsigns, only german translation, remove birth-death-dates, no non latin, tokenized text #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_1t = postprocessing.corpus_postprocessing(df, tokenization=True)
df_v3_1t.to_csv("data/corpora/wikicatcorpus_v3_1t.csv", index=False)
# no doubleequalsigns, only german translation, remove birth-death-dates, no non latin, replaces umlauts #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_1u = postprocessing.corpus_postprocessing(df, replacing_umlauts=True)
df_v3_1u.to_csv("data/corpora/wikicatcorpus_v3_1u.csv", index=False)
# no doubleequalsigns, only german translation, remove birth-death-dates, no non latin, replaces umlauts, tokenized text #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_1tu = postprocessing.corpus_postprocessing(df, tokenization=True, replacing_umlauts=True)
df_v3_1tu.to_csv("data/corpora/wikicatcorpus_v3_1tu.csv", index=False)

## no german translation inside parantheses ##
# no doubleequalsigns, remove birth-death-dates, no non latin #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_2 = postprocessing.corpus_postprocessing(df, only_german=False)
df_v3_2.to_csv("data/corpora/wikicatcorpus_v3_2.csv", index=False)
# no doubleequalsigns, remove birth-death-dates, no non latin, tokenized text #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_2t = postprocessing.corpus_postprocessing(df, tokenization=True, only_german=False)
df_v3_2t.to_csv("data/corpora/wikicatcorpus_v3_2t.csv", index=False)
# no doubleequalsigns, remove birth-death-dates, no non latin, replaces umlauts #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_2u = postprocessing.corpus_postprocessing(df, only_german=False, replacing_umlauts=True)
df_v3_2u.to_csv("data/corpora/wikicatcorpus_v3_2u.csv", index=False)
# no doubleequalsigns, remove birth-death-dates, no non latin, replaces umlauts, tokenized text #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_2tu = postprocessing.corpus_postprocessing(df, tokenization=True, only_german=False, replacing_umlauts=True)
df_v3_2tu.to_csv("data/corpora/wikicatcorpus_v3_2tu.csv", index=False)


## no removed birth death dates ##
# no doubleequalsigns, only german translation, no non latin #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_3 = postprocessing.corpus_postprocessing(df, birth_death_dates=False)
df_v3_3.to_csv("data/corpora/wikicatcorpus_v3_3.csv", index=False)
# no doubleequalsigns, only german translation, no non latin, tokenized text #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_3t = postprocessing.corpus_postprocessing(df, tokenization=True, birth_death_dates=True)
df_v3_3t.to_csv("data/corpora/wikicatcorpus_v3_3t.csv", index=False)
# no doubleequalsigns, only german translation, no non latin, replaces umlauts #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_3u = postprocessing.corpus_postprocessing(df, birth_death_dates=False, replacing_umlauts=True)
df_v3_3u.to_csv("data/corpora/wikicatcorpus_v3_3u.csv", index=False)
# no doubleequalsigns, only german translation, no non latin, replaces umlauts, tokenized text #
df = pd.read_csv("data/corpora/wikicatcorpus_v2.csv")
df_v3_3tu = postprocessing.corpus_postprocessing(df, tokenization=True, birth_death_dates=True, replacing_umlauts=True)
df_v3_3tu.to_csv("data/corpora/wikicatcorpus_v3_3tu.csv", index=False)
"""
