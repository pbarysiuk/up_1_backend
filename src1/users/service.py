from src.users.business import BusinessUsers
from flask import  request
from urllib.parse import unquote

def initService(flaskApp):
    @flaskApp.route('/users/insertDefaultUser', methods=['GET'])
    def insertDefaultUser():
        return BusinessUsers.insertDefaultUser()

    @flaskApp.route('/users', methods=['POST'])
    def addUser():
        headers = request.headers
        data = request.get_json(force=True)
        return BusinessUsers.addUser(token=headers['auth'], name=data["name"], email=data["email"], password=data["password"], role = data["role"])

    @flaskApp.route('/users/<string:id>', methods=['PUT'])
    def updateUser(id):
        headers = request.headers
        data = request.get_json(force=True)
        return BusinessUsers.updateUser(token=headers['auth'], userId=id, name=data["name"], email=data["email"], role = data["role"])

    @flaskApp.route('/users/<string:id>', methods=['DELETE'])
    def deleteUser(id):
        headers = request.headers
        return BusinessUsers.deleteUser(token=headers['auth'], userId=id)

    @flaskApp.route('/users/<string:id>', methods=['GET'])
    def getUser(id):
        headers = request.headers
        return BusinessUsers.getUser(token=headers['auth'], userId=id)

    @flaskApp.route('/users', methods=['GET'])
    def getUsersList():
        headers = request.headers
        args = request.args
        return BusinessUsers.getUsersList(token=headers['auth'], page=args.get("page", default=1, type=int), pageSize=args.get("pageSize", default=10, type=int), criteria=unquote(args.get("query", default="", type=str)) )

    @flaskApp.route('/profile', methods=['GET'])
    def getProfile():
        headers = request.headers
        return BusinessUsers.getProfile(token=headers['auth'])

    @flaskApp.route('/profile', methods=['PUT'])
    def updateProfile():
        headers = request.headers
        data = request.get_json(force=True)
        return BusinessUsers.updateProfile(token=headers['auth'], email=data["email"], name=data["name"])

    @flaskApp.route('/profile/changePassword', methods=['PUT'])
    def changePassword():
        headers = request.headers
        data = request.get_json(force=True)
        return BusinessUsers.changePassword(token=headers['auth'], oldPassword=data["old_password"], newPassword=data["new_password"])



    