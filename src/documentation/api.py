toxicity_model = {
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
models = {
    "toxicity": toxicity_model,
    "ai": {
        "smiles": "String",
        "solubility": "Float",
        "toxicity": toxicity_model
    }
}


def endpoints():
    return {
        "endpoints": [
            {
                "GET /drugs/<string:drug_names>": {
                    "description": "Eval solubility and toxicity from a given drug names split by :",
                    "example": "drugs/favipiravir:aspirin",
                    "output": {
                        "not_found_drugs": "Array string of drug names not found",
                        "<drugname>": models["ai"]
                    }
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
                        "drug_interactions": "Array",
                        "food_interactions": "Array",
                        "calculated_properties": "Array",
                        "experimental_properties": "Array",
                        "targets": "Array",
                        "toxicity": models['toxicity']
                    }
                },
                "GET /drugbank/value_calculator": {
                    "description": "Get min and max value of all drugs in database of each required property",
                },
                "GET /drugbank/query/<string:query>?page=<int:page_number>": {
                    "description": "Search in name, clinical_description, chemical_properties, calculated_properties."
                                   "Paginated by 10",
                    "filters": {
                        "query_params": {
                            "page": "Required Integer Ex.: 0."
                        }
                    },
                    "example": "/drugbank/query/covid",
                    "output": {
                        "drugbank_id": "String",
                        "name": "String",
                        "calculated_properties": "Array",
                        "chemical_properties": "Array"
                    }
                },
                "GET /drugbank/document/<string:drugbank_id>": {
                    "description": "Get drug full info from drugbank",
                    "example": "/document/DB01234",
                    "output": "Everything from drugbank"
                },
                "GET /natural_products/query/<string:query>?page=<int:page_number>": {
                    "description": "Search in cn (canonical_name)"
                                   "Paginated by 10",
                    "filters": {
                        "query_params": {
                            "page": "Required Integer Ex.: 0."
                        }
                    },
                    "example": "/natural_products/query/diacetoxyspata",
                    "output": {
                        "drugbank_id": "String",
                        "name": "String",
                        "calculated_properties": "Array",
                        "chemical_properties": "Array"
                    }
                },
                "GET /lotus/query/<string:query>?page=<int:page_number>": {
                    "description": "Search in traditional_name"
                                   "Paginated by 10",
                    "filters": {
                        "query_params": {
                            "page": "Required Integer Ex.: 0."
                        }
                    },
                    "example": "/lotus/query/diacetoxyspata",
                    "output": {
                        "drugbank_id": "String",
                        "name": "String",
                        "calculated_properties": "Array",
                        "chemical_properties": "Array"
                    }
                },
                "GET /eval?smiles=<string:smiles>": {
                    "description": "Run AI models for given drug SMILES",
                    "output": models["ai"]
                },
                "POST /drug-interaction": {
                    "description": "Run AI for drug interaction, giving likelihood of interaction",
                    "body": {
                      "smile1": "String",
                      "smile2": "String"
                    },
                    "output": [
                        {
                            "label": "String",
                            "value": "Number"
                        }
                    ]
                }
            }
        ]
    }
