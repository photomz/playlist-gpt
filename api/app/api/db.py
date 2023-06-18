from app.services.db import table
from fastapi import APIRouter, HTTPException

router = APIRouter()

# @router.post("/")
# def create(item: Playlist):
#     """
#     Create a new item in the database.
#     """
#     item_dict = asdict(item)
#     item_id = table.insert(item_dict)
#     return {"id": item_id, "item": item_dict}

@router.get("/all")
def get_all():
    """
    Retrieve all items from the database.
    """
    return table.all()

@router.get("/{item_id}")
def get(item_id: int):
    """
    Retrieve an item from the database by its ID.
    """
    item = table.get(doc_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "item": item}


# @router.put("/{item_id}")
# def update(item_id: int, item: Playlist):
#     """
#     Update an item in the database by its ID.
#     """
#     existing_item = table.get(doc_id=item_id)
#     if existing_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     updated_item = {**dict(item), 'id': item_id} # type: ignore
#     table.update(updated_item, doc_ids=[item_id])
#     return {"id": item_id, "item": updated_item}


# @router.delete("/{item_id}")
# def delete(item_id: int):
#     """
#     Delete an item from the database by its ID.
#     """
#     existing_item = table.get(doc_id=item_id)
#     if existing_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     table.remove(doc_ids=[item_id])
#     return {"message": "Item deleted"}