from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl, Field

# class ProductImage(BaseModel):
#     url: HttpUrl
#     alt_text: Optional[str] = None

# class ProductCharacteristic(BaseModel):
#     name: str
#     value: str

# class Product(BaseModel):
#     id: int
#     name: str
#     description: str
#     category: str
#     all_categories: List[str]
#     brand: str
#     images: List[ProductImage]
#     characteristics: List[ProductCharacteristic]
#     reviews: List[Dict[str, Any]]  # [{"rating": 5, "comment": "Отличный телефон"}]
#     instructions: Optional[HttpUrl] = None
#     availability: Dict[str, Dict[str, Any]]  # {"store1": {"available": True, ...}}
#     configurations: List[str]  # Список конфигураций
#     url: HttpUrl
#     price: Optional[float]
#     full_price: Optional[float]

class NLPChatRequest(BaseModel):
    source: str
    messages: Optional[List[str]]