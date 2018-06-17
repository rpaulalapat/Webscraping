# import necessary libraries
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection  available to remove duplicates
db.mars_info.drop()

# Creates a collection in the database and insert new scraped data
mars_scraped_data = scrape_mars.scrape()
db.mars_info.insert(mars_scraped_data)

# Route that will trigger scrape functions
@app.route("/scrape")
def scraper():

    # Run scraped functions
    mars_scraped_data = scrape_mars.scrape()
    mars_info = db.mars_info
    
    # update mongodb
    mars_info.update(
        {},
        mars_scraped_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():

    # Find data
    mars_info = db.mars_info.find_one()

    # return template and data
    return render_template("index.html", mars_info=mars_info)
    

if __name__ == "__main__":
    app.run(debug=True)
