from tinydb import TinyDB
from app.helpers.types import Playlist
from fastapi import APIRouter, HTTPException

db = TinyDB('bin/database.json')  # Create a TinyDB instance and specify the database file
table = db.table('playlists')

router = APIRouter()

@router.post("/items")
def create_item(item: Playlist):
    """
    Create a new item in the database.
    """
    item_dict = asdict(item)
    item_id = table.insert(item_dict)
    return {"id": item_id, "item": item_dict}


@router.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    Retrieve an item from the database by its ID.
    """
    item = table.get(doc_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "item": item}


@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Playlist):
    """
    Update an item in the database by its ID.
    """
    existing_item = table.get(doc_id=item_id)
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = {**item.dict(), 'id': item_id}
    table.update(updated_item, doc_ids=[item_id])
    return {"id": item_id, "item": updated_item}


@router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """
    Delete an item from the database by its ID.
    """
    existing_item = table.get(doc_id=item_id)
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    table.remove(doc_ids=[item_id])
    return {"message": "Item deleted"}


@router.get("/items")
async def read_all_items():
    """
    Retrieve all items from the database.
    """
    items = table.all()
    return {"items": items}