# Webscrape NYT best selling books
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Setup file path for final csv output
PATH_TO_OUTPUT = "./"
todaysDate = datetime.today().strftime('%Y-%m-%d')

# Call the GET request
url = "https://www.nytimes.com/books/best-sellers/hardcover-nonfiction/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

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



# define helper functions
def getNytText(tag: str, myClass: str) -> list:
    """Performs GET request and returns list of all matches"""
    
    myList = soup.find_all(str(tag), class_=str(myClass))
    return (myList)


def makeNytDf(infoItem: str, tag: str, class_name: str) -> list:
    """
    Iterate through each item of interest
    """
    # get the "soup"
    infoItem = getNytText(str(tag), str(class_name))

    # create our empty list
    output = []

    # iterate  through all objects in our "soup"
    [output.append(item.get_text().title()) for item in infoItem]

    return (output)


def acquireBestSellers() -> None:
    """Executes helper functions to save as CSV file"""
    
    scrapedNyt = pd.DataFrame(
        map(makeNytDf, nytDf['infoItem'], nytDf['tag'], nytDf['class'])).transpose(
    ).rename(columns=nytDf['infoItem'])

    # remove the word "by" from the author series
    scrapedNyt['author'] = scrapedNyt['author'].map(lambda x: x.lstrip('By '))

    print(scrapedNyt)

    # Save to output folder
    scrapedNyt.to_csv(
        str(PATH_TO_OUTPUT) +
        '/' +
        str(todaysDate) +
        '_nytBestSellers.csv',

        index=False
    )

    print('Please find your file in the data-output folder')


if __name__ == "__main__":
    acquireBestSellers()
