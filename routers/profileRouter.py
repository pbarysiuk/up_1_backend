from src.users.profileBusiness import ProfileBusiness
from flask import  request
from urllib.parse import unquote

def initService(flaskApp):
    @flaskApp.route('/profile/get', methods=['GET'])
    def getProfile():
        headers = request.headers
        return ProfileBusiness.getProfile(token=headers['auth'])

    @flaskApp.route('/profile/update', methods=['PUT'])
    def updateProfile():
        headers = request.headers
        data = request.get_json(force=True)
        return ProfileBusiness.updateProfile(token=headers['auth'], email=data["email"], name=data["name"], image=data['image'])

    @flaskApp.route('/profile/changePassword', methods=['PUT'])
    def changePassword():
        headers = request.headers
        data = request.get_json(force=True)
        return ProfileBusiness.changePassword(token=headers['auth'], newPassword=data["newPassword"])
    