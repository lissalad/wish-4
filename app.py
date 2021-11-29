from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import certifi

host = os.environ.get("DB_URL")
client = MongoClient(host, tlsCAFile=certifi.where())
db = client.wish4
lists = db.lists
items = db.items

app = Flask(__name__)

# ----------- PAGES ----------------------------------------- #
@app.route('/')
def wish4_index():
    return render_template('index.html')

@app.route('/wishlists')
def wishlists():
    return render_template('wishlists.html', lists=lists.find())

@app.route('/wishlists/new')
def wishlists_new():
    return render_template('wishlists_new.html')

@app.route('/wishlists/<wishlist_id>')
def wishlists_show(wishlist_id):
  wishlist = lists.find_one({'_id':ObjectId(wishlist_id)})
  return render_template('wishlists_view.html', wishlist=wishlist)


# ----------- CREATE WISHLIST --------------------------------- #
@app.route('/wishlists', methods=['POST'])
def wishlist_create():
  wishlist = {
    'title': request.form.get('title'),
    'description': request.form.get('description')
    }
  lists.insert_one(wishlist)
  return redirect(url_for('wish4_index'))


# ----------- RUN ----------------------------------------------------- #
if __name__ == '__main__':
    app.run(debug=True)                          
