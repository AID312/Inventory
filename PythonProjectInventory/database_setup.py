from flask import Flask
from config import Config
from models import db, InventoryItem
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def create_database():
    with app.app_context():
        db.create_all()
        print("Database created successfully!")

def import_data_from_excel():
    try:
        df = pd.read_excel('InventoryDB.xlsx')
        print("Excel file read successfully.")
        print("Columns in the Excel file:", df.columns)
        print(df.head())
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    with app.app_context():
        for _, row in df.iterrows():
            try:
                item = InventoryItem(
                    item_name=row['inventory item name'],
                    type=row['inventory type'],
                    status=row['inventory status']
                )
                db.session.add(item) #pentru verificari
                print(f"Imported: {item.item_name}, {item.type}, {item.status}")
            except Exception as e:
                print(f"Error importing row: {e}")
        db.session.commit()
        print("Data imported successfully!")

def print_database_contents():  #pentru verificari
    with app.app_context():
        items = InventoryItem.query.all()
        for item in items:
            print(f"ID: {item.id}, Name: {item.item_name}, Type: {item.type}, Status: {item.status}")

if __name__ == "__main__":
    create_database()
    import_data_from_excel()
    print_database_contents()
