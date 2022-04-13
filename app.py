from bson.json_util import dumps
from flask import Flask, jsonify, request
from flask_cors import CORS
from urllib.parse import unquote

from src.ai_models.eval import eval, get_data
from src.ai_models.drug_interaction.eval import run_inference as run_drug_interaction
from src.documentation import api
from src.drugbank import \
    service, \
    value_calculator, \
    importer as drugbank_importer, \
    exporter as drugbank_exporter
from src.natural_products import \
    importer as natural_products_importer, \
    service as natural_products_service
from src.lotus import service as lotus_service

app = Flask(__name__)
CORS(app)


@app.route('/')
def help():
    return api.endpoints()


@app.route('/drugs/<string:drug_names>')
def drugs(drug_names):
    output = eval(drug_names)
    return jsonify(output)


@app.route('/drugbank')
def drugbank():
    return service.find(request.args.get('name'), request.args.get('id'), request.args.get('props'))


@app.route('/drugbank/value_calculator')
def calculator():
    return value_calculator.calculator()


@app.route('/drugbank/query/<string:query>')
def drugbank_query(query):
    return service.query(unquote(query), int(request.args.get('page')))


@app.route('/drugbank/import')
def drugbank_import():
    return drugbank_importer.execute()


@app.route('/drugbank/export')
def drugbank_export():
    return drugbank_exporter.export_smiles_amino_acid_sequences()


@app.route('/drugbank/export-false')
def drugbank_export_false():
    return drugbank_exporter.export_false_smiles_amino_acid_sequences()


@app.route('/drugbank/document/<string:drug_id>')
def document(drug_id: str):
    return service.document(drug_id)


@app.route('/natural_products/query/<string:query>')
def natural_products_query(query):
    return natural_products_service.query(unquote(query), int(request.args.get('page')))


@app.route('/natural_products/import')
def natural_products_import():
    return natural_products_importer.execute()


@app.route('/lotus/query/<string:query>')
def lotus(query):
    return lotus_service.query(unquote(query), int(request.args.get('page')))


@app.route('/eval')
def eval_smiles():
    return get_data([unquote(request.args.get('smiles'))])


@app.route('/drug-interaction', methods=['POST'])
def drug_interaction():
    data = request.get_json(force=True)
    result = run_drug_interaction(data["smile1"], data["smile2"])
    return dumps(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
