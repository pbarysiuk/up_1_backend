class UsersWrapper:
    @staticmethod
    def __user(item, method):
        result = {
            "id" : str(item['_id']),
            "name" : item['name'],
            'email' : item['email'],
            "role" : item['role'],
            "image" : item['image'],
            "status" : item['status'],
            "createdAt" : str(item['createdAt'].isoformat()),
        }
        if method == 'details':
            result['thrirdPartyLogin'] = {} if item['thirdPartyLogin'] is None else item['thirdPartyLogin']
            result['createdBy'] = None if item['createdBy'] is None else str(item['createdBy'])
            result['updatedAt'] = None if item['updatedAt'] is None else str(item['updatedAt'].isoformat())
            result['verifiedAt'] = None if item['verifiedAt'] is None else str(item['verifiedAt'].isoformat())
            result['approvedAt'] = None if item['approvedAt'] is None else str(item['approvedAt'].isoformat())
            result['lastChangePasswordAt'] = None if item['lastChangePasswordAt'] is None else str(item['lastChangePasswordAt'].isoformat())
        if method == 'profile':
            result['thrirdPartyLogin'] = {} if item['thirdPartyLogin'] is None else item['thirdPartyLogin']
            result['apiKey'] = item['apiKey'].get('value')
            result['lastChangePasswordAt'] = None if item['lastChangePasswordAt'] is None else str(item['lastChangePasswordAt'].isoformat())
            #result['updatedAt'] = None if item['updatedAt'] is None else str(item['updatedAt'].isoformat())
        return result


    @staticmethod
    def detailsResult(item):
        return UsersWrapper.__user(item, 'details')

    @staticmethod
    def profileResult(item):
        return UsersWrapper.__user(item, 'profile')      

    @staticmethod
    def loginResult(item, accessToken, refreshToken):
        result = {
            "accessToken" : accessToken,
            "refreshToken" : refreshToken,
            "user" : UsersWrapper.profileResult(item)
        }
        return result

    @staticmethod
    def listResult(list, count):
        items = []
        for item in list:
            items.append(UsersWrapper.__user(item = item, method='list'))
        return {"count" : count, "items" : items}

    @staticmethod
    def forgetPasswordResult(insertedId):
        result = {
            "forgetPasswordRequestId" : str(insertedId)
        }
        return result

    @staticmethod
    def resetPasswordFirstTimeTokenResult(token):
        result = {
            "firstTimeResetPasswordToken" : token
        }
        return result

