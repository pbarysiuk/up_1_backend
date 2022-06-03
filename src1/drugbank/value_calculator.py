from src.shared import database
import re


def calculator():
    db = database.get_connection()
    drugs = db.drugs.find()
    ret = {
        "experimental_properties": {
            "Water Solubility": {
                "min": None,
                "max": None,
            },
            "Melting Point": {
                "min": None,
                "max": None,
            },
            "Boiling Point": {
                "min": None,
                "max": None,
            },
            "logP": {
                "min": None,
                "max": None,
            },
            "logS": {
                "min": None,
                "max": None,
            },
            "caco2 Permeability": {
                "min": None,
                "max": None,
            },
            "pKa": {
                "min": None,
                "max": None,
            },
        },
        "calculated_properties": {
            "logP": {
                "min": None,
                "max": None,
            },
            "Molecular Weight": {
                "min": None,
                "max": None,
            },
            "Polar Surface Area (PSA)": {
                "min": None,
                "max": None,
            },
            "Refractivity": {
                "min": None,
                "max": None,
            },
            "Polarizability": {
                "min": None,
                "max": None,
            },
            "pKa (strongest acidic)": {
                "min": None,
                "max": None,
            },
            "Physiological Charge": {
                "min": None,
                "max": None,
            },
            "ALOGPS": {
                "logP": {
                    "min": None,
                    "max": None,
                },
                "logS": {
                    "min": None,
                    "max": None,
                },
                "Water Solubility": {
                    "min": None,
                    "max": None,
                }
            },
        },

    }
    for drug in drugs:
        for attribute in ret.keys():
            for property in ret[attribute].keys():
                if property == "ALOGPS":
                    for subproperty in ret[attribute][property]:
                        if attribute not in drug or drug[attribute] is None or \
                                property not in drug[attribute] or drug[attribute][property] is None or \
                                subproperty not in drug[attribute][property] or \
                                drug[attribute][property][subproperty] is None:
                            continue
                        values = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", drug[attribute][property][subproperty])

                        if len(values) == 0:
                            continue
                        value = float(values[0])
                        max = ret[attribute][property][subproperty]["max"]
                        min = ret[attribute][property][subproperty]["min"]
                        if max is None or value > max:
                            ret[attribute][property][subproperty]["max"] = value
                        if min is None or value < min:
                            ret[attribute][property][subproperty]["min"] = value
                else:
                    if drug[attribute] is None or property not in drug[attribute]:
                        continue
                    values = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", drug[attribute][property])

                    try:
                        if len(values) == 0:
                            continue

                        value = float(values[0])
                        max = ret[attribute][property]["max"]
                        min = ret[attribute][property]["min"]
                        if max is None or value > max:
                            ret[attribute][property]["max"] = value
                        if min is None or value < min:
                            ret[attribute][property]["min"] = value
                    except ValueError:
                        print(values)
    return ret
