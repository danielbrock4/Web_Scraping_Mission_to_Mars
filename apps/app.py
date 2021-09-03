# Use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, url_for, redirect
# Use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
# Use the scraping code, we will convert from Jupyter notebook to Python
import scraping

# Set Up Flask
    # To define our Flask app we will create a Flask application called "app."
app = Flask(__name__)

# Connect to Mongo using PyMongo
    # Use flask_pymongo to set up mongo connection
        # app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL
        # "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create the Main Route
    # Step 1: Define the main HTML page everyone will view when visiting the web app
    # Step 2: mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script. We will also assign that path to themars variable for use later.
    # Step 3: return render_template("index.html" tells Flask to return an HTML template using an index.html file: We'll create this file after we build the Flask routes.
    # Step 4: , mars=mars) tells Python to use the "mars" collection in MongoDB
    
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)  
        
# Set up our scraping route
    # Step 1: @app.route(“/scrape”) defines the route that Flask will be using.
    # Step 2:  The next lines allow us to access the database, scrape new data using our scraping.py script, update the database, and return a message when successful. 
    # Step 3: Define it with def scrape():
    # Step 4: Assign a new variable that points to our Mongo database: mars = mongo.db.mars
    # Step 5: we created a new variable to hold the newly scraped data: mars_data = scraping.scrape_all(). In this line, we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook.
    # Step 6: update the database using .update(query_parameter, data, options)
        # 6a. We're inserting data, so first we'll need to add an empty JSON object with {} in place of the query_parameter.
        # 6b. Use the data we have stored in mars_data.
        # 6c. the option we'll include is upsert=True. This indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved (even if we haven't already created a document for it).
    # Step 7: Add a redirect after successfully scraping the data: return redirect('/', code=302). This will navigate our page back to / where we can see the updated content.
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)  


if __name__ == "__main__":
   app.run()