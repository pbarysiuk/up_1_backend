import json
import os
import re
from bson.json_util import dumps
from src.shared.database import Database
from src.shared.generalWrapper import GeneralWrapper
import pymongo
import traceback

def calculateMaintenanceDosage(drugs, weight, age, gender, geo):
    try:
        result = []
        for d in drugs:
            md = calculateMaintenanceDosageForSingleDrug(d, weight, age, gender, geo)
            result.append({
                "drug" : d,
                "maintenanceDosage" : md
            })
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)

def calculateMaintenanceDosageForSingleDrug(drug, weight, age, gender, geo):
    allDrugs = {
        "favipiravir" : {
            'dose' : 600,
            "groups" : [
                {
                    'gt' : -10000000,
                    'lwe' : 30,
                    'clearance' : 6.72,
                    'volumeOfDistribution' : 15
                },
                {
                    'gt' : 30,
                    'lwe' : 60,
                    'clearance' : 6.23,
                    'volumeOfDistribution' : 17
                },
                {
                    'gt' : 60,
                    'lwe' : 1000000,
                    'clearance' : 5.4,
                    'volumeOfDistribution' : 20
                },
            ]
        },
        "balicatib" : {
            'dose' : 600,
            "groups" : [
                {
                    'gt' : -10000000,
                    'lwe' : 30,
                    'clearance' : 0.45,
                    'volumeOfDistribution' : 3
                },
                {
                    'gt' : 30,
                    'lwe' : 60,
                    'clearance' : 0.4,
                    'volumeOfDistribution' : 3.2
                },
                {
                    'gt' : 60,
                    'lwe' : 1000000,
                    'clearance' : 0.3,
                    'volumeOfDistribution' : 3.5
                },
            ]
        },
        "ritonavir" : {
            'dose' : 100,
            "groups" : [
                {
                    'gt' : -10000000,
                    'lwe' : 30,
                    'clearance' : 10,
                    'volumeOfDistribution' : 2.46
                },
                {
                    'gt' : 30,
                    'lwe' : 60,
                    'clearance' : 9,
                    'volumeOfDistribution' : 2.7
                },
                {
                    'gt' : 60,
                    'lwe' : 1000000,
                    'clearance' : 7.8,
                    'volumeOfDistribution' : 3.2
                },
            ]
        },
        "remdesivir" : {
            'dose' : 200,
            "groups" : [
                {
                    'gt' : -10000000,
                    'lwe' : 30,
                    'clearance' : 1.8,
                    'volumeOfDistribution' : 45.1
                },
                {
                    'gt' : 30,
                    'lwe' : 60,
                    'clearance' : 1.2,
                    'volumeOfDistribution' : 62.3
                },
                {
                    'gt' : 60,
                    'lwe' : 1000000,
                    'clearance' : 0.9,
                    'volumeOfDistribution' : 73.4
                },
            ]
        },
        "cephalexin" : {
            'dose' : 10,
            "groups" : [
                {
                    'gt' : -10000000,
                    'lwe' : 5,
                    'clearance' : 22.56,
                    'volumeOfDistribution' : 5.2
                },
                {
                    'gt' : 5,
                    'lwe' : 15,
                    'clearance' : 20.24,
                    'volumeOfDistribution' : 5.8
                },
                {
                    'gt' : 15,
                    'lwe' : 1000000,
                    'clearance' : 18.38,
                    'volumeOfDistribution' : 6.3
                },
            ]
        },
        "ivermectin" : {
            'dose' : 1,
            "groups" : [
                {
                    'gt' : -10000000,
                    'lwe' : 30,
                    'clearance' : 18,
                    'volumeOfDistribution' : 3
                },
                {
                    'gt' : 30,
                    'lwe' : 60,
                    'clearance' : 16,
                    'volumeOfDistribution' : 3.3
                },
                {
                    'gt' : 60,
                    'lwe' : 1000000,
                    'clearance' : 14.8,
                    'volumeOfDistribution' : 3.5
                },
            ]
        }
    }
    selectedDrug = allDrugs.get(drug.lower())
    if selectedDrug is None:
        selectedDrug = allDrugs.get('favipiravir')
    clearance = selectedDrug['groups'][0]['clearance']
    volumeOfDistribution = selectedDrug['groups'][0]['volumeOfDistribution']
    for g in selectedDrug['groups']:
        if age > g['gt'] and age <= g['lwe']:
            clearance = g['clearance']
            volumeOfDistribution = g['volumeOfDistribution']
            break
    if weight <= 0:
        weight = 1.0 
    maintenanceDose = (clearance * selectedDrug['dose']) / (volumeOfDistribution * weight) 
    #print ("md: " + str(maintenanceDose))
    genders = ['male', 'female']
    #if not (gender.lower() in genders):
    #    gender =genders[0]
    if gender.lower() == genders[1]:
        maintenanceDose = maintenanceDose - (maintenanceDose* 0.08)
    #print ("md after gender: " + str(maintenanceDose))

    if geo.lower() == 'europe':
        maintenanceDose = maintenanceDose + (maintenanceDose* 0.01)
    elif geo.lower() == 'africa':
        maintenanceDose = maintenanceDose + (maintenanceDose* 0.07)
    elif geo.lower() == 'australia':
        maintenanceDose = maintenanceDose + (maintenanceDose* 0.03)
    elif geo.lower() == 'america':
        maintenanceDose = maintenanceDose + (maintenanceDose* 0.02)
    #print ("md after geo: " + str(maintenanceDose))
    return maintenanceDose

        



