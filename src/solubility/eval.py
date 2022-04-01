# -*- coding: utf-8 -*-
"""Eval_Solubility.ipynb

Vicent Ribas PhD
"""

### Dependencies:
### 1.- Deepchem
### 2.- rdkit

#### General libraries

from typing import List

import numpy as np
#### Specific libraries
from deepchem.data.datasets import NumpyDataset
from deepchem.feat.graph_features import ConvMolFeaturizer
from deepchem.models import GraphConvModel
from rdkit import Chem
import os

##### Variable pointing to the model folder needs to be updated when deploying!
dirname = os.path.dirname(__file__)
print("dirname!", dirname)
model_dir = filename = os.path.join(dirname, 'model')

#### Load model

model = GraphConvModel(1, mode='regression', model_dir=model_dir, batch_size=50)
model.restore()

#### Define featurizer

feat = ConvMolFeaturizer()


def compute_features(smiles: List[str]) -> np.array:
    """Compute the features for a list of molecules

    Args:
        smiles ([str]): SMILES of molecules to evaluate
    Returns:
        (np.array) Features for each molecule
    """
    # Create the dataset
    mols = [Chem.MolFromSmiles(x) for x in smiles]
    return np.array(feat.featurize(mols))


#### Define model invokation
def invoke_model(feats: np.array, smiles: List[str]) -> [dict]:
    """Invoke the model

    Args:
        feats (np.array): Features for the model
        smiles ([str]): SMILES
    Returns:
        ([dict]) Return the data
    """
    # Turn the features into a Numpy dataset
    dataset = NumpyDataset(feats)

    # Run inference
    scores = model.predict(dataset)

    # Get the output
    # scores = y_pred[:, 1]
    return [float(i[0]) for i in scores]


#### Inference function

def run_inference(smiles: List[str]) -> [dict]:
    """Run inference on the machine learning models
    Args:
        smiles ([str]): List of SMILES to evaluate
    Returns:
        ([dict]) Dictionary of the solubilities
    """
    feats = compute_features(smiles)
    return invoke_model(feats, smiles)

#### Execution to be changed in BE (tested with Favipiravir and Remdesivir)
# smiles = ['C1=C(N=C(C(=O)N1)C(=O)N)F', 'CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4']
# run_inference(smiles)

##### Output
# {0.96714014: -0.28310442,
# 'smiles': ['C1=C(N=C(C(=O)N1)C(=O)N)F',
#  'CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4']}
