# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Instead of scraping each row or data in table, scrape the entire table with Pandas' .read_html() function.
import pandas as pd


# Set your executable path via Splinter
# Then set up the URL 'https://redplanetscience.com/' for scraping
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
    # Search for elements with a specific combination of tag (div) and attribute (list_text).
    # Tell our browser to wait one second before searching for components
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Set up the HTML parser using BeautifulSoup
html = browser.html
news_soup = soup(html, 'html.parser')
# Assign slide_elem as the variable to look for the <div /> tag and its descendent (the other tags within the <div /> element)
slide_elem= news_soup.select_one('div.list_text')


 # Chain .find onto our previously assigned variable, slide_elem and look for content title
slide_elem.find('div', class_='content_title')    


# Use the parent element to find the first `a` tag and save it as `news_title` variable
    # When the .get_text() this method is chained onto .find(), only the text of the element is returned.
news_title = slide_elem.find('div', class_='content_title').get_text()
print("-------------1st ARTICLE---------")
print(news_title)

# Use the parent element to find the paragraph text
news_summary = slide_elem.find('div', class_="article_teaser_body").get_text()
print("-------------SUMMARY-------------")
print(news_summary)


# Visit URL
url = 'https://spaceimages-mars.com/'
browser.visit(url)


# Find and click the full image button
    # Assign a  new variable to hold the scraping result
    # Use the browser finds to find an element by its tag
    # Use index chaining at the end of first block of code to stipulate taht we want our browser to click the 2nd button
full_imagine_elem = browser.find_by_tag('button')[1]
    # Splinter will "click" the imagine to view its full size
full_imagine_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url using BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image
    # An img tag is nested within this HTML, so we've included it.
    # .get('src') pulls the link to the image.
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel
# Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."


# Use the base URL to create an absolute URL
    # img_url is the variable that holds our f string
    # the f-string is a type of string formatting used for print statements in Python.
    # {} The curly brackets hold a variable that will be inserted into the f-string when it's executed.
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# Create a new DataFrame from the HTML table.
    # The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML.
    # By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list.
# Assign columns to the new DataFrame for additional clarity.
# Use the .set_index() function, we're turning the Description column into the DataFrame's index
    # inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df = pd.read_html('https://galaxyfacts-mars.com/')[0]
df.columns = ['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df    


df.to_html()


browser.quit()



