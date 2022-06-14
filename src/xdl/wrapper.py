class XdlWrapper:
    @staticmethod 
    def __xdlItem(item, method):
        result = {
            "id" : str(item['_id']),
            "filePath" : item['filePath'],
            "createdAt" : str(item['createdAt'].isoformat()),
            "createdBy" : None,
            "statusChangedAt" :  None if item['statusChangedAt'] is None else str(item['statusChangedAt'].isoformat()),
            "statusChangedBy" : None, 
        }
        if method == 'list':
            result['name'] = item['name']
            result['status'] = item['status']
        elif method == 'search':
            result['name'] = item['name']
        elif method == 'details':
            result['allDrugsNames'] = item['allDrugsNames']
            result['approvedDrugsNames'] = item['approvedDrugsNames']
            result['status'] = item['status']
            result['xml'] = item['xml']
            result['text'] = item['text']
        return result

    @staticmethod
    def listResult(list, count):
        items = []
        for item in list:
            items.append(XdlWrapper.__xdlItem(item = item, method='list'))
        return {"count" : count, "items" : items}

    @staticmethod
    def searchResult(list, count):
        items = []
        for item in list:
            items.append(XdlWrapper.__xdlItem(item = item, method='search'))
        return {"count" : count, "items" : items}

    @staticmethod
    def detailsResult(item):
        return XdlWrapper.__xdlItem(item = item, method='details')
   










