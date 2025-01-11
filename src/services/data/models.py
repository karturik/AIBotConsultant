from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl, validator, Field

class ProductImage(BaseModel):
    url: HttpUrl
    alt_text: Optional[str] = None

class ProductCharacteristic(BaseModel):
    name: str
    value: str

class ProductOffer(BaseModel):
    id: int = Field(..., alias="ID")
    name: str = Field(..., alias="NAME")
    category: str = Field(..., alias="CATEGORY")
    all_categories: List[str] = Field(..., alias="CATEGORY_ALL")
    price: float = Field(..., alias="PRICE")
    full_price: float = Field(..., alias="PRICE_FULL")
    brand: str = Field(..., alias="BRAND")
    remind_status: str = Field(..., alias="STATUS_REMIND_ITEM")
    url: HttpUrl = Field(...)


class Product(BaseModel):
    id: int
    name: str
    description: str
    images: List[ProductImage]
    characteristics: List[ProductCharacteristic]
    offers: List[ProductOffer]
    reviews: List[Dict[str, Any]] #  Словарь для отзывов
    videos: List[HttpUrl]
    instructions: Optional[HttpUrl] = None
    availability: Dict[str, Dict[str, Any]]  #  Словарь для наличия

    @validator('offers', pre=True)
    def parse_offers(cls, value):
        if isinstance(value, dict):
            return [v for k, v in value.items()]  # извлекаем значения словаря в список
        return value
