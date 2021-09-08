# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


slide_elem.find('div', class_='content_title')


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


df.to_html()


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# 2. Create a list to hold the images and titles.

# Set up the HTML parser using BeautifulSoup, which parses the HTML text and then stores it as an object.
html = browser.html
soup1 = soup(html, 'html.parser')

#Parse Products List in HTML in element item
hemispheres = soup1.find_all('div', class_='item')

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
    
    #vist new sight and click on link
    browser.visit(image_link)
    
    # use css elements to access link to jpeg
    element = browser.find_link_by_text('Sample').first
    img_url = element['href']
    
#     browser.visit(image_link)
#     html = browser.html
#     hemi_soup = soup(html, 'html.parser')
    
#     div_downloads = hemi_soup.find("div", class_="downloads")
#     image_url_breadcrumb = div_downloads.a["href"]
#     image_url = base_url + image_url_breadcrumb

    # create a dictionary and send it to list
    hemisphere_image_urls.append({"title": title, "img_url": img_url})
#     hemisphere_image_urls.append(div_downloads)
    
print(hemisphere_image_urls) 


# 5. Quit the browser
browser.quit()
