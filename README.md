# German Text Classification Tutorial Series

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/realjanpaulus/german_text_classification_nlp/master)


This project mainly consists of a german tutorial series on text classification with Python and german data. The tutorials are available as Jupyter notebooks in the <b>tutorials</b> folder. In addition, this project contains tools for extracting articles from Wikipedia by categories and a csv-post-processing tool. Already prepared datasets are provided in the <b>data</b> folder. A smaller and more compact dataset is stored in the <b> dl_dataset </b> folder.

## Installation

Required: Python 3.6+

```pip install -r requirements.txt```

## Usage

For a detailed explanation of the following two tools see `tutorials/Zusatzkapitel - Wie baue ich mein eigenes Wikipediakorpus?` (only available in German).

### Wikiparser
```
$ python wikiparser.py --help
usage: path [-h] [--max_articles MAX_ARTICLES] [--save_date]

optional arguments:
-h, --help            show this help message and exit
--max_articles, -ma   sets the maximum of articles per category
--save_date, -sd      indicates if the generation date of the corpus should be saved

```

### Data Postprocess
```
$ python data_postprocess.py --help
usage: path [-h] [--drop_duplicates] [--unify_articles_amount] [--tokenization] [--german_translation] [--nonlation] [--no_umlauts] [--save_methods]

optional arguments:
-h, --help                      show this help message and exit
--drop_duplicates, -dd",        indicates if the duplicates should be dropped
--unify_articles_amount, -uaa   indicates if the amount of the articles per category                                   should be unified
--tokenization, -t              indicates if the articles should be tokenized or not
--german_translation, -gt       indicates if given german translations should replace                                 the original phrases
--nonlatin, -nl                 indicates if non-latin characters should be removed
--no_umlauts, -nu               indicates if umlauts should be replaced
--save_methods, -sm             indicates if an abbreviation for the postprocessing                                   methods should be added to the output name
    
```

## Project Structure

### data

Corpora with german Wikipedia articles and categories as csv-files (subfolder `corpora`), JSON-files with german Wikipedia categories and subcategories and a german dictionary file.

### dl_dataset

Dataset for the university course "Deep Learning" (Julius-Maximilians-university, SS19).

### src

<b>data_generation</b>: Module which stores all the python files for the generation of the data by parsing wikipedia articles on the basis of categories stored in wikicategories.json. The articles will be preprocessed (tokenization, removal of unnecessary parts etc.) and extracted into a csv-file with the columns "category", "summary", "text".

### tutorials

German tutorial series for Text Classification with Machine Learning, Scikit learn and Deep Learning as Jupyter Notebooks.
