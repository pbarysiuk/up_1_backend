import requests

from src.shared import database


def execute():
    db = database.get_connection()
    db.dosage.drop()
    aid_url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/type/doseresponse/aids/JSON'
    AID_list = requests.get(aid_url).json()["IdentifierList"]["AID"]
    for AID in AID_list:
        try:
            url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/AID/{}/doseresponse/JSON".format(AID)
            response = requests.get(url).json()
            columns = ["AID",
                       "SID",
                       "Concentration",
                       "ConcentrationUnit",
                       "Response",
                       "ResponseUnit"]
            rows = response["Table"]["Row"]
            for row in rows:
                cell = row["Cell"]
                key = {'AID': AID}
                new_sid = dict()
                for i, column in enumerate(columns):
                    new_sid[column] = cell[i]
                db.dosage.update_one(key, {"$addToSet": {"sids": new_sid}}, upsert=True)
        except:
            print("AID not found {}".format(AID))

    return "Import Done"
