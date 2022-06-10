from flask import  request
from urllib.parse import unquote
from src.xdl.business import XdlBusiness

def init_router(flaskApp):
    @flaskApp.route('/xdl/add', methods=['POST'])
    def addXdl():
        data = request.get_json(force=True)
        return XdlBusiness.add(drugs = data["drugs"], filePath=data["filePath"])

    @flaskApp.route('/xdl/getList', methods=['GET'])
    def getXdlList():
        args = request.args
        return XdlBusiness.getList(query= unquote(args.get("query", default='', type=str)), pageNumber=args.get("page", default=0, type=int), pageSize=args.get("pageSize", default=10, type=int))

    @flaskApp.route('/xdl/getDetails/<string:id>', methods=['GET'])
    def getXdlDetails(id):
        return XdlBusiness.getDetails(id = id)

    @flaskApp.route('/xdl/changeStatus/<string:id>', methods=['PUT'])
    def changeXdlStatus(id):
        data = request.get_json(force=True)
        return XdlBusiness.changeStatus(id= id, status=data["approve"])

    @flaskApp.route('/xdl/search', methods=['GET'])
    def searchXdl():
        args = request.args
        return XdlBusiness.search(query= unquote(args.get("query")), pageNumber=args.get("page", default=0, type=int), pageSize=args.get("pageSize", default=10, type=int))

