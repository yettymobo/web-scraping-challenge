from flask import Flask, render_template, redirect
import pymongo

# From the separate python file in this directory, we'll import the code that is used to scrape craigslist
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create variable for our connection string
conn = 'mongodb://localhost:27017'

# Pass connection string to the pymongo instance.
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.news
collection.drop()

@app.route('/')
def home():
    mars = collection.find_one()
    

    return render_template('index.html', mars = mars)

@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()
    collection.insert_one(mars_data)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
