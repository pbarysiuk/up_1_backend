from pubchempy import get_compounds

from src.solubility.eval import run_inference as run_solubility
from src.toxicity.eval import run_inference as run_toxicity


def get_data(smiles: [str]) -> dict:
    solubility = run_solubility(smiles)
    toxicity = run_toxicity(smiles)
    output = dict()
    output['smiles'] = smiles
    output['solubility'] = solubility
    output['toxicity'] = dict()
    for key in toxicity:
        output['toxicity'][key] = list(map(lambda x: float(x), toxicity[key]))
    return output


def eval(drugnames: str):
    smiles = []
    drug_names_list = drugnames.split(":")
    not_found_drugs = []
    for drug_name in drug_names_list:
        try:
            drug_compounds = get_compounds(drug_name, 'name')
            smiles.append(drug_compounds[0].canonical_smiles)
        except:
            not_found_drugs.append(drug_name)

    if len(smiles) == 0 and len(not_found_drugs) > 0:
        return "Drugs not found: {}".format(not_found_drugs)

    data = get_data(smiles)
    found_drugs = list(filter(lambda x: x not in not_found_drugs, drug_names_list))
    output = dict()
    if (len(not_found_drugs)) > 0:
        output['not_found_drugs'] = not_found_drugs

    for idx, val in enumerate(found_drugs):
        output[val] = dict()
        output[val]['smiles'] = data['smiles'][idx]
        output[val]['solubility'] = data['solubility'][idx]
        output[val]['toxicity'] = [{task: value[idx]} for task, value in data['toxicity'].items()]

    return output
