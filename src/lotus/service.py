from bson.json_util import dumps

from src.shared import database


def query(query: str, page: int) -> [dict]:
    db = database.get_connection()
    filter = {'$or': [
        {
            "traditional_name": {
                "$regex": ".*{}.*".format(query),
                "$options": "i"
            }
        },
    ]}
    products = db.lotusUniqueNaturalProduct.find(filter).skip(page * 10).limit(10)
    #count = db.lotusUniqueNaturalProduct.count_documents(filter)
    return dumps({"count": "n", "items": list(products)})
