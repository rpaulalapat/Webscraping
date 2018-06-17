# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():

    # Find data
    mars_info = mongo.db.mars_info.find_one()

    # return template and data
    return render_template("index.html", mars_info=mars_info)


# Route that will trigger scrape functions
@app.route("/scrape")
def scraper():

    # Run scraped functions
    mars_scraped_data = scrape_mars.scrape()

    mars_info = mongo.db.mars_info
    mars_scraped_data = scrape_mars.scrape()
    # update mongodb
    mars_info.update(
        {},
        mars_scraped_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)
    

if __name__ == "__main__":
    app.run(debug=True)
