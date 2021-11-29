from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import certifi

host = os.environ.get("DB_URL")
client = MongoClient(host, tlsCAFile=certifi.where())
db = client.wish4
playlists = db.wishlists
comments = db.items

app = Flask(__name__)

# ----------- PAGES ----------------------------------------- #
@app.route('/')
def playlists_index():
    return render_template('index.html')


# ----------- RUN ----------------------------------------------------- #
if __name__ == '__main__':
    app.run(debug=True)                          