def calculateMaintenanceDosage1(drug, weight, age, gender, geo):
    try:
        clearanceG1 = [6.72, 0.45, 10, 1.8, 22.56, 18]
        clearanceG2 = [6.23, 0.40, 9, 1.2, 20.24, 16]
        clearanceG3 = [5.4, 0.3, 7.8, 0.9, 18.38, 14.8]
        volumeOfDistributionG1 = [15, 3, 2.46, 45.1, 5.2, 3]
        volumeOfDistributionG2 = [17, 3.2, 2.7, 62.3, 5.8, 3.3]
        volumeOfDistributionG3 = [20, 3.5, 3.2, 73.4, 6.3, 3.5]
        dose = [600, 600, 100, 200, 10, 1]
        drugs = ["favipiravir", "balicatib", "ritonavir", "remdesivir", "cephalexin", "ivermectin"]
        selectedIndex = 0
        currentIndex = 0
        for d in drugs:
            if d == drug.lower():
                selectedIndex = currentIndex
                break
            currentIndex += 1
        selectedGroup = 'g1'
        if selectedIndex == 4:
            if age <= 5:
                selectedGroup = 'g1'
            elif age > 5 and age <= 15:
                selectedGroup = 'g2'
            elif age > 15:
                selectedGroup = 'g3'
        else:
            if age < 30:
                selectedGroup = 'g1'
            elif age >= 31 and age <= 60:
                selectedGroup = 'g2'
            elif age >= 61:
                selectedGroup = 'g3'
        clearance = clearanceG1
        volumeOfDistribution = volumeOfDistributionG1
        if selectedGroup == 'g2':
            clearance = clearanceG2
            volumeOfDistribution = volumeOfDistributionG2
        elif selectedGroup == 'g3':
            clearance = clearanceG3
            volumeOfDistribution = volumeOfDistributionG3

        if weight <= 0:
            weight = 1.0 
        maintenanceDose = (clearance[selectedIndex] * dose[selectedIndex]) / (volumeOfDistribution[selectedIndex] * weight) 
        #print ("md: " + str(maintenanceDose))
        genders = ['male', 'female']
        #if not (gender.lower() in genders):
        #    gender =genders[0]
        if gender.lower() == genders[1]:
            maintenanceDose = maintenanceDose - (maintenanceDose* 0.08)
        #print ("md after gender: " + str(maintenanceDose))

        if geo.lower() == 'europe':
            maintenanceDose = maintenanceDose + (maintenanceDose* 0.01)
        elif geo.lower() == 'africa':
            maintenanceDose = maintenanceDose + (maintenanceDose* 0.07)
        elif geo.lower() == 'australia':
            maintenanceDose = maintenanceDose + (maintenanceDose* 0.03)
        elif geo.lower() == 'america':
            maintenanceDose = maintenanceDose + (maintenanceDose* 0.02)
        #print ("md after geo: " + str(maintenanceDose))


        result = {
            "maintenanceDosage" : maintenanceDose
        }  
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)

def find(drug_name: str, drug_id: str, props: str):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        props_list = props and props.split(":") or []
        if not "calculated_properties" in props_list and "toxicity" in props_list:
            props_list.append("calculated_properties")
        query = get_query(drug_id, drug_name)
        drug = db.drugs.find_one(query, props_list)
        if drug is None:
            return {
                "isBase64Encoded": False,
                "statusCode": 404,
                "headers": { "Access-Control-Allow-Origin": "*" },
                "body": dumps({})
            }
        return GeneralWrapper.successResult(drug)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)


