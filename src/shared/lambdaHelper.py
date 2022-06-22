from json import loads

class LambdaHelper:

    valueTypeString = 'string'
    valueTypeInt = 'int'
    valueTypeFloat = 'float'
    
    @staticmethod
    def __getValue(event, parentKey, key, type, defaultValue):
        if event.get(parentKey) is None:
            return defaultValue
        value = event[parentKey].get(key)
        if value is None:
            return defaultValue
        if type == LambdaHelper.valueTypeFloat:
            return float(value)
        elif type == LambdaHelper.valueTypeInt:
            return int(value)
        return value

    @staticmethod
    def getQueryStringParam(event, key, type = 'string', defaultValue = None):
        return LambdaHelper.__getValue(event, 'queryStringParameters', key, type, defaultValue)
    
    @staticmethod 
    def getPathParam(event, key, type = 'string'):
        return LambdaHelper.__getValue(event, 'pathParameters', key, type, None)

    @staticmethod
    def getBodyParams(event, keys):
        if event.get('body') is None:
            result = {}
            for key in keys:
                result[key] = None
            return result
        body = loads(event['body'])
        result = {}
        for key in keys:
            result[key] = body.get(key)
        return result
