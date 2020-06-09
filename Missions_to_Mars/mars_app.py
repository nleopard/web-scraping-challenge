from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create route that renders index.html template and finds data from mongo
@app.route("/")
def home(): 

    # Find data
    mars_facts = mongo.db.mars_facts.find_one()

    # Return template and data
    return render_template("index.html", mars_facts_data=mars_facts)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars_facts = mongo.db.mars_facts

    # Run the scrape function
    mars_facts_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_facts.update({}, mars_facts_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