def query(user_query: str, page: int, category: str):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        molecules =  None
        if category is None:
            molecules = db.molecules.find({
                "name" : {
                    "$regex": user_query,
                    "$options": "i"
                }
            }, {"name" : 1}).skip(page * 10).limit(10)
            names = [o['name'] for o in molecules]
            columns = ["cid", "drugbank_id", "name", "clinical_description", "chemical_properties", "calculated_properties",
                "experimental_properties", "synonyms", "structured_adverse_effects", "structured_contraindications"]
            where_query = {
                "name" : {
                    "$in" : names
                } 
            }
            drugs = db.drugs.find(where_query, columns)
            count = db.molecules.count_documents({
                "name" : {
                    "$regex": user_query,
                    "$options": "i"
                }
            })
            result = {"count": count, "items": list(drugs)}
            return GeneralWrapper.successResult(result)
        else:
            
            or_query = {
                "name" : {
                    "$regex": user_query,
                    "$options": "i"
                }
            }
            columns = ["cid", "drugbank_id", "name", "clinical_description", "chemical_properties", "calculated_properties",
                    "experimental_properties", "synonyms", "structured_adverse_effects", "structured_contraindications"]
            '''
            or_query = {
                '$or': [
                    {
                        "clinical_description": {
                            "$regex": user_query,
                            "$options": "i"
                        }
                    },
                    {
                        "name": {
                            "$regex": user_query,
                            "$options": "i"
                        }
                    },
                    {
                        "synonyms.synonym": {
                            "$regex": user_query,
                            "$options": "i"
                        }
                    }
                ]
            }
            '''
            where_query = {
                "$and": [
                    or_query,
                ],
            }
            where_query["$and"].append({"categories.drugbank_id": category})
            drugs = None
            drugs = db.drugs.find(where_query, columns).skip(page * 10).limit(10)
            count = db.drugs.count_documents(where_query)
            result = {"count": count, "items": list(drugs)}
            return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)


def moleculeQuery(user_query: str):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        molecules = db.molecules.find({
            "name" : {
                "$regex": user_query,
                "$options": "i"
            }
        }, {"name" : 1}).limit(10)
        names = [o['name'] for o in molecules]
        or_query = {
            "name" : {
                "$in" : names
            } 
        }
        columns = ["cid", "drugbank_id", "name", "clinical_description", "chemical_properties", "calculated_properties",
                "experimental_properties", "synonyms", "structured_adverse_effects", "structured_contraindications"]
        '''
        or_query = {
            '$or': [
                {
                    "clinical_description": {
                        "$regex": user_query,
                        "$options": "i"
                    }
                },
                {
                    "name": {
                        "$regex": user_query,
                        "$options": "i"
                    }
                },
                {
                    "synonyms.synonym": {
                        "$regex": user_query,
                        "$options": "i"
                    }
                }
            ]
        }
        '''
        where_query = {
            "$and": [
                or_query,
            ],
        }    
        drugs = db.drugs.find(where_query, columns)
        count = db.drugs.count_documents(where_query)
        result = {"count": count, "items": list(drugs)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)



def get_query(drug_id, drug_name):
    regx = re.compile("^{}".format(drug_name), re.IGNORECASE)
    ret = {}
    if drug_name:
        ret["name"] = {
            "$regex": drug_name,
            "$options": "i"
        }
    if drug_id:
        ret["drugbank_id"] = drug_id
    return ret



def document(drug_id: str) -> dict:
    dirname = os.path.dirname(__file__)
    drugbank_dir = os.path.join(dirname, '../../drugbank_docs')
    file_path = os.path.join(drugbank_dir, drug_id + ".json")
    file = open(file_path)
    data = json.load(file)
    file.close()
    return data


def query_targets(user_query: str, page = None, pageSize = None):
    try:
        if not page:
            page = 0
        if not pageSize:
            pageSize = 25
        dbConnection = (Database())
        db = dbConnection.db
        targets = db.targets.find({
            "name": {
                "$regex": user_query,
                "$options": "i"
            }
        }).skip(page * pageSize).limit(pageSize)
        return GeneralWrapper.successResult(list(targets))
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)


def query_categories(user_query: str, page: int):
    try:    
        dbConnection = (Database())
        db = dbConnection.db
        where_query = {
            "name": {
                "$regex": user_query,
                "$options": "i"
            }
        }
        categories = db.categories.find(where_query).skip(page * 10) \
            .limit(10)
        count = db.categories.count_documents(where_query)
        result = {"count": count, "items": list(categories)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)



def drugbank_drugs_by_category(category_id, page):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        where_query = {
            "categories.drugbank_id": category_id
        }
        drugs = db.drugs.find(where_query, hint = [('categories.drugbank_id', pymongo.ASCENDING)]).skip(page * 10).limit(10)
        count = db.drugs.count_documents(where_query, hint = [('categories.drugbank_id', pymongo.ASCENDING)])
        result = {"count": count, "items": list(drugs)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)

