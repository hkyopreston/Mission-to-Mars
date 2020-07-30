# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
from scrape_mars import scrape
import os


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection, for mission to mars db
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


# Route to render index.html template using data from Mongo
@app.route("/")
def home(): 

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data, Flask stuff
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape_results():

    # Run scrape function
    mars_data = scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_data.update({}, mars_data, upsert=True)

    # Back to home page
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)