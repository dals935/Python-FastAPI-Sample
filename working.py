from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None
    
class UpdateItem(BaseModel):
    name: Optional[str] = None   
    price: Optional[float] = None
    brand: Optional[str] = None    

app = FastAPI()

# @app.get("/")
# def home():
#     return {"Data": "Testing"}

# @app.get("/about")
# def about():
#     return {"Data": "About"}

inventory = {}

@app.get("/get-by-name")
def get_item(*, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item Name Not Found")


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID Already Exists")
    
    inventory[item_id] = item
    return inventory[item_id]

@app.put("update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID Not Found")
    
    if item.name != None:
        inventory[item_id].name = item.name
        
    if item.price != None:
        inventory[item_id].price = item.price
        
    if item.brand != None:
        inventory[item_id].brand = item.brand
        
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", ge=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID Not Found")
    
    del inventory[item_id]
