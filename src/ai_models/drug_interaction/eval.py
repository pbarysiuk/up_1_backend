import os

import deepchem as dc
import numpy as np
from tensorflow import keras
from tensorflow_addons.optimizers import AdamW
from src.ai_models.drug_interaction.model.assets.legend import get as get_legend

featurizer = dc.feat.CircularFingerprint()

##### Variable pointing to the model
dirname = os.path.dirname(__file__)
model_dir = filename = os.path.join(dirname, 'model')

model = keras.models.load_model(model_dir, custom_objects={'AdamW': AdamW})


def invoke_model(drugs: np.array) -> [float]:
    x = np.transpose(drugs)
    x = x.reshape(1, 64, 64, 1)
    scores = model.predict(x) * 100
    legend = get_legend()
    return [{"label": legend[i+1], "value":round(x, 3)} for i, x in enumerate(scores.astype(np.float)[0])]


def run_inference(smile1, smile2):
    drug1 = featurizer(smile1)
    drug2 = featurizer(smile2)
    drugs = np.array([np.transpose(drug1), np.transpose(drug2)])
    return invoke_model(drugs)
