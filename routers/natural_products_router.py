from urllib.parse import unquote

from flask import request

from src.natural_products import importer, service


def init_router(app):
    @app.route('/natural_products/query/<string:query>')
    def natural_products_query(query):
        return service.query(query=unquote(query),page=int(request.args.get('page')))


    @app.route('/natural_products/import')
    def natural_products_import():
        return importer.execute()