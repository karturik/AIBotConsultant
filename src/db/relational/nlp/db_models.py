from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, Table, Index
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association tables for many-to-many relationships
product_images = Table(
    'product_images',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('image_id', Integer, ForeignKey('images.id'), primary_key=True)
)

product_characteristics = Table(
    'product_characteristics', 
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('characteristic_id', Integer, ForeignKey('characteristics.id'), primary_key=True)
)


class DBProduct(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String, nullable=False)
    reviews = Column(JSON)  # Stores product reviews as JSON
    shops_availability = Column(JSON)  # Stores availability data as JSON
    product_id = Column(Integer, nullable=True)
    category = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    full_price = Column(Float, nullable=False)
    brand = Column(String(100), nullable=False, index=True)
    remind_status = Column(String(50))
    url = Column(String, nullable=False)
    additional_info = Column(String, nullable=True)  
    
    # Relationships
    images = relationship("DBProductImage", secondary=product_images, back_populates="products")
    characteristics = relationship("DBProductCharacteristic", secondary=product_characteristics, back_populates="products")

    # Create indexes
    __table_args__ = (
        Index('ix_products_name_category', 'name', 'category'),
        Index('ix_products_brand_price', 'brand', 'price'),
    )

class DBProductImage(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    alt_text = Column(String)
    
    # Relationship
    products = relationship("DBProduct", secondary=product_images, back_populates="images")

class DBProductCharacteristic(Base):
    __tablename__ = 'characteristics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    value = Column(String(255), nullable=False)
    
    # Relationship
    products = relationship("DBProduct", secondary=product_characteristics, back_populates="characteristics")

    # Create index for characteristics
    __table_args__ = (
        Index('ix_characteristics_name_value', 'name', 'value'),
    )

def init_db(engine):
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
