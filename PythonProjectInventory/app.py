from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, InventoryItem

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = InventoryItem.query.all()
    #pentru verificari
    for item in items:
        print(f"ID: {item.id}, Name: {item.item_name}, Type: {item.type}, Status: {item.status}")
    return render_template('index.html', items=items)

@app.route('/book_item/<int:item_id>', methods=['POST'])
def book_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    action = request.form['action']
    if action == 'book' and item.status == 'Free':
        item.status = 'In use'
    elif action == 'unbook' and item.status == 'In use':
        item.status = 'Free'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    inventory_items = InventoryItem.query.all()
    return render_template('admin.html', items=inventory_items)

@app.route('/edit_item/<int:item_id>', methods=['POST'])
def edit_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    item.item_name = request.form['item_name']
    item.type = request.form['type']
    item.status = request.form['status']
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)