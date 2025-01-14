from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
from sqlalchemy import Integer
from typing import List, Optional, Any
# from services.database.nlp.models import Product, ProductOffer, ProductImage, ProductCharacteristic
from db.relational.nlp.db_models import Base, DBProduct, DBProductCharacteristic, DBProductOffer


class ProductDBManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        
    def get_product_by_id(self, product_id: int) -> Optional[DBProduct]:
        with Session(self.engine) as session:
            db_product = session.query(DBProduct).filter(DBProduct.id == product_id).first()
            if db_product:
                return db_product
            return None
            
    def search_products_by_name(self, name_query: str) -> List[Optional[DBProduct]]:
        with Session(self.engine) as session:
            db_products = session.query(DBProduct).filter(
                DBProduct.name.ilike(f'%{name_query}%')
            ).all()
            return db_products
    
    def filter_products_by_characteristics(
        self, 
        characteristics: List[Any]
    ) -> List[DBProduct]:
        with Session(self.engine) as session:
            query = select(DBProduct).join(DBProduct.characteristics)
            
            filters = []
            for char in characteristics:
                filters.append(
                    and_(
                        DBProductCharacteristic.name == char.name,
                        DBProductCharacteristic.value == char.value
                    )
                )
                
            if filters:
                query = query.filter(and_(*filters))
                
            db_products = session.execute(query).scalars().all()
            return db_products
    
    def filter_products_by_category(self, category: str) -> List[Optional[DBProduct]]:
        with Session(self.engine) as session:
            query = select(DBProduct).filter(
                DBProduct.category == category
            ).distinct()
            
            db_products = session.execute(query).scalars().all()
            return db_products

    def filter_products_with_discount(self) -> List[Optional[DBProduct]]:
        with Session(self.engine) as session:
            query = select(DBProduct).filter(
                DBProduct.price < DBProduct.full_price
            ).distinct()
            
            db_products = session.execute(query).scalars().all()
            return db_products

    def filter_products_by_brand(self, brand: str) -> List[Optional[DBProduct]]:
        with Session(self.engine) as session:
            query = select(DBProduct).filter(
                DBProduct.brand == brand
            ).distinct()
            
            db_products = session.execute(query).scalars().all()
            return db_products

    def filter_products_by_availability(self, store_id: str, min_quantity: int = 1) -> List[Optional[DBProduct]]:
        with Session(self.engine) as session:
            query = select(DBProduct).filter(
                # Проверяем, что в словаре availability для данного магазина
                # количество товара больше или равно минимальному
                DBProduct.availability[store_id]['quantity'].astext.cast(Integer) >= min_quantity
            )
            
            db_products = session.execute(query).scalars().all()
            return db_products
        