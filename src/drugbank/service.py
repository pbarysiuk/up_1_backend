import json
import os
import re

from bson.json_util import dumps

from src.shared import database
from src.ai_models.toxicity.eval import run_inference as run_toxicity


def find(drug_name: str, drug_id: str, props: str) -> [dict]:
    db = database.get_connection()

    props_list = props and props.split(":") or []
    if not "calculated_properties" in props_list and "toxicity" in props_list:
        props_list.append("calculated_properties")

    query = get_query(drug_id, drug_name)
    drug = db.drugs.find_one(query, props_list)

    if drug is None:
        raise Exception("drug not found")

    get_toxicity(drug, props_list)

    return dumps(drug)


def query(query: str, page: int) -> [dict]:
    db = database.get_connection()
    columns = ["drugbank_id", "name", "clinical_description", "chemical_properties", "calculated_properties",
               "experimental_properties"]
    filter = {'$or': [
        {
            "clinical_description": {
                "$regex": ".*{}.*".format(query),
                "$options": "i"
            }
        },
        {
            "calculated_properties": {
                "$regex": ".*{}.*".format(query),
                "$options": "i"
            }
        },
        {
            "chemical_properties": {
                "$regex": ".*{}.*".format(query),
                "$options": "i"
            }
        },
        {
            "name": {
                "$regex": ".*{}.*".format(query),
                "$options": "i"
            }
        }
    ]}
    drugs = db.drugs.find(filter, columns)\
        .skip(page*10)\
        .limit(10)
    count = db.drugs.count_documents(filter)
    return dumps({"count": count, "items": list(drugs)})


def get_query(drug_id, drug_name):
    regx = re.compile("^{}".format(drug_name), re.IGNORECASE)
    ret = {}
    if drug_name:
        ret["name"] = regx
    if drug_id:
        ret["drugbank_id"] = drug_id
    return ret


def get_toxicity(drug, props_list):
    if "toxicity" in props_list:
        smiles = drug["calculated_properties"]["SMILES"]
        toxicity = run_toxicity([smiles])
        drug["toxicity"] = dict()
        for key in toxicity:
            drug['toxicity'][key] = float(toxicity[key][0])


def document(drug_id: str) -> dict:
    dirname = os.path.dirname(__file__)
    drugbank_dir = os.path.join(dirname, '../../drugbank_docs')
    file_path = os.path.join(drugbank_dir, drug_id + ".json")
    file = open(file_path)
    data = json.load(file)
    file.close()
    return data
