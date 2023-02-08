import json 

file = "database.json"

tmp = []

database = {
        "users" : {
            "username" : "",
            "password" : ""},
        "farm"  : []
        }

def save_user(username="admin", password="0000"):
    try:
        with open(file, "r") as db:
            data = json.load(db)

    except FileNotFoundError:
        with open(file, "w") as db:
            json.dump(data, db, indent=4)

    else: 
        database["user"]["username"] = "admin"
        database["user"]["password"] = "0000"

        with open(file, "w") as db:
            json.dump(database, db, indent=4)

def update(tmp):
    with open(file, "r") as db:
        data = json.load(db)
    with open(file, "w") as save_db:
        json.dump(data, save_db, indent=4)


def gen(rows):
    try:
        with open(file, "r") as db:
            data = json.load(db)

            for x in rows.values():
                data["farm"].append(x)

            with open(file, "w") as save:
                json.dump(data, save, indent=4)
    except FileNotFoundError:
        with open(file, "w") as db:
            json.dump(database, db, indent=4)

    with open(file, "r") as db:
        data = json.load(db)

        return data["farm"]




def check_plnt(plant):
    pass
    
