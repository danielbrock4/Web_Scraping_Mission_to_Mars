# import Splinter and Beautiful Soap
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
    #**executable_path is unpacking the dictionary we've stored the path in – think of it as unpacking a suitcase
    # headless=False means that all of the browser's actions will be displayed in a Chrome window so we can see them.


# Visit the Quotes to Scrape site
    #This code tells Splinter which site we want to visit by assigning the link to a URL.
url = 'http://quotes.toscrape.com/'
browser.visit(url)


# Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')


# In our next cell, we will find the title and extract it.

# Scrape the Title
    # We used our html_soup object we created earlier and chained find() to it to search for the <h2 /> tag.
    # We've also extracted only the text within the HTML tags by adding .text to the end of the code.
title = html_soup.find('h2').text
title


# Scrape the top ten tags
    # Create a new variable tag_box, which will be used to store the results of a search.
        # In this case, we're looking for <div /> elements with a class of tags-box, and we're searching for it in the HTML we parsed earlier and stored in the html_soup variable.
tag_box = html_soup.find('div', class_='tags-box')
# tag_box
    # Hold the results of a find_all, but this time we're searching through the parsed results stored in our tag_box variable to find <a /> elements with a tag class. 
        # Use find_all this time because we want to capture all results, instead of a single or specific one.
tags = tag_box.find_all("a", class_='tag')

# Add for lopp
    # This for loop cycles through each tag in the tags variable, strips the HTML code out of it, and then prints only the text of each tag.
for tag in tags: # a for loop that cycles through each tag in the list
    word = tag.text # strips the HTLM from the code and assings the result to a variable
    print(word) #prints each word in the list


for x in range(1, 6): # a for loop with five interations (pages 1- 6)
   html = browser.html # Create an HTML object, assigned to html variable
   quote_soup = soup(html, 'html.parser') # Use BeautifulSoup to parse the html object
   quotes = quote_soup.find_all('span', class_='text') # Use BeautifulSoup to final all <span \> tags with a class of "text".
   for quote in quotes: #Print statments Wrapped in another for loop thta will print each parsed
      print('page:', x, '----------')
      print(quote.text)
   browser.links.find_by_partial_text('Next').click() #Use Splinter to click the "Next" button



