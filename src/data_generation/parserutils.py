from nltk import word_tokenize
import itertools


def extracting_section(unnecessary_sections, sections, level=0):
    """Extracts text from a list of sections and its subsections recursively.

    Args:
        unnecessary_sections (list): List of sections which won't be returned.
        sections (list): List of sections of a Wikipedia article.
        level (int): Integer of the current level.
    Returns:
        String with the combined sections but without the unnecessary sections.
    """
    extracted_text = ""
    for section in sections:
        if section.title not in unnecessary_sections:
            extracted_text += section.text
            extracted_text += extracting_section(unnecessary_sections,
                                                 section.sections, level + 1)
    return extracted_text


def getArticle(wikipedia, article, category_name, unnecessary_sections):
    """Generates a dictionary with the title of the article as key and a
        dictionary with the keys "category", "text" and "length" as value.

    Example:
        >>> getArticle(wikipedia,
                       Altersrente (id: ??, ns: 0),
                       "Kategorie:Wirtschaft",
                       ["Literatur", "Weblinks", "Einzelnachweis",
                       "Einzelnachweise", "Siehe auch"])
        {"Altersrente":{category:"Kategorie:Wirtschaft", text:"...", len:1812}}
    Args:
        wikipedia (Wikipedia): Wikipedia-Object from the wikipediaapi-module
        article (WikipediaPage): Page of the Wikipedia-Article.
        category_name (string): Name of the articles category.
        unnecessary_sections (list): List of strings with skippable sections.
    Returns:
        Dictionary with the articles title as key and a dictionary with the
        keys "category", "text" and "length" as value.
    """
    article_dict = {}

    # no anchored section articles in other articles
    if article.exists():
        reduced_article = article.summary \
                            + extracting_section(unnecessary_sections,
                                                 article.sections)
        article_length = len(word_tokenize(reduced_article))

        if article_length > 100 and article_length < 2000:
            article_dict["category"] = category_name
            article_dict["text"] = reduced_article
            article_dict["length"] = article_length
            # article_dict["summary"] = article.summary

        elif article_length >= 2000:

            # reduces the size of the article to 2000 without removing
            # important punctuation marks after words
            splitted_article = [[word_tokenize(w), ' ']
                                for w in reduced_article.split()][:2000]
            resized_article = ""
            resized_article = resized_article.join(list(itertools.chain(
                                *list(itertools.chain(*splitted_article)))))

            article_dict["category"] = category_name
            article_dict["text"] = resized_article
            article_dict["length"] = len(word_tokenize(resized_article))
            # article_dict["summary"] = article.summary

    return article_dict


def generate_categories(wikipedia, categories, unnecessary_sections,
                        max_articles=200):
    """Parses through a dictionary of Wikipedia categories and extracts
        articles per category until the max_articles parameter is reached.
        Each article has to contain at least 100 words or symbols and articles
        which contain more than 2000 words or symbols will be shortened.
        The name of the category, the shortened article and the length of the
        article are saved in a dictionary which is linked with the articles
        title. This dictionary with the articles titles as keys is saved in an
        "articles"-dictionary.

    Args:
        wikipedia (Wikipedia): Wikipedia-Object from the wikipediaapi-module.
        categories (dict): Dict of Wikipedia category names as keys and
                            a list of subcategories as values.
        unnecessary_sections (list): List of strings with skippable sections.
        max_articles (int): The maximum of articles per category.
    Returns:
        Dictionary with the articles titles as keys and a dictionary with the
        keys "category", "text" and "length" as value.
    """

    articles = {}

    for category_name, subcategories in categories.items():
        article_counter = 0
        for subcategory in subcategories:
            if article_counter == max_articles:
                break
            category = wikipedia.page(subcategory)
            for article in category.categorymembers.values():
                # articles which aren't real articles but a list of articles
                # will be skipped
                if article.ns == 0 and ("Liste von" not in article.title
                                        and "Liste d" not in article.title):
                    article_dict = getArticle(wikipedia,
                                              article,
                                              category_name,
                                              unnecessary_sections)
                    if article_dict:
                        articles[article.title] = article_dict
                        article_counter += 1

    return articles
