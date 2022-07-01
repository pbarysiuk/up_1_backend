from bson.json_util import dumps

from src.shared.database import Database
from src.shared.generalWrapper import GeneralWrapper

def query(query: str, page: int):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        filter = {'$or': [
            {
                "traditional_name": {
                    "$regex": query,
                    "$options": "i"
                }
            },
        ]}
        products = db.lotusUniqueNaturalProduct.find(filter).skip(page * 10).limit(10)
        #count = db.lotusUniqueNaturalProduct.count_documents(filter)
        result = {"count": "n", "items": list(products)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        return GeneralWrapper.generalErrorResult(e)
