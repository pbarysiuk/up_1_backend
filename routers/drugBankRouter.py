from urllib.parse import unquote

from flask import request
from importers import drugbankImporter, value_calculator

from src.drugbank import service


def initService(app):
    @app.route('/drugbank')
    def drugbank():
        return service.find(drug_name=request.args.get('name'),
                            drug_id=request.args.get('id'),
                            props=request.args.get('props'))

    @app.route('/drugbank/value_calculator')
    def calculator():
        return value_calculator.calculator()

    @app.route('/drugbank/query/<string:query>')
    def dquery(query):
        return service.query(user_query=unquote(query),
                             page=int(request.args.get('page')),
                             category=request.args.get('category'))

    @app.route('/drugbank/target/query/<string:query>')
    def targets_query(query):
        return service.query_targets(user_query=unquote(query))

    @app.route('/drugbank/category/query/<string:query>')
    def categories_query(query):
        return service.query_categories(user_query=unquote(query), page=int(request.args.get('page')))

    @app.route('/drugbank/drugs/category/<string:category_id>')
    def drugs_by_category(category_id):
        return service.drugbank_drugs_by_category(category_id, page=int(request.args.get('page')))

    @app.route('/drugbank/molecule/<string:query>')
    def molecule_query(query):
        return service.moleculeQuery(user_query=unquote(query))

    @app.route('/drugbank/import')
    def drugbank_import():
        return drugbankImporter.execute()

    @app.route('/drugbank/import/targets')
    def targets_import():
        return drugbankImporter.targets()

    @app.route('/drugbank/import/categories')
    def categories_import():
        return drugbankImporter.categories()
    
    @app.route('/drugbank/calculateMaintenanceDosage', methods=['POST'])
    def calculateMaintenanceDosage():
        data = request.get_json(force=True)
        return service.calculateMaintenanceDosage(data.get('drugs'), data.get('weight'), data.get('age'), data.get('gender'), data.get('geo'))

