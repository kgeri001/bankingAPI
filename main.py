from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from faker import Faker
import json

app = FastAPI()
fake = Faker()

persons_db = [
    {"name": "Alice", "age": 30, "balance": 5000, "bban" : "TZIR92411578156593"},
    {"name": "Bob", "age": 25, "balance": 3000, "bban" : "MYNB48764759382421"}
]

with open("db.json", "r") as output:
    db_data = json.loads(output.read())

for idx in range(len(db_data)):
    persons_db.append(
        db_data[idx]
    )

# Pydantic Model for Data Validation
class Person(BaseModel):
    name: str
    age: int
    balance: float
    bban: str

# 1. Get all persons
@app.get("/persons", response_model=List[Person])
def get_all_persons():
    return persons_db

# 2. Search for a person by name AND BBAN
@app.get("/persons/{name}/{bban}", response_model=Person)
def get_person(name: str, bban: str):
    for person in persons_db:
        if person["name"].lower() == name.lower() and person["bban"] == bban:
            return person
    raise HTTPException(status_code=404, detail="Person not found")

# 3. Delete a person by name AND BBAN
@app.delete("/persons/{name}/{bban}")
def delete_person(name: str, bban: str):
    global persons_db
    new_db = [p for p in persons_db if not (p["name"].lower() == name.lower() and p["bban"] == bban)]
    
    if len(new_db) == len(persons_db):  # No change means person was not found
        raise HTTPException(status_code=404, detail="Person not found")
    
    persons_db = new_db
    return {"message": f"Person {name} with BBAN {bban} deleted successfully"}

# 4. Add a new person (Prevent duplicate name + BBAN)
@app.post("/persons", response_model=Person)
def add_person(person: Person):
    # Check if name & BBAN already exist
    for existing_person in persons_db:
        if existing_person["name"].lower() == person.name.lower() and existing_person["bban"] == person.bban:
            raise HTTPException(status_code=400, detail="A person with this name and BBAN already exists")

    persons_db.append(person.dict())
    return person

# 5. Update a person's details by name AND BBAN
@app.put("/persons/{name}/{bban}", response_model=Person)
def update_person(name: str, bban: str, updated_person: Person):
    for person in persons_db:
        if person["name"].lower() == name.lower() and person["bban"] == bban:
            person.update(updated_person.dict())
            return person
    raise HTTPException(status_code=404, detail="Person not found")