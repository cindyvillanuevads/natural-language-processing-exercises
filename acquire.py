from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd


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