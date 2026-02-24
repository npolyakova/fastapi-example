from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter(prefix="/products", tags=["products"])

DATA_FILE = "menu_data.json"

initial_menu = [
    {
        "id": 1,
        "name": "Борщ",
        "category": "супы",
        "price": 350,
        "weight": 300
    },
    {
        "id": 2,
        "name": "Паста Карбонара",
        "category": "горячее",
        "price": 450,
        "weight": 350
    },
    {
        "id": 3,
        "name": "Чизкейк",
        "category": "десерты",
        "price": 300,
        "weight": 150
    },
    {
        "id": 4,
        "name": "Цезарь с курицей",
        "category": "салаты",
        "price": 380,
        "weight": 250
    },
    {
        "id": 5,
        "name": "Греческий салат",
        "category": "салаты",
        "price": 320,
        "weight": 280
    }
]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        save_data(initial_menu)
        return initial_menu

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

menu_items = load_data()

@router.get("/")
async def get_menu(sorting: str = None):
    if sorting == "asc":
        return sorted(menu_items, key=lambda x: x["name"])
    elif sorting == "desc":
        return sorted(menu_items, key=lambda x: x["name"], reverse=True)
    return {
        "items": menu_items,
        "total": len(menu_items)
    }

@router.get("/category/{category_name}")
async def get_items_by_category(category_name: str):
    result = [item for item in menu_items if item["category"].lower() == category_name.lower()]
    if result:
        return {
            "category": category_name,
            "items": result,
            "count": len(result)
        }
    return {"message": f"В категории '{category_name}' ничего не найдено"}

@router.get("/{item_id}")
async def get_item(item_id: int):
    for item in menu_items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Блюдо не найдено")

@router.post("/")
async def create_item(name: str, category: str, price: int, weight: int):
    new_id = max([item["id"] for item in menu_items] + [0]) + 1
    new_item = {
        "id": new_id,
        "name": name,
        "category": category,
        "price": price,
        "weight": weight
    }
    menu_items.append(new_item)
    save_data(menu_items) 
    return new_item

@router.put("/{item_id}")
async def update_item(item_id: int, name: str = None, category: str = None, 
                      price: int = None, weight: int = None):
    for item in menu_items:
        if item["id"] == item_id:
            if name: item["name"] = name
            if category: item["category"] = category
            if price: item["price"] = price
            if weight: item["weight"] = weight
            save_data(menu_items) 
            return item
    raise HTTPException(status_code=404, detail="Блюдо не найдено")

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    for i, item in enumerate(menu_items):
        if item["id"] == item_id:
            deleted = menu_items.pop(i)
            save_data(menu_items)  
            return {"message": f"Блюдо '{deleted['name']}' удалено", "deleted_item": deleted}
    raise HTTPException(status_code=404, detail="Блюдо не найдено")