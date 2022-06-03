from bson.json_util import dumps
from src.shared.database import Database


def query(query: str, page: int):
    dbConnection = (Database())
    db = dbConnection.db
    filter = {'$or': [
        {
            "cn": {
                "$regex": ".*{}.*".format(query),
                "$options": "i"
            }
        },
    ]}
    products = db.natural_products.find(filter).skip(page * 10).limit(10)
    count = db.natural_products.count_documents(filter)
    return dumps({"count": count, "items": list(products)})
