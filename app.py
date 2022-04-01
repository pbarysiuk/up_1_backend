from flask import Flask, jsonify, request
from flask_cors import CORS
from urllib.parse import unquote

from src.ai_models.eval import eval, get_data
from src.drugbank import \
    service, \
    value_calculator, \
    importer as drugbank_importer, \
    exporter as drugbank_exporter
from src.natural_products import \
    importer as natural_products_importer, \
    service as natural_products_service

app = Flask(__name__)
CORS(app)


@app.route('/')
def help():
    return {
        "endpoints": [
            {
                "GET /drugs/<string:drug_names>": {
                    "description": "Eval solubility and toxicity from a given drug names split by :",
                    "example": "drugs/favipiravir:aspirin",
                    "output": {
                        "not_found_drugs": "Array string of drug names not found",
                        "drugname": {
                            "smiles": "String",
                            "solubility": "Float",
                            "toxicity": {
                                'NR-AR': "Float",
                                'NR-AR-LBD': "Float",
                                'NR-AhR': "Float",
                                'NR-Aromatase': "Float",
                                'NR-ER': "Float",
                                'NR-ER-LBD': "Float",
                                'NR-PPAR-gamma': "Float",
                                'SR-ARE': "Float",
                                'SR-ATAD5': "Float",
                                'SR-HSE': "Float",
                                'SR-MMP': "Float",
                                'SR-p53': "Float"
                            }
                        }
                    }
                },
                "GET /drugbank/value_calculator": {
                    "description": "Get min and max value of all drugs in database of each required property",
                },
                "GET /drugbank": {
                    "description": "Get drug selected info from drugbank",
                    "filters": {
                        "query_params": {
                            "id": "String. Ex.: DB01234",
                            "name": "String. Ex.: favipiravir",
                            "props": "String split by : with props to retrieve. Ex: name:drug_interactions:targets",
                        }
                    },
                    "example": "/drugbank?name=favipiravir&props=name:drug_interactions:targets",
                    "output": {
                        "drugbank_id": "String",
                        "name": "String",
                        "drug_interacions": "Array",
                        "food_interactions": "Array",
                        "calculatedProperties": "Array",
                        "experimental_properties": "Array",
                        "targets": "Array",
                        "toxicity": {
                            'NR-AR': "Float",
                            'NR-AR-LBD': "Float",
                            'NR-AhR': "Float",
                            'NR-Aromatase': "Float",
                            'NR-ER': "Float",
                            'NR-ER-LBD': "Float",
                            'NR-PPAR-gamma': "Float",
                            'SR-ARE': "Float",
                            'SR-ATAD5': "Float",
                            'SR-HSE': "Float",
                            'SR-MMP': "Float",
                            'SR-p53': "Float"
                        }
                    }
                },
                "GET /document/<string:drugbank_id>": {
                    "description": "Get drug full info from drugbank",
                    "example": "/document/DB01234",
                    "output": "Everything from drugbank"
                }
            }
        ]
    }


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
    return drugbank_exporter.execute()


@app.route('/natural_products/query/<string:query>')
def natural_products_query(query):
    return natural_products_service.query(unquote(query), int(request.args.get('page')))


@app.route('/natural_products/import')
def natural_products_import():
    return natural_products_importer.execute()


@app.route('/document/<string:drug_id>')
def document(drug_id: str):
    return service.document(drug_id)


@app.route('/eval')
def eval_smiles():
    return get_data([unquote(request.args.get('smiles'))])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
