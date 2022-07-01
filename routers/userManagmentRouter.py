from src.users.userManagmentBusiness import UserManagmentBusiness
from flask import  request
from urllib.parse import unquote

def initService(flaskApp):
    @flaskApp.route('/users/insertDefaultUser', methods=['GET'])
    def insertDefaultUser():
        return UserManagmentBusiness.insertDefaultUser()

    @flaskApp.route('/usersManagement/add', methods=['POST'])
    def addUser():
        headers = request.headers
        data = request.get_json(force=True)
        return UserManagmentBusiness.addUser(token=headers['auth'], name=data["name"], email=data["email"], role = data["role"], image=data.get('image'))

    @flaskApp.route('/usersManagement/update/<string:id>', methods=['PUT'])
    def updateUser(id):
        headers = request.headers
        data = request.get_json(force=True)
        return UserManagmentBusiness.updateUser(token=headers['auth'], userId=id, name=data["name"], email=data["email"], role = data["role"], image = data['image'])

    @flaskApp.route('/usersManagement/delete/<string:id>', methods=['DELETE'])
    def deleteUser(id):
        headers = request.headers
        return UserManagmentBusiness.deleteUser(token=headers['auth'], userId=id)

    @flaskApp.route('/usersManagement/details/<string:id>', methods=['GET'])
    def getUser(id):
        headers = request.headers
        return UserManagmentBusiness.getUser(token=headers['auth'], userId=id)

    @flaskApp.route('/usersManagement/list', methods=['GET'])
    def getUsersList():
        headers = request.headers
        args = request.args
        return UserManagmentBusiness.getUsersList(token=headers['auth'], pageNumber=args.get("page", default=0, type=int), pageSize=args.get("pageSize", default=10, type=int), criteria=unquote(args.get("query", default="", type=str)) )

    