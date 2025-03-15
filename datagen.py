from faker import Faker
import json

fake = Faker()

persons_db = []

for i in range(50):
    persons_db.append(
        {
            "name": fake.name(),
            "age": fake.random_int(min=18, max=80),
            "balance": round(fake.random.uniform(1000, 100000), 2),
            "bban" : fake.bban()
        }
    )

with open("db.json", "w") as output:
    json.dump(persons_db, output)