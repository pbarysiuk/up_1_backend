from DeepPurpose import DTI as models
from DeepPurpose import utils
import os

def invoke_model(drugs: list, target: str):
    drug_encoding, target_encoding = 'CNN', 'Transformer'
    pconfig = utils.generate_config(drug_encoding, target_encoding, transformer_n_layer_target=8)
    model = models.model_initialize(**pconfig)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'model.pt')
    model.load_pretrained(filename)
    y = [1 for x in drugs]
    X_pred = utils.data_process([x["id"] for x in drugs],
                                target,
                                y,
                                drug_encoding,
                                target_encoding,
                                split_method='no_split')
    return model.predict(X_pred)


def run_inference(drugs: list, target: str):
    pred = invoke_model(drugs, target)
    ret = []
    for i, drug in enumerate(drugs):
        ret.append({"label": drug["label"], "value": pred[i]})
    return ret
