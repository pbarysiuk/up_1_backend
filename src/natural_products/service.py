from bson.json_util import dumps
from src.shared.database import Database
from src.shared.generalWrapper import GeneralWrapper
import traceback

def query(query: str, page: int):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        filter = {'$or': [
            {
                "cn": {
                    "$regex": query,
                    "$options": "i"
                }
            },
        ]}
        products = db.natural_products.find(filter).skip(page * 10).limit(10)
        count = db.natural_products.count_documents(filter)
        result = {"count": count, "items": list(products)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)
