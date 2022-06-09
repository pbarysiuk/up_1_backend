from flask import Flask, jsonify, request
from flask_cors import CORS

from routers import drug_bank_router
from routers import natural_products_router
from routers import xdl_router

app = Flask(__name__)
CORS(app)



drug_bank_router.init_router(app)
natural_products_router.init_router(app)
xdl_router.init_router(app)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

