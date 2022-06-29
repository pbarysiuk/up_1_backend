from flask import Flask, jsonify, request
from flask_cors import CORS

from routers import drugBankRouter
from routers import naturalProductsRouter
from routers import xdlRouter
from routers import threeDRouter
from routers import userManagmentRouter
from routers import authRouter
from routers import profileRouter

app = Flask(__name__)
CORS(app)



drugBankRouter.initService(app)
naturalProductsRouter.initService(app)
xdlRouter.initService(app)
threeDRouter.initService(app)
userManagmentRouter.initService(app)
authRouter.initService(app)
profileRouter.initService(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

