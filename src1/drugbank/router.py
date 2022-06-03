from urllib.parse import unquote

from flask import request

from src.drugbank import value_calculator, service, exporter, importer


def init_router(app):
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

    @app.route('/drugbank/import')
    def drugbank_import():
        return importer.execute()

    @app.route('/drugbank/import/targets')
    def targets_import():
        return importer.targets()

    @app.route('/drugbank/import/categories')
    def categories_import():
        return importer.categories()

    @app.route('/drugbank/export')
    def export():
        return exporter.export_smiles_amino_acid_sequences()

    @app.route('/drugbank/export-false')
    def export_false():
        return exporter.export_false_smiles_amino_acid_sequences()

    @app.route('/drugbank/document/<string:drug_id>')
    def document(drug_id: str):
        return service.document(drug_id)
