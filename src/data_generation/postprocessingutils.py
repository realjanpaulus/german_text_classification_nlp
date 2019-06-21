#%%
import re
import pandas as pd
from nltk import word_tokenize


### Helper functions ###

def load_dic(path="data/german.dic"):
    """Returns a set with german dictionary words.
    
    Args:
        path (string): Path to the dic-file.
    Returns:
        Set with german dictionary words.    
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as dic:
        germandic = [word[:-1] for word in dic]
    return set(germandic)


def hasNumbers(string):
    """Returns True if the string contains a number."""
    return any(char.isdigit() for char in string)

#TODO: docstring
def find_foreign_phrase(string, dic):
    """ """
    foreign_words = []
    for idx, word in enumerate(word_tokenize(string)):
        if word in dic or word.capitalize() in dic or word.lower() in dic:
            pass
        else:
            special_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:"\'`.]')
            if special_regex.search(word) == None:
                foreign_words.append((word, idx))
    lw = 0
    last_phrase_word = ""
    for idx, tupel in enumerate(foreign_words[::-1]):
        if idx != 0:
            if (lw - tupel[1]) >= 2:
                break
        last_phrase_word = tupel[0]
        lw = tupel[1]
        
    return string[string.find(last_phrase_word):]


### postprocessing functions ###
    
def only_german_translation(text, dic):
    """Removes foreign terms or phrases when their german translation is given in parantheses.
    
    Args:
        text (string): String of a Wikipedia article.
        dic (set): Set with dictionary words as strings.
    Returns:
        String without the foreign terms or phrases but their german translation instead.
    """
    #TODO: erst muss removes non latin gemacht werden
    
    # matches 15 words or quotation before parantheses
    regex = re.compile("((?:(\w+\s+|\w+')){1,15}\(((d|D)eutsch:|zu (d|D)eutsch).*?\)|\"([^\"]*)\" \(((d|D)eutsch:|zu (d|D)eutsch):.*?\))")
    original_and_translation = regex.search(text)
    
    if original_and_translation != None:
        original = re.search("^.*?\(", original_and_translation.group()).group()[:-1]
        
        if re.search("\"([^\"]*)\"", original) == None:
            original = find_foreign_phrase(original, dic)
        
        paranthesis = re.search("\(((d|D)eutsch:|zu (d|D)eutsch).*?\)", original_and_translation.group())
        if paranthesis != None:
            translation = re.sub("\(((d|D)eutsch:|zu (d|D)eutsch). |\)", "", paranthesis.group())
        
        return text[:text.find(original)] + translation + text[text.find(paranthesis.group()) + len(paranthesis.group()):]
    else:
        return text
    
#%%
    
dic = load_dic()
s = 'An mehreren Stellen what is it im Film ist der Satz Who watches the Watchmen (zu deutsch: "Wer überwacht die Wächter?") zu sehen.'


print(only_german_translation(s, dic))




