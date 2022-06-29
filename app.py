from flask import Flask, jsonify, request
from flask_cors import CORS

from routers import drug_bank_router
from routers import natural_products_router
from routers import xdl_router
from routers import threeD_router
from routers import userManagmentRouter
from routers import auth_router
from routers import profileRouter

app = Flask(__name__)
CORS(app)



drug_bank_router.init_router(app)
natural_products_router.init_router(app)
xdl_router.init_router(app)
threeD_router.init_router(app)
userManagmentRouter.initService(app)
auth_router.initService(app)
profileRouter.initService(app)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

