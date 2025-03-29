from pydantic import BaseModel, Field 
from typing import List,Optional 
from uuid import uuid4

class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    author: str
    description: str
    price: float
    sole_buyer: bool
    labels: List[str]
    image_url: str
    likes: int = 0
    ratings: List[int] = []
    avg_rating: float = 0.0
    
    @property
    def avg_rating(self) -> float:
        return round(sum(self.ratings) / len(self.ratings), 2) if self.ratings else 0.0

class LikeRequest(BaseModel):
    user_id: str
    item_id: str

class RatingRequest(BaseModel):
    user_id: str
    item_id: str
    rating: int = Field(..., ge=1, le=5)