# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # Initiate headless driver for deployment
       # When we were testing our code in Jupyter, headless was set as False so we could see the scraping in action. 
       # Now that we are deploying our code into a usable web app, we don't need to watch the script work.
       # So, when headless=True is declared as we initiate the browser, we are telling it to run in headless mode. 
       # All of the scraping will still be accomplished, but behind the scenes.
    browser = Browser('chrome', **executable_path, headless=True) 
    
    #  set our news title and paragraph variables 
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemisphere_image_urls": mars_hemispheres(browser),
      # adding the date the code was run last 
      "last_modified": dt.datetime.now(),
    }
    
    # Stop webdriver and return data
        # You can quit the automated browser by physically closing it, but there's a chance it won't fully quit in the background.
        # By using code to exit the browser, you'll know that all of the processes have been stopped.
    browser.quit()
    return data

def mars_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    slide_elem.find('div', class_='content_title')
    
    # Add try/except for error handling  Errors can pop up from anywhere, but in web scraping the most common cause 
    # of an error is when the webpage's format has changed and the scraping code no longer matches the new HTML 
    # elements.  Errors can pop up from anywhere, but in web scraping the most common cause of an error is when the 
    # webpage's format has changed and the scraping code no longer matches the new HTML elements.
    try:
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
            return None, None
    
    return news_title, news_paragraph

## JPL Space Images Featured Image
def featured_image(browser):
    
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

## Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    # A BaseException is a little bit of a catchall when it comes to error handling. It is raised when any of the 
    # built-in exceptions are encountered and it won't handle any user-defined exceptions. We're using it here because 
    # we're using Pandas' read_html() function to pull data, instead of scraping with BeautifulSoup and Splinter. 
    # The data is returned a little differently and can result in errors other than AttributeErrors, which is what 
    # we've been addressing so far.
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

## Mars Hemispheres
def mars_hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.

    # Set up the HTML parser using BeautifulSoup, which parses the HTML text and then stores it as an object.
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    #Parse Products List in HTML in element item
    hemispheres = hemi_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for which_hemisphere in hemispheres:
        # get title of hemisphere name and remove unnessary text
        full_title = which_hemisphere.h3.text
        title = full_title.replace(" Enhanced", "")
        
        # the base URL doesnt hold the absolute link to the JPEG, so parse html to link
        # add it to base url
        href_relative_link = which_hemisphere.find('a')['href']
        base_url = "https://marshemispheres.com/"
        image_link = base_url + href_relative_link
        
        #vist new sight adn click on link
        browser.visit(image_link)
        
        # use css elements to access link to jpeg
        element = browser.find_link_by_text('Sample').first
        img_url = element['href']

        # create a dictionary and send it to list
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
        
    return hemisphere_image_urls

# tell Flask that our script is complete and ready for action.
if __name__=='__main__':
    # If running as script, print scraped data
    print(scrape_all())
    