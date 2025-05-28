import os
import sys

# Add src directory to Python path
HOME_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
print(HOME_DIR)
sys.path.append(HOME_DIR)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import json
import re
from src.db.relational.nlp.db_models import DBProduct, DBProductImage, DBProductCharacteristic, init_db
from src.db.relational.init_database import SQLALCHEMY_DATABASE_URL

def clean_text(text):
    if pd.isna(text):
        return ""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', str(text))
    # Remove special characters but keep cyrillic and latin
    text = re.sub(r'[^\w\s\-.,;:!?"\'()а-яА-ЯёЁa-zA-Z]', '', text)
    return text.strip()

def clean_json_field(field):
    if pd.isna(field):
        return {}
    if isinstance(field, str):
        try:
            # Try to parse JSON string
            data = json.loads(field)
            # Ensure proper encoding for cyrillic
            return json.loads(json.dumps(data, ensure_ascii=False))
        except json.JSONDecodeError:
            return {}
    return field

def init_database(csv_files):
    # Create engine with proper encoding
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={'client_encoding': 'utf8'}
    )
    
    # Create all tables
    init_db(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        for csv_file in csv_files:
            # Read CSV with proper encoding
            df = pd.read_csv(csv_file, encoding='utf-8')
            
            for _, row in df.iterrows():
                # Clean text fields
                name = clean_text(row['name'])
                description = clean_text(row['description'])
                brand = clean_text(row['brand'])
                remind_status = clean_text(row['remind_status'])
                url = clean_text(row['url'])
                category = clean_text(row['category'])
                
                # Clean and parse JSON fields
                reviews = clean_json_field(row['reviews'])
                shops_availability = clean_json_field(row['shops_availability'])
                
                # Create product
                product = DBProduct(
                    name=name,
                    description=description,
                    reviews=reviews,
                    shops_availability=shops_availability,
                    price=float(row['price']) if pd.notna(row['price']) else 0.0,
                    full_price=float(row['full_price']) if pd.notna(row['full_price']) else 0.0,
                    brand=brand,
                    remind_status=remind_status,
                    url=url,
                    category=category
                )
                
                # Handle images
                if not pd.isna(row['images']):
                    images = clean_json_field(row['images'])
                    if isinstance(images, list):
                        for img in images:
                            if isinstance(img, dict) and 'url' in img:
                                image = DBProductImage(
                                    url=clean_text(img['url']),
                                    alt_text=clean_text(img.get('alt_text', ''))
                                )
                                product.images.append(image)
                
                # Handle characteristics
                if not pd.isna(row['characteristics']):
                    chars = clean_json_field(row['characteristics'])
                    if isinstance(chars, dict):
                        for name, value in chars.items():
                            char = DBProductCharacteristic(
                                name=clean_text(name),
                                value=clean_text(str(value))
                            )
                            product.characteristics.append(char)
                
                session.add(product)
            
            # Commit after each file
            session.commit()
            print(f"Data from {csv_file} imported successfully!")
        
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    
    print("Database initialization completed!")

csv_files = ['src/data_parsing/notebooks.csv', 
             'src/data_parsing/phones.csv', 
             'src/data_parsing/smart_watch.csv', 
             'src/data_parsing/televizory.csv']
init_database(csv_files)