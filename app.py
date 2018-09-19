from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scarpe_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    scrape_mars = mongo.db.collection.find_one()
    return render_template("index.html", scrape_mars=scrape_mars)


@app.route("/scrape")
def scraper():

    mars_info = mongo.db.collection
    mars_data = scarpe_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)
    # Run scraped functions
   # mars = scarpe_mars.scrape()

    # Store results into a dictionary
    #scrape_mars = {
  #      "news_title": mars["news_title"],
  #      "news_p": mars["news_p"],
  #      "featured_image_url": mars["featured_image_url"],
  #      "mars_weather": mars["mars_weather"]
  #  }
    #"html_table": mars["html_table"]
    # "hemisphere_image_urls": mars["hemisphere_image_urls"]
    # Insert forecast into database
  #  mongo.db.collection.insert_one(scarpe_mars)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
