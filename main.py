from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
from functools import wraps
import datetime
import logging
import json
import inspect
import os

app = FastAPI()

# Ensure the log file exists and is writable
log_file_path = "app.log"

# Configure logging explicitly
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler that writes to 'app.log'
file_handler = logging.FileHandler(log_file_path, mode="a")
file_handler.setLevel(logging.INFO)

# Define the log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Attach the handler to the logger
if not logger.hasHandlers():
    logger.addHandler(file_handler)

# Force logging to flush immediately
file_handler.flush()
os.fsync(file_handler.stream.fileno())

persons_db = [
    {"name": "Alice", "age": 30, "balance": 5000, "bban": "TZIR92411578156593"},
    {"name": "Bob", "age": 25, "balance": 3000, "bban": "MYNB48764759382421"}
]

with open("db.json", "r") as output:
    db_data = json.loads(output.read())

persons_db.extend(db_data)

# Pydantic Model for Data Validation
class Person(BaseModel):
    name: str
    age: int
    balance: float
    bban: str

# Custom decorator to log request time
def log_request_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        if request:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            url = str(request.url)
            log_message = f"GET Request received at {timestamp} - URL: {url}"
            logger.info(log_message)
            
            # Manually flush logs to ensure immediate writing
            file_handler.flush()
            os.fsync(file_handler.stream.fileno())
        
        if inspect.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        return func(*args, **kwargs)
    
    return wrapper

# 1. Get all persons
@app.get("/persons", response_model=List[Person])
@log_request_time
async def get_all_persons(request: Request):
    return persons_db

# 2. Search for a person by name AND BBAN
@app.get("/persons/{name}/{bban}", response_model=Person)
@log_request_time
async def get_person(name: str, bban: str, request: Request):
    for person in persons_db:
        if person["name"].lower() == name.lower() and person["bban"] == bban:
            return person
    raise HTTPException(status_code=404, detail="Person not found")

# 3. Delete a person by name AND BBAN
@app.delete("/persons/{name}/{bban}")
async def delete_person(name: str, bban: str):
    global persons_db
    new_db = [p for p in persons_db if not (p["name"].lower() == name.lower() and p["bban"] == bban)]
    
    if len(new_db) == len(persons_db):  # No change means person was not found
        raise HTTPException(status_code=404, detail="Person not found")
    
    persons_db = new_db
    return {"message": f"Person {name} with BBAN {bban} deleted successfully"}

# 4. Add a new person (Prevent duplicate name + BBAN)
@app.post("/persons", response_model=Person)
async def add_person(person: Person):
    for existing_person in persons_db:
        if existing_person["name"].lower() == person.name.lower() and existing_person["bban"] == person.bban:
            raise HTTPException(status_code=400, detail="A person with this name and BBAN already exists")

    persons_db.append(person.dict())
    return person

# 5. Update a person's details by name AND BBAN
@app.put("/persons/{name}/{bban}", response_model=Person)
async def update_person(name: str, bban: str, updated_person: Person):
    for person in persons_db:
        if person["name"].lower() == name.lower() and person["bban"] == bban:
            person.update(updated_person.dict())
            return person
    raise HTTPException(status_code=404, detail="Person not found")
