# German Text Classification Tutorial Series

This project mainly consists of a german tutorial series on text classification with Python and german data. The tutorials are available as Jupyter notebooks are in the <b>tutorials</b> folder. In addition, this project contains tools for extracting articles from Wikipedia by categories. Other available tools include a post-processing tool and a text classification tool with classifier from Scikit learn. Already prepared datasets are provided in the <b>data</b> folder. A smaller and more compact dataset is stored in the <b> dl_dataset </b> folder.

## Installation

Required: Python 3.6+

```pip install -r requirements.txt```

## Project Structure

### data
...

### dl_datasat
...

### src

<b>data_generation</b>: Module which stores all the python files for the generation of the data by parsing wikipedia articles on the basis of categories stored in wikicategories.json. The articles will be preprocessed (tokenization, removal of unnecessary parts etc.) and extracted into a csv-file with the columns "category", "summary", "text".

### tutorials
