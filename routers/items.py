from typing import Optional,List
from models.items import Item,RatingRequest,LikeRequest
from fastapi import Query,APIRouter
from fastapi import HTTPException

router = APIRouter()

# Sample in-memory storage
db_items = []
db_likes = {}
db_ratings = {}

@router.post("/items/", response_model=Item)
def create_item(item: Item):
    db_items.append(item)
    return item

@router.get("/items/", response_model=List[Item])
def get_items(sort_by: Optional[str] = Query("likes", regex="^(likes|price|author)$")):
    sorted_items = sorted(db_items, key=lambda x: getattr(x, sort_by), reverse=True)
    return sorted_items

@router.get("/items/search/", response_model=List[Item])
def search_items(
    query: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    sole_buyer: Optional[bool] = None,
):
    filtered_items = db_items

    # Filter by query (title or labels)
    print(query)
    if query:
        filtered_items = [
            item for item in filtered_items
            if query.lower() in item.title.lower() or query.lower() in item.labels
        ]

    # Filter by price range
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.price >= min_price]

    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.price <= max_price]

    # Filter by minimum rating
    if min_rating is not None:
        filtered_items = [item for item in filtered_items if item.avg_rating >= min_rating]

    # Filter by sole_buyer (one-time buy)
    if sole_buyer is not None:
        filtered_items = [item for item in filtered_items if item.sole_buyer == sole_buyer]

    return filtered_items

@router.get("/items/{item_id}",response_model=Item)
def get_item_by_id(item_id:str):
    for item in db_items:
        if item.id == item_id:
            return item 
    raise HTTPException(status_code=404,detail=f"Item with id {item_id} not found." )
        
@router.post("/items/like/")
def like_item(like: LikeRequest):
    if like.item_id not in db_likes:
        db_likes[like.item_id] = set()
    db_likes[like.item_id].add(like.user_id)
    for item in db_items:
        if item.id == like.item_id:
            item.likes = len(db_likes[like.item_id])
    return {"message": "Item liked successfully"}

@router.post("/items/rate/")
def rate_item(rating: RatingRequest):
    if rating.item_id not in db_ratings:
        db_ratings[rating.item_id] = {}
    db_ratings[rating.item_id][rating.user_id] = rating.rating
    for item in db_items:
        if item.id == rating.item_id:
            item.ratings = list(db_ratings[rating.item_id].values())
            item.avg_rating = sum(item.ratings) / len(item.ratings)
    return {"message": "Item rated successfully"}

@router.get("/user/{user_id}/likes", response_model=List[Item])
def get_user_liked_items(user_id: str):
    liked_items = [item for item in db_items if item.id in db_likes and user_id in db_likes[item.id]]
    return liked_items
