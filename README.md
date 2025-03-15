# FastAPI Banking API

A simple banking API built with FastAPI that allows you to:
- List all persons
- Search for a person by **name** and **BBAN**
- Delete a person by **name** and **BBAN**
- Add a new person (Prevents duplicates by **name** and **BBAN**)
- Update a person's details by **name** and **BBAN**

This project also includes a script to generate **random banking data** using the **Faker** library and store it in a `db.json` file.

---

## 🚀 Installation & Setup

### 1️⃣ Install Python and Virtual Environment
Ensure you have **Python 3.8+** installed. Create a virtual environment and activate it:
```sh
python -m venv venv  # Create virtual environment
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate  # Windows
```

### 2️⃣ Install Dependencies
```sh
pip install fastapi uvicorn faker
```

### 3️⃣ Generate Sample Data
Run the script to generate **50 random persons** and save them in `db.json`:
```sh
python generate_data.py
```

### 4️⃣ Start FastAPI Server
Run the FastAPI application using Uvicorn:
```sh
uvicorn main:app --reload
```
The API will be available at: `http://127.0.0.1:8000`

### 5️⃣ Access API Documentation
FastAPI provides **interactive API docs** at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📌 API Endpoints

### 🔹 1. Get All Persons
**GET /persons**
```sh
curl -X 'GET' 'http://127.0.0.1:8000/persons' -H 'accept: application/json'
```
Response:
```json
[
  {"name": "Alice", "age": 30, "balance": 5000, "bban": "TZIR92411578156593"},
  {"name": "Bob", "age": 25, "balance": 3000, "bban": "MYNB48764759382421"}
]
```

### 🔹 2. Search Person by Name & BBAN
**GET /persons/{name}/{bban}**
```sh
curl -X 'GET' 'http://127.0.0.1:8000/persons/Alice/TZIR92411578156593' -H 'accept: application/json'
```

### 🔹 3. Delete Person by Name & BBAN
**DELETE /persons/{name}/{bban}**
```sh
curl -X 'DELETE' 'http://127.0.0.1:8000/persons/Bob/MYNB48764759382421' -H 'accept: application/json'
```

### 🔹 4. Add New Person
**POST /persons**
```sh
curl -X 'POST' 'http://127.0.0.1:8000/persons' \
-H 'Content-Type: application/json' \
-d '{"name": "Charlie", "age": 40, "balance": 8000, "bban": "GB29NWBK60161331926819"}'
```

⚠️ **Duplicate Check:** If the person with the same `name` and `bban` already exists, the API will return:
```json
{"detail": "A person with this name and BBAN already exists"}
```

### 🔹 5. Update Person by Name & BBAN
**PUT /persons/{name}/{bban}**
```sh
curl -X 'PUT' 'http://127.0.0.1:8000/persons/Alice/TZIR92411578156593' \
-H 'Content-Type: application/json' \
-d '{"name": "Alice", "age": 35, "balance": 9000, "bban": "TZIR92411578156593"}'
```

---

---

## 📌 Using Postman

1️⃣ Open **Postman** and create a new request.  
2️⃣ Select **GET**, **POST**, **PUT**, or **DELETE** depending on the operation.  
3️⃣ For **POST** and **PUT**, set the request type to **JSON** and provide a valid JSON body.  
4️⃣ Click **Send** and check the response.  

### 🔹 Postman Usage for Each API Transaction

#### 📍 Get All Persons
- Method: **GET**
- URL: `http://127.0.0.1:8000/persons`
- Click **Send**

#### 📍 Search for a Person by Name & BBAN
- Method: **GET**
- URL: `http://127.0.0.1:8000/persons/{name}/{bban}`
- Example: `http://127.0.0.1:8000/persons/Alice/TZIR92411578156593`
- Click **Send**

#### 📍 Delete a Person by Name & BBAN
- Method: **DELETE**
- URL: `http://127.0.0.1:8000/persons/{name}/{bban}`
- Example: `http://127.0.0.1:8000/persons/Bob/MYNB48764759382421`
- Click **Send**

#### 📍 Add a New Person
- Method: **POST**
- URL: `http://127.0.0.1:8000/persons`
- Body (JSON):
```json
{
  "name": "Charlie",
  "age": 40,
  "balance": 8000,
  "bban": "GB29NWBK60161331926819"
}
```
- Click **Send**

#### 📍 Update a Person by Name & BBAN
- Method: **PUT**
- URL: `http://127.0.0.1:8000/persons/{name}/{bban}`
- Body (JSON):
```json
{
  "name": "Alice",
  "age": 35,
  "balance": 9000,
  "bban": "TZIR92411578156593"
}
```
- Click **Send**

---

## 📂 Project Structure
```
📂 fastapi-banking-api
├── 📄 main.py            # FastAPI Application
├── 📄 generate_data.py   # Script to generate fake data (db.json)
├── 📄 db.json            # Sample database with persons
├── 📄 README.md          # Documentation
└── 📄 requirements.txt   # Python dependencies
```

---

## 🛠️ To-Do & Improvements
✅ Add database integration (e.g., SQLite, PostgreSQL)  
✅ Implement authentication for secure access  
✅ Add pagination for large datasets  