from src.users.authBusiness import BusinessAuth
from flask import  request

def initService(flaskApp):
    @flaskApp.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json(force=True)
        return BusinessAuth.login(email=data["email"], password=data["password"])

    @flaskApp.route('/auth/refreshToken', methods=['GET'])
    def refreshToken():
        headers = request.headers
        return BusinessAuth.refreshToken(refreshToken=headers['auth'])

    @flaskApp.route('/auth/resendVerificationCode', methods=['POST'])
    def resendVerificationCode():
        data = request.get_json(force=True)
        return BusinessAuth.resendVerificationCode(email=data["email"])

    @flaskApp.route('/auth/verifyAccount', methods=['POST'])
    def verifyAccount():
        data = request.get_json(force=True)
        return BusinessAuth.verify(email= data["email"], code=data["code"], password=data["password"])
    
    '''
    @flaskApp.route('/auth/forgetPasswordFirstStep', methods=['POST'])
    def forgetPasswordFirstStep():
        data = request.get_json(force=True)
        return BusinessAuth.forgetPasswordFirstStep(email=data["email"])

    @flaskApp.route('/auth/resendForgetPasswordCode', methods=['POST'])
    def resendForgetPasswordCode():
        data = request.get_json(force=True)
        return BusinessAuth.resendForgetPasswordCode(requestId = data["request_forget_password_id"])

    @flaskApp.route('/auth/forgetPasswordSecondStep', methods=['POST'])
    def forgetPasswordSecondStep():
        data = request.get_json(force=True)
        return BusinessAuth.forgetPasswordSecondStep(requestId = data["request_forget_password_id"], code=data["code"], password=data["password"])
    '''
    