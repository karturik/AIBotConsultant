from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
from sqlalchemy import Integer
from typing import List, Optional
from .models import Product, ProductOffer, ProductImage, ProductCharacteristic
from db.relational.models import Base, DBProduct, DBProductCharacteristic, DBProductOffer


class ProductDBManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        with Session(self.engine) as session:
            db_product = session.query(DBProduct).filter(DBProduct.id == product_id).first()
            if db_product:
                return self._convert_to_product_model(db_product)
            return None
            
    def search_products_by_name(self, name_query: str) -> List[Product]:
        with Session(self.engine) as session:
            db_products = session.query(DBProduct).filter(
                DBProduct.name.ilike(f'%{name_query}%')
            ).all()
            return [self._convert_to_product_model(p) for p in db_products]
    
    def filter_products_by_characteristics(
        self, 
        characteristics: List[ProductCharacteristic]
    ) -> List[Product]:
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
            return [self._convert_to_product_model(p) for p in db_products]
    
    def filter_products_by_category(self, category: str) -> List[Product]:
        with Session(self.engine) as session:
            query = select(DBProduct).join(DBProduct.offers).filter(
                DBProductOffer.category == category
            ).distinct()
            
            db_products = session.execute(query).scalars().all()
            return [self._convert_to_product_model(p) for p in db_products]

    def filter_products_with_discount(self) -> List[Product]:
        with Session(self.engine) as session:
            query = select(DBProduct).join(DBProduct.offers).filter(
                DBProductOffer.price < DBProductOffer.full_price
            ).distinct()
            
            db_products = session.execute(query).scalars().all()
            return [self._convert_to_product_model(p) for p in db_products]

    def filter_products_by_brand(self, brand: str) -> List[Product]:
        with Session(self.engine) as session:
            query = select(DBProduct).join(DBProduct.offers).filter(
                DBProductOffer.brand == brand
            ).distinct()
            
            db_products = session.execute(query).scalars().all()
            return [self._convert_to_product_model(p) for p in db_products]

    def filter_products_by_availability(self, store_id: str, min_quantity: int = 1) -> List[Product]:
        with Session(self.engine) as session:
            query = select(DBProduct).filter(
                # Проверяем, что в словаре availability для данного магазина
                # количество товара больше или равно минимальному
                DBProduct.availability[store_id]['quantity'].astext.cast(Integer) >= min_quantity
            )
            
            db_products = session.execute(query).scalars().all()
            return [self._convert_to_product_model(p) for p in db_products]
    
    def _convert_to_product_model(self, db_product: DBProduct) -> Product:
        return Product(
            id=db_product.id,
            name=db_product.name,
            description=db_product.description,
            images=[
                ProductImage(url=img.url, alt_text=img.alt_text) 
                for img in db_product.images
            ],
            characteristics=[
                ProductCharacteristic(name=char.name, value=char.value)
                for char in db_product.characteristics    
            ],
            offers=[
                ProductOffer(
                    ID=offer.id,
                    NAME=offer.name,
                    CATEGORY=offer.category,
                    CATEGORY_ALL=offer.all_categories,
                    PRICE=offer.price,
                    PRICE_FULL=offer.full_price,
                    BRAND=offer.brand,
                    STATUS_REMIND_ITEM=offer.remind_status,
                    url=offer.url
                )
                for offer in db_product.offers
            ],
            reviews=db_product.reviews,
            videos=db_product.videos,
            instructions=db_product.instructions,
            availability=db_product.availability
        )
