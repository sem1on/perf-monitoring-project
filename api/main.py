"""
CRUD API для нагрузочного тестирования
FastAPI + in-memory хранилище
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import time

# =============================================
# Модели данных
# =============================================

class ItemBase(BaseModel):
    """Базовая модель товара"""
    name: str = Field(..., min_length=1, max_length=100, example="Gaming Laptop")
    price: float = Field(..., gt=0, le=1000000, example=1299.99)

class ItemCreate(ItemBase):
    """Модель для создания товара"""
    pass

class ItemUpdate(BaseModel):
    """Модель для обновления товара"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0, le=1000000)

class Item(ItemBase):
    """Модель товара с ID"""
    id: int
    created_at: float = Field(default_factory=time.time)

# =============================================
# Создание FastAPI приложения
# =============================================

app = FastAPI(
    title="Performance Monitoring API",
    description="API для нагрузочного тестирования с k6",
    version="1.0.0"
)

# Добавляем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================
# In-memory хранилище
# =============================================

items_db = []
next_id = 1

# =============================================
# CRUD эндпоинты
# =============================================

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"message": "Performance Monitoring API", "docs": "/docs"}

@app.get("/items", response_model=List[Item])
async def get_items():
    """Получить все товары"""
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Получить товар по ID"""
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """Создать новый товар"""
    global next_id
    
    new_item = Item(
        id=next_id,
        name=item.name,
        price=item.price
    )
    items_db.append(new_item)
    next_id += 1
    
    return new_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemUpdate):
    """Обновить товар"""
    for i, existing in enumerate(items_db):
        if existing.id == item_id:
            if item_update.name is not None:
                existing.name = item_update.name
            if item_update.price is not None:
                existing.price = item_update.price
            return existing
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """Удалить товар"""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(i)
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )

@app.get("/stats")
async def get_stats():
    """Получить статистику"""
    if not items_db:
        return {"total": 0, "avg_price": 0, "min_price": 0, "max_price": 0}
    
    prices = [item.price for item in items_db]
    return {
        "total": len(items_db),
        "avg_price": sum(prices) / len(prices),
        "min_price": min(prices),
        "max_price": max(prices)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    