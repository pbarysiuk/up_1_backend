from src.users.authBusiness import AuthBusiness
from flask import  request

def initService(flaskApp):
    @flaskApp.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json(force=True)
        return AuthBusiness.login(email=data["email"], password=data["password"])

    @flaskApp.route('/auth/resetPasswordFirstTime', methods=['PUT'])
    def resetPasswordFirstTime():
        data = request.get_json(force=True)
        headers = request.headers
        return AuthBusiness.resetPasswordFirstTime(resetPasswordToken= headers['auth'], password=data["password"])

    @flaskApp.route('/auth/refreshToken', methods=['POST'])
    def refreshToken():
        headers = request.headers
        return AuthBusiness.refreshToken(refreshToken=headers['auth'])

    @flaskApp.route('/auth/resendVerificationCode', methods=['POST'])
    def resendVerificationCode():
        data = request.get_json(force=True)
        return AuthBusiness.resendVerificationCode(email=data["email"])

    @flaskApp.route('/auth/verifyAccount', methods=['POST'])
    def verifyAccount():
        data = request.get_json(force=True)
        return AuthBusiness.verify(email= data["email"], code=data["code"])
    
    
    @flaskApp.route('/auth/forgetPasswordFirstStep', methods=['POST'])
    def forgetPasswordFirstStep():
        data = request.get_json(force=True)
        return AuthBusiness.forgetPasswordFirstStep(email=data["email"])

    @flaskApp.route('/auth/resendForgetPasswordCode', methods=['POST'])
    def resendForgetPasswordCode():
        data = request.get_json(force=True)
        return AuthBusiness.resendForgetPasswordCode(requestId = data["forgetPasswordRequestId"])

    @flaskApp.route('/auth/forgetPasswordSecondStep', methods=['POST'])
    def forgetPasswordSecondStep():
        data = request.get_json(force=True)
        return AuthBusiness.forgetPasswordSecondStep(requestId = data["forgetPasswordRequestId"], code=data["code"], password=data["password"])
    
    @flaskApp.route('/auth/register', methods=['POST'])
    def register():
        data = request.get_json(force=True)
        return AuthBusiness.register(email=data["email"], password=data["password"], name=data['name'], image=data.get('image'))

    @flaskApp.route('/auth/loginWith3rdParty', methods=['POST'])
    def loginWithThirdParty():
        data = request.get_json(force=True)
        return AuthBusiness.loginWithThirdParty(thrirdPartyType=data["thrirdPartyType"], thirdPartyToken=data["thirdPartyToken"])