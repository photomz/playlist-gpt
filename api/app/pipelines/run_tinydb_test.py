from tinydb import TinyDB
from dataclasses import dataclass, asdict

db = TinyDB('database.json')  # Create a TinyDB instance and specify the database file
table = db.table('items')  # Create a table called 'items' in the database


@dataclass
class Item:
    name: str
    price: float


if __name__ == "__main__":
    item1 = Item("Hexagonal", 10.99)
    item2 = Item("Surprise", 19.99)

    # Insert items into the table
    a = table.insert(asdict(item1))
    b = table.insert(asdict(item2))

    # Assert that the retrieved items match the inserted items
    assert asdict(item1) == table.get(doc_id=a)
    assert asdict(item2) == table.get(doc_id=b)

    # Update item1
    updated_item1 = Item("Hexagonal Updated", 12.99)
    table.update(asdict(updated_item1), doc_ids=[a])
    assert asdict(updated_item1) == table.get(doc_id=a)

    # Delete item2
    table.remove(doc_ids=[b])
    assert table.get(doc_id=b) is None

    # Batch get all items
    all_items = [Item(item['name'], item['price']) for item in table.all()]
    all_items_dicts = [asdict(item) for item in all_items]
    print(all_items_dicts)
