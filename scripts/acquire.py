# Webscrape NYT best selling books 

import pandas as pd
import requests
from bs4 import BeautifulSoup

# GET request
url = "https://www.nytimes.com/books/best-sellers/hardcover-nonfiction/"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

# define a function to get the "soup"
def getNytText(tag, myClass):
  myList = soup.find_all(str(tag), class_=str(myClass))
  return(myList)

# Create a dataframe that contains the items we need to iterate through
nytDf = pd.DataFrame({
  'infoItem': [
    'weeksOnList', 
    'title', 
    'author', 
    'publisher', 
    'abstract'
  ], 
  'tag': [
    'p', 
    'h3', 
    'p', 
    'p', 
    'p'
  ], 
  'class': [
    'css-1o26r9v', 
    'css-5pe77f', 
    'css-hjukut', 
    'css-heg334', 
    'css-14lubdp'
  ]
})

print(nytDf)

def makeNytDf(infoItem, tag, class_name):
  # get the "soup"
  infoItem = getNytText(str(tag), str(class_name))

  # create our empty list
  output = []

  # iterate  through all objects in our "soup"
  for item in infoItem:
    output.append(item.get_text().title()) # make title case too

  return(output)

scrapedNyt = pd.DataFrame(map(makeNytDf, nytDf['infoItem'], nytDf['tag'], nytDf['class'])).transpose().rename(columns = nytDf['infoItem'])

print(scrapedNyt)

###