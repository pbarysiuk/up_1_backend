class UsersWrapper:
    @staticmethod
    def __user(item, method):
        result = {
            "id" : str(item['_id']),
            "name" : item['name'],
            'email' : item['email'],
            "role" : item['role'],
            "image" : item['image'],
            "createdAt" : str(item['createdAt'].isoformat())
        }
        if method == 'details':
            result['verifiedAt'] = None if item['verifiedAt'] is None else str(item['verifiedAt'].isoformat())
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

