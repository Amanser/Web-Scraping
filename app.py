from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Create an instance of Flask
app = Flask(__name__)


# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_info")
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)



@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)



@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_info = mongo.db.mars_info

    mars_data = scrape_mars.scrape_news()
    mars_data = scrape_mars.scrape_feature()
    mars_data = scrape_mars.scrape_facts()
    mars_data = scrape_mars.scrape_weather()
    # mars_data = scrape_mars.scrape_hemispheres()

    mars_info.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)