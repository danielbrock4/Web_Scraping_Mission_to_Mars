#!/usr/bin/env python
# coding: utf-8

# ## MISSION TO MARS
# ### Scrape Mars Data: The News

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

# Instead of scraping each row or data in table, scrape the entire table with Pandas' .read_html() function.
import pandas as pd


# Set up the executable path and initialize a browser. With these two lines of code, we are creating an instance of a Splinter browser.  This means that we're prepping our automated browser.  We're also specifying that we'll be using Chrome as our browser.

# In[2]:


# Set your executable path via Splinter
# Then set up the URL 'https://redplanetscience.com/' for scraping
    #**executable_path is unpacking the dictionary we've stored the path in – think of it as unpacking a suitcase
    # headless=False means that all of the browser's actions will be displayed in a Chrome window so we can see them.
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Assign the URL and instruct the browser to visit it
# 
# With the following line, browser.is_element_present_by_css('div.list_text', wait_time=1), we are accomplishing two things:
# 1) We're searching for elements with a specific combination of tag (div) and attribute (list_text). As an example, ul.item_list would be found in HTML as ul class="item_list".
# 2) We're also telling our browser to wait one second before searching for components. The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
    # Search for elements with a specific combination of tag (div) and attribute (list_text).
    # Tell our browser to wait one second before searching for components
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Use BeautifulSoup to parse the HTML. This means that BeautifulSoup has taken a look at the different components and can now access them. Specifically, BeautifulSoup parses the HTML text and then stores it as an object.

# In[4]:


# Set up the HTML parser using BeautifulSoup
html = browser.html
news_bs = bs(html, 'html.parser')
# Assign slide_elem as the variable to look for the <div /> tag and its descendent (the other tags within the <div /> element)
    # This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further.
    # The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text. 
    # CSS works from right to left, such as returning the last item on the list instead of the first.
    # Because of this, when using select_one, the first matching element returned will be a <li /> element with a class of slide and all nested elements within it.
slide_elem = news_bs.select_one('div.list_text')


# After opening the page in a new browser, right-click to inspect and activate your DevTools. Then search for the HTML components you'll use to identify the title and paragraph you want.We'll want to assign the title and summary text to variables we'll reference later. 
# 
# In this line of code, we chained .find onto our previously assigned variable, slide_elem. When we do this, we're saying, "This variable holds a ton of information, so look inside of that information to find this specific data." The data we're looking for is the content title, which we've specified by saying, "The specific data is in a <div /> with a class of 'content_title'."

# In[5]:


# Chain .find onto our previously assigned variable, slide_elem and look for content title
slide_elem.find('div', class_='content_title')


# The title is in that mix of HTML in our output—that's awesome! But we need to get just the text, and the extra HTML stuff isn't necessary

# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title` variable
    # When the .get_text() this method is chained onto .find(), only the text of the element is returned.
news_title = slide_elem.find('div', class_='content_title').get_text()
print("-------------1st ARTICLE---------")
print(news_title)

# Use the parent element to find the paragraph text
news_summary = slide_elem.find('div', class_="article_teaser_body").get_text()
print("-------------SUMMARY-------------")
print(news_summary)


# ##### IMPORTANT
# There are two methods used to find tags and attributes with BeautifulSoup:
# * .find() is used when we want only the first class and attribute we've specified.
# * .find_all() is used when we want to retrieve all of the tags and attributes.
# For example, if we were to use .find_all() instead of .find() when pulling the summary, we would retrieve all of the summaries on the page instead of just the first one.

# ### Scrape Mars Data: Featured Image

# The first image that pops up on the webpage is the featured image. Robin wants the full-size version of this image, so we know we'll want Splinter to click the "Full Image" button. From there, the page directs us to a slideshow. It's a little closer to getting the full-size feature image, but we aren't quite there yet.

# In[7]:


# Visit URL
url = 'https://spaceimages-mars.com/'
browser.visit(url)


# Next, we want to click the "Full Image" button. This button will direct our browser to an image slideshow. Let's take a look at the button's HTML tags and attributes with the DevTools.
# 
# This is a fairly straightforward HTML tag: the "button" element has a two classes (btn and btn-outline-light) and a string reading "FULL IMAGE". First, let's use the dev tools to search for all the button elements.
# 
# Since there are only three buttons, and we want to click the full-size image button, we can go ahead and use the HTML tag in our code.

