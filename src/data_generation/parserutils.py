from nltk import word_tokenize
import itertools

def extracting_section(unnecessary_sections, sections, level=0):
    """Extracts recursively text from a list of sections and its subsections.
    
    Args:
        unnecessary_sections (list): List of sections which won't be returned.
        sections (list): List of sections of a Wikipedia article.
        level (int): Integer of the current level.
    Returns:
        String with the combined sections without the unnecessary sections.
    """
    extracted_text = ""
    for section in sections:
        if section.title not in unnecessary_sections:
            extracted_text += section.text
            extracted_text += extracting_section(unnecessary_sections, section.sections, level + 1)
            
    return extracted_text

#TODO: ...

"""
    Input: {cat:[subcat1, subcat2, subcat3, ...]}
    Output: {article_title1:{category:..., text:..., len:...}, article_title2:{category:..., text:..., len:...}}
"""



#%%
#TODO: docstring
def getArticle(wikipedia, article, category_name, unnecessary_sections):
    """
    Args:
        wikipedia (Wikipedia): Wikipedia-Object from the wikipediaapi-module
        article (WikipediaPage): Page of the Wikipedia-Article.
        category_name (string): Name of the articles category.
        unnecessary_sections (list): List of strings with skippable sections.
    """
    article_dict = {}
    #no anchored section articles in other articles
    if article.exists() == True and article.title == article.title:
        
        reduced_article = article.summary + extracting_section(unnecessary_sections, article.sections)
        
        if len(word_tokenize(reduced_article)) > 100 and len(word_tokenize(reduced_article)) < 2000:
            article_dict["category"] = category_name
            article_dict["text"] = reduced_article
            article_dict["length"] = len(word_tokenize(reduced_article))
            #article_dict["summary"] = article.summary
            
        elif len(word_tokenize(reduced_article)) >= 2000:
            
            #reduces the size of the article to 2000 without removing important punctuation marks after words
            splitted_article = [[word_tokenize(w), ' '] for w in reduced_article.split()][:2000]
            resized_reduced_article = ""
            resized_reduced_article = resized_reduced_article.join(list(itertools.chain(*list(itertools.chain(*splitted_article)))))
            
            article_dict["category"] = category_name
            article_dict["text"] = resized_reduced_article
            article_dict["length"] = len(word_tokenize(resized_reduced_article))
            #article_dict["summary"] = article.summary
            
    return article_dict

def generate_categories_list(wikipedia, categories, unnecessary_sections, max_articles=200):
    #TODO: list ist jetzt dict
    """Parses through a list of Wikipedia categories and extracts articles per category until the max_articles parameter is reached.
        Each article has to contain at least 100 words or symbols and articles which contain more than 2000 words or symbols will be shortened.
        The name of the category, the summary of the article and the whole reduced article is saved in a list which is saved in a category
        list and every list for every category is saved in the output categories_list.
    
    Args:
        wikipedia (Wikipedia): Wikipedia-Object from the wikipediaapi-module.
        categories (dict): Dict of Wikipedia category names as keys and a list of subcategories as values.
        unnecessary_sections (list): List of strings with skippable sections.
        max_articles (int): The maximum of articles per category.
    Returns:
        List of categories lists where the name of the category, the summary of the article and the whole reduced article is saved in a list.
    """
    
    articles = {}
    
    for category_name, subcategories in categories.items():
        article_counter = 0
        for subcategory in subcategories:
            if article_counter == max_articles:    
                break
            category = wikipedia.page(subcategory)
            for article in category.categorymembers.values():
                #no articles which aren't real articles but again a list of articles
                if article.ns == 0 and ("Liste von" not in article.title and "Liste d" not in article.title):
                    article_dict = getArticle(wikipedia, article, category_name, unnecessary_sections)
                    if article_dict:
                        articles[article.title] = article_dict
                        article_counter += 1 
                
        
        
        
        
        
        
        
        
        """
        category_list = []
        
        
        for subcategory in subcategories:
            if article_counter == max_articles:    
                break
            category = wikipedia.page(subcategory)
            for article in category.categorymembers.values():
                article_list = []
              
                    if article_list:
                        # only articles which doesn't contain only a summary
                        if (len(word_tokenize(article_list[2])) - len(word_tokenize(article_list[1]))) > 10:
                            category_list.append(article_list)
                        else:
                            article_counter = article_counter - 1
                    
                    if article_counter == max_articles:
                        break
        categories_list.append(category_list)"""
    return articles