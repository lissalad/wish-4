from flask import Flask, render_template, request, redirect, url_for, flash
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
app.secret_key = '3' 

# ----------- PAGES ----------------------------------------- #
@app.route('/')
def wish4_index():
    return render_template('index.html')

@app.route('/wishlists')
def wishlists():
    return render_template('wishlists.html', lists=lists.find().sort([['_id',-1]]))

@app.route('/wishlists/new')
def wishlists_new():
    return render_template('wishlists_new.html')

@app.route('/wishlists/<wishlist_id>')
def wishlists_show(wishlist_id):
  wishlist = lists.find_one({'_id':ObjectId(wishlist_id)})
  wishlist_items = items.find({'wishlist_id':wishlist_id})

  return render_template('wishlist.html', wishlist=wishlist, items=wishlist_items)

@app.route('/wishlists/<wishlist_id>/add-item')
def add_item(wishlist_id):
  return render_template('add_item.html', wishlist_id=wishlist_id)

@app.route('/wishlists/<wishlist_id>/edit')
def edit_wishlist(wishlist_id):
    wishlist = lists.find_one({'_id':ObjectId(wishlist_id)})
    return render_template('wishlist_edit.html', wishlist=wishlist)

@app.route('/wishlists/<item_id>/edit-item')
def edit_item(item_id):
    item = items.find_one({'_id':ObjectId(item_id)})
    wishlist = lists.find_one({'_id':item['wishlist_id']})
    return render_template('item_edit.html', item=item,wishlist=wishlist)


# ----------- WISHLIST --------------------------------- #
@app.route('/wishlists', methods=['POST'])
def wishlist_create():
  wishlist = {
    'title': request.form.get('title'),
    'description': request.form.get('description')
    }
  lists.insert_one(wishlist)
  # test=  lists.insert_one(wishlist)
  # print(test)
  flash("Created Wishlist")
  return redirect(url_for('wishlists_show', wishlist_id=wishlist['_id']))

@app.route('/wishlists/<wishlist_id>/delete')
def wishlist_delete(wishlist_id):
  lists.delete_one({'_id': ObjectId(wishlist_id)}) 
  flash("Wishlist Deleted") 
  return redirect(url_for('wishlists'))

@app.route('/wishlists/<wishlist_id>', methods=['POST'])
def wishlist_update(wishlist_id):
  updated = {
  'title': request.form.get('title'),
  'description': request.form.get('description')
  }
  lists.update_one({'_id':ObjectId(wishlist_id)}, {'$set': updated})
  flash("Updated List")
  return redirect(url_for('wishlists_show', wishlist_id=wishlist_id))

# ----------- ITEM --------------------------------- #
@app.route('/wishlists/<wishlist_id>/add-item', methods=["POST"])
def item_create(wishlist_id):
  item={
    'wishlist_id': wishlist_id,
    'title': request.form.get('title'),
    'comment':request.form.get('comment'),
    'link':request.form.get('link'),
    'img_address':request.form.get('img_address')
  }
  if item['img_address'] == '':
    item['img_address'] = '/static/images/gifts.png'
  # if item['link'] == '':
    # item['link'] = 'https://www.google.com/search?q=no+link&oq=no+link&aqs=chrome..69i57j0i512l9.1218j0j4&sourceid=chrome&ie=UTF-8'
  items.insert_one(item)
  print(f"\n {item['wishlist_id']} \n")
  print('yes!!!!!')
  flash("Added Item")
  return redirect(url_for('wishlists_show', wishlist_id=item['wishlist_id']))
  #wishlist_id=item["wishlist_id"]))

@app.route('/wishlists/<item_id>', methods=['POST'])
def item_update(item_id):
  item = items.find_one({'_id':ObjectId(item_id)})
  updated={
  'wishlist_id': item['wishlist_id'],
  'title': request.form.get('title'),
  'comment':request.form.get('comment'),
  'link':request.form.get('link'),
  'img_address':request.form.get('img_address')
}
  if updated['img_address'] == '':
    updated['img_address'] = '/static/images/gifts.png'
  if updated['link'] == '':
    updated['link'] = 'https://www.google.com/search?q=no+link&oq=no+link&aqs=chrome..69i57j0i512l9.1218j0j4&sourceid=chrome&ie=UTF-8'
  items.update_one(
    {'_id':ObjectId(item_id)},
    {'$set': updated})
  flash("Updated Item")
  return redirect(url_for('wishlists_show', wishlist_id=item['wishlist_id']))
 


@app.route('/wishlists/<item_id>/delete', methods=['POST'])
def item_delete(item_id):
  item = items.find_one({'_id':ObjectId(item_id)})
  items.delete_one({'_id': ObjectId(item_id)})  
  flash("Item Deleted")
  return redirect(url_for('wishlists_show', wishlist_id=item['wishlist_id']))


# ----------- RUN ----------------------------------------------------- #
if __name__ == '__main__':
    app.run(debug=True)    