# In[8]:


# Find and click the full image button
    # Assign a  new variable to hold the scraping result
    # Use the browser finds to find an element by its tag
    # Use index chaining at the end of first block of code to stipulate taht we want our browser to click the 2nd button
full_image_elem = browser.find_by_tag("button")[1]
# Splinter will "click" the imagine to view its full size
full_image_elem.click() 


# With the new page loaded onto our automated browser, it needs to be parsed so we can continue and scrape the full-size image URL. 

# In[9]:


# Parse the resulting html with soup
html = browser.html
img_bs = bs(html, 'html.parser')


# Now we need to find the relative image URL. In our browser (make sure you're on the same page as the automated one), activate your DevTools again. This time, let's find the image link for that image. It's important to note that the value of the src will be different every time the page is updated, so we can't simply record the current value—we would only pull that image each time the code is executed, instead of the most recent one.
# 
# We'll use the image tag and class (img /and fancybox-img) to build the URL to the full-size image. 

# In[10]:


# Find the relative image url using BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image
    # An img tag is nested within this HTML, so we've included it.
    # .get('src') pulls the link to the image.
img_url_rel = img_bs.find('img', class_='fancybox-image').get('src')
img_url_rel
# Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."


# Let's add the base URL to our code, because if we copy and paste this link into a browser, it won't work. This is because it's only a partial link, as the base URL isn't included. If we look at our address bar in the webpage, we can see the entire URL up there already; we just need to add the first portion to our app.
# 
# We're using an f-string for this print statement because it's a cleaner way to create print statements; they're also evaluated at run-time. This means that it, and the variable it holds, doesn't exist until the code is executed and the values are not constant. This works well for our scraping app because the data we're scraping is live and will be updated frequently.

# In[11]:


# Use the base URL to create an absolute URL
    # img_url is the variable that holds our f string
    # the f-string is a type of string formatting used for print statements in Python.
    # {} The curly brackets hold a variable that will be inserted into the f-string when it's executed.
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Scrape Mars Data: Mars Facts
# Get a table from Mars Facts and display it as a table on our own web app. Let's look at the webpage again, this time using our DevTools. All of the data we want is in a table / tag. 
# 
# Tables in HTML are basically made up of many smaller containers. The main container is the table / tag. Inside the table is tbody /, which is the body of the table—the headers, columns, and rows.
# 
# tr / is the tag for each table row. Within that tag, the table data is stored in td / tags. This is where the columns are established.
# 
# Instead of scraping each row, or the data in each td /, we're going to scrape the entire table with Pandas' .read_html() function.

# In[12]:


# Create a new DataFrame from the HTML table.
    # The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML.
    # By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list.
# Assign columns to the new DataFrame for additional clarity.
# Use the .set_index() function, we're turning the Description column into the DataFrame's index
    # inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
df = pd.read_html('https://galaxyfacts-mars.com/')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# Robin's web app is going to be an actual webpage. Thankfully, Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function. 
# 
# The result is a slightly confusing-looking set of HTML code—it's a <table /> element with a lot of nested elements. This means success. After adding this exact block of code to Robin's web app, the data it's storing will be presented in an easy-to-read tabular format.

# In[13]:


df.to_html()


# Now that we've gathered everything on Robin's list, we can end the automated browsing session. This is an important line to add to our web app also. Without it, the automated browser won't know to shut down—it will continue to listen for instructions and use the computer's resources (it may put a strain on memory or a laptop's battery if left on). 

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[14]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.

# Set up the HTML parser using BeautifulSoup, which parses the HTML text and then stores it as an object.
html = browser.html
soup = bs(html, 'html.parser')

#Parse Products List in HTML in element item
hemispheres = soup.find_all('div', class_='item')

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
    
#     browser.visit(image_link)
#     html = browser.html
#     soup = soup(html, 'html.parser')
    
