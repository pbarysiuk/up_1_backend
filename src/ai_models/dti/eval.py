from DeepPurpose import DTI as models
from DeepPurpose import utils


def invoke_model(smiles: list, target: str):
    drug_encoding, target_encoding = 'CNN', 'Transformer'
    pconfig = utils.generate_config(drug_encoding, target_encoding, transformer_n_layer_target=8)
    model = models.model_initialize(**pconfig)
    model.load_pretrained('./DTI_model/model.pt')
    y = [1 for x in smiles]
    X_pred = utils.data_process(smiles, target, y,
                                drug_encoding, target_encoding,
                                split_method='no_split')
    return model.predict(X_pred)


def run_inference(drugs: list, target: str):
    pred = invoke_model([x["smiles"] for x in drugs], target)
    ret = []
    for drug, i in drugs:
        ret.append({"name": drug["name"], "value": pred[i]})
    return ret
