import json
import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["products"])

# Путь к базе данных
JSON_PATH = "products.json"

# Модель данных
class OfficeProduct(BaseModel):
    name: str
    product_type: str
    price: float
    manufacturer: str

# Функции для работы с файлом
def load_products() -> List[dict]:
    if not os.path.exists(JSON_PATH):
        # Если файла нет, создаем его с начальными данными
        initial_data = [
            {"name": "Бумага A4", "product_type": "Канцелярия", "price": 500.0, "manufacturer": "SvetoCopy"},
            {"name": "Ручка синяя", "product_type": "Письменные", "price": 25.0, "manufacturer": "ErichKrause"}
        ]
        save_products(initial_data)
        return initial_data
    
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_products(data: List[dict]):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- Эндпоинты ---

# Получение всех товаров с сортировкой (Задание 4)
@router.get("/")
async def get_products(sorting: Optional[str] = Query(None, pattern="^(asc|desc)$")):
    products = load_products()
    
    if sorting:
        reverse_order = (sorting == "desc")
        # Сортировка по названию (name)
        products.sort(key=lambda x: x["name"].lower(), reverse=reverse_order)
        
    return {
        "products": products,
        "total": len(products),
        "applied_sorting": sorting
    }

# Поиск по производителю
@router.get("/search")
async def search_by_manufacturer(manufacturer: str):
    products = load_products()
    filtered = [p for p in products if p["manufacturer"].lower() == manufacturer.lower()]
    
    if not filtered:
        raise HTTPException(status_code=404, detail="Производитель не найден")
    
    return {"manufacturer": manufacturer, "products": filtered}

# Создание нового товара (Задание 3)
@router.post("/", status_code=201)
async def create_product(product: OfficeProduct):
    products = load_products()
    
    # Превращаем модель в словарь и добавляем в список
    new_product_dict = product.model_dump()
    products.append(new_product_dict)
    
    # Сохраняем обновленный список в JSON
    save_products(products)
    
    return {
        "message": "Товар успешно добавлен в базу",
        "product": new_product_dict
    }