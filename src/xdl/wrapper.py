class XdlWrapper:
    @staticmethod 
    def __xdlItem(item, method):
        result = {
            "id" : str(item['_id']),
            "name" : item['name'],
            'title' : item.get('title'),
            "filePath" : item['filePath'],
            "createdAt" : str(item['createdAt'].isoformat()),
            "createdBy" : None,
            "statusChangedAt" :  None if item['statusChangedAt'] is None else str(item['statusChangedAt'].isoformat()),
            "statusChangedBy" : None, 
        }
        if method == 'list':
            result['status'] = item['status']
        elif method == 'details':
            result['status'] = item['status']
            result['xml'] = item['xml']
            result['text'] = item['text']
        elif method == 'search':
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
   