#     div_downloads = soup.find("div", class_="downloads")
#     image_url_breadcrumb = div_downloads.a["href"]
#     image_url = base_url + image_url_breadcrumb

    # create a dictionary and send it to list
    hemisphere_image_urls.append({"title": title, "img_url": img_url})
    
print(hemisphere_image_urls) 


# In[14]:


browser.quit()


# ### Export to Python
# 
# JUPYTER LAB:
# 1) While your notebook is open, navigate to the top of the page to the Files tab.
# 2) From here, scroll down to the "Export Notebook as" section of the drop-down menu.
# 3) Select "Executeable Script (.py)" from the next menu to download the code.
# JUPYTER NOTEBOOK:
# 
# The Jupyter ecosystem is an extremely versatile tool. We already know many of its great functions, such as the different libraries that work well with it and also how easy it is to troubleshoot code. Another feature is being able to download the notebook into different formats.
# 
# There are several formats available, but we'll focus on one by downloading to a Python file.
# 
# 1) While your notebook is open, navigate to the top of the page to the Files tab.
# 2) From here, scroll down to the "Download as" section of the drop-down menu.
# 3) Select "Python (.py)" from the next menu to download the code.
# 4) If you get a warning about downloading this type of file, click "Keep" to continue the download. 
# 5) Navigate to your Downloads folder and open the new file. A brief look at the first lines of code shows us that the code wasn't the only thing to be ported over. The number of times each cell has been run is also there, for example.
# 6) Clean up the code by removing unnecessary blank spaces and comments.
# 
# 

# ## MONGODB: Store the Data

# MongoDB (Mongo for short) is a non-relational database that stores data in Binary JavaScript Object Notation (JSON), or BSON format. We'll access data stored in Mongo the same way we access data stored in JSON files. This method of data storage is far more flexible than SQL's model.
# 
# A Mongo database contains collections. These collections contain documents, and each document contains fields, and fields are where the data is stored.
# 
# JSON, JavaScript Object Notation, is a method that sorts and presents data in the form of key:value pairs. It looks much like a Python dictionary and can be traversed through using list notation.
# 
# #### Starting MongDB (Windows)
# 1) To get started with Mongo, first open a new terminal window, but make sure your working environment is activated. Note that your environment does not need to have the same name as the one in the image.
# 2) Then, to start an instance, type mongod into the first line of your terminal and press return or enter on your keyboard. We need to keep this tab open and active so that the Mongo instance continues to run. While Mongo does have a GUI, similar to pgAdmin for Postgres, we'll be using a command line interface (CLI) to make connections within the database.
# 3) In our terminal, create a second window or tab to use for working in Mongo. Again, make sure your environment is active.On the first line of this new window, type "mongo." 

# #### Create a Database
# 
# * use = In the terminal where Mongo is active and awaiting instruction, type "use practicedb" and then press Enter. This creates a new database named "practicedb" and makes it our active database.
# * db = When “db” is entered by itself, the active database is returned.
# * show dbs = You can also see how many databases are stored locally by typing "show dbs" in your terminal.
# * show collections = There is also a way to check to see what data, or collections, are already in the database.
# 
# #### Insert Data
# 
# The syntax follows: db.collectionName.insert({key:value}). Its components do the following:
# * db refers to the active database, practicedb.
# * collectionName is the name of the new collection we're creating (we'll customize it when we practice).
# * .insert({ }) is how MongoDB knows we're inserting data into the collection.
# * key:value is the format into which we're inserting our data; its construction is very similar to a Python dictionary.
# 
# EXAMPLE:
# db.zoo.insert({name: 'Cleo', species: 'jaguar', age: 12, hobbies: ['sleeping', 'eating', 'climbing']})
# 
# After pressing Enter, the next line in your terminal should read WriteResult({ 'nInserted" : 1 }). This means that we've successfully inserted Cleo into the database.
# 
# Documents can also be deleted or dropped. The syntax to do so follows: db.collectionName.remove({}).
# 
# We can also empty the collection at once, instead of one document at a time. For example, to empty our pets collection, we would type: db.zoo.remove({})
# 
# Additionally, to remove a collection all together, we would use db.zoo.drop()
# 
# And to remove the test database, we will use this line of code: db.dropDatabase().
