from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])

products = [
    {
        "name": "Молоко 3.2%",
        "count": 10,
        "price": 102
    },
    {
        "name": "Молоко 2.5%",
        "count": 13,
        "price": 91
    },
    {
        "name": "Сыр Сливочный 35%",
        "count": 43,
        "price": 298
    },
    {
        "name": "Сыр плавленный с грибами",
        "count": 10,
        "price": 165
    },
    {
        "name": "Сыр чечил",
        "count": 12,
        "price": 100
    },
    {
        "name": "Сметана 10%",
        "count": 30,
        "price": 120
    },
    {
        "name": "Сметана 20%",
        "count": 2,
        "price": 150
    }
]

# Получить список всех продуктов
@router.get("/")
async def get_products():
    return {
        "products": products,
        "total": len(products)
    }
