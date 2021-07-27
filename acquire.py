from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd



# ************************************************** CODEUP BLOG ************************************************** 

def get_codeup_blog (url):
    '''
    '''
    #set the headers
    headers = {'User-Agent': 'Codeup Data Science'}
    
    #Get rhe http response object from the server
    response = get(url, headers=headers)
    
    soup = BeautifulSoup(response.text)
    
    # get the content
    content = soup.find('div', class_='jupiterx-post-content').get_text(strip = True)
    
    #get the title
    title = soup.find('h1', class_='jupiterx-post-title').text

    #get the date
    published_date = soup.time.text
    
    #create a dictionary
    dic = {
        'title': title,
        'content': content,
        'published_date': published_date
    }
    return dic



def get_glob_articles (urls):
    #create a list of dictionaries
    list_dic = [get_codeup_blog(url) for url in urls]
    
    return pd.DataFrame(list_dic)


# ************************************************** NEWS ARTICLES ************************************************** 

#create a function ther get a single article
def get_article(article, category):
    '''
    takes in a single article and category and return a dictionary with  the title, content and category of 
    the given article
    '''
    # Attribute selector
    title = article.select("[itemprop='headline']")[0].text
    
    # article body
    content = article.select("[itemprop='articleBody']")[0].text
    
    #create a dictionary
    output = {}
    #save info 
    output["title"] = title
    output["content"] = content
    output["category"] = category
    
    return output

#create a function to get all the articles
def get_articles(category, base ="https://inshorts.com/en/read/"):
    """
    This function takes in a category as a string. Category must be an available category in inshorts
    Returns a list of dictionaries where each dictionary represents a single inshort article
    """
    
    # We concatenate our base_url with the category
    url = base + category
    
    # Set the headers
    headers = {"User-Agent": "Codeup Data Scient student"}

    # Get the http response object from the server
    response = get(url, headers=headers)

    # Make soup out of the raw html
    soup = BeautifulSoup(response.text)
    
    # Ignore everything, focusing only on the news cards
    articles = soup.select(".news-card")
    
    output = []
    
    # Iterate through every article tag/soup 
    for article in articles:
        
        # Returns a dictionary of the article's title, body, and category
        article_data = get_article(article, category) 
        
        # Append the dictionary to the list
        output.append(article_data)
    
    # Return the list of dictionaries
    return output


def get_all_news_articles(categories):
    """
    Takes in a list of categories where the category is part of the URL pattern on inshorts
    Returns a dataframe of every article from every category listed
    Each row in the dataframe is a single article
    """
    all_inshorts = []

    for category in categories:
        all_category_articles = get_articles(category)
        all_inshorts = all_inshorts + all_category_articles

    df = pd.DataFrame(all_inshorts)
    return df