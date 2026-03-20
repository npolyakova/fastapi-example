from fastapi import APIRouter, Query
from pathlib import Path
import json

router = APIRouter(prefix="/products", tags=["Furniture"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FILE = BASE_DIR / "data" / "furniture.json"


def read_data():
    if not DATA_FILE.exists():
        return {"items": []}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def write_data(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


@router.get("/")
async def get_furniture(
    sorting: str | None = Query(default=None),
    furniture_type: str | None = Query(default=None)
):
    data = read_data()
    items = data.get("items", [])

    if furniture_type:
        items = [
            item for item in items
            if item.get("type", "").lower() == furniture_type.lower()
        ]

    if sorting == "asc":
        items = sorted(items, key=lambda x: x.get("name", "").lower())
    elif sorting == "desc":
        items = sorted(items, key=lambda x: x.get("name", "").lower(), reverse=True)

    return {
        "items": items,
        "total": len(items)
    }


@router.post("/")
async def create_furniture(item: dict):
    data = read_data()
    items = data.get("items", [])

    new_id = 1
    if items:
        new_id = max(x.get("id", 0) for x in items) + 1

    item["id"] = new_id
    items.append(item)
    data["items"] = items
    write_data(data)

    return {
        "message": "Объект создан",
        "item": item
    }