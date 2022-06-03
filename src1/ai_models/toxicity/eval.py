# -*- coding: utf-8 -*-
"""Eval_Toxicity.ipynb

Vicent Ribas PhD
"""

### Dependencies:
### 1.- Deepchem
### 2.- rdkit


from typing import List

import numpy as np
#### Specific libs
from deepchem.data.datasets import NumpyDataset
from deepchem.feat.graph_features import ConvMolFeaturizer
from deepchem.models import GraphConvModel
##### General libs
from rdkit import Chem
import os

##### variable pointing to the model folder needs to be updated when deploying!
dirname = os.path.dirname(__file__)
model_dir = filename = os.path.join(dirname, 'model')


#### Hard-coding tasks to avoit problems
tasks = ['NR-AR', 'NR-AR-LBD', 'NR-AhR', 'NR-Aromatase', 'NR-ER', 'NR-ER-LBD', 'NR-PPAR-gamma', 'SR-ARE', 'SR-ATAD5',
         'SR-HSE', 'SR-MMP', 'SR-p53']

#### Load model
model = GraphConvModel(12, mode='classification', model_dir=model_dir, batch_size=128)
model.restore()

#### Compute features

feat = ConvMolFeaturizer()


def compute_features(smiles: List[str]) -> np.array:
    """Compute the features for a list of molecules

    Args:
        smiles ([str]): SMILES of molecules to evaluate
    Returns:
        (np.array) Features for each molecule
    """
    # Create the dataset
    try:
        mols = [Chem.MolFromSmiles(x) for x in smiles]
        return np.array(feat.featurize(mols))
    except:
        return ('error in featurization')


#### Model evaluation
def invoke_model(feats: np.array, smiles: List[str]) -> [dict]:
    """Invoke the model

    Args:
        feats (np.array): Features for the model
        smiles ([str]): SMILES
    Returns:
        ([dict]) Return the data
    """
    # Turn the features into a Numpy dataset
    try:
        dataset = NumpyDataset(feats, n_tasks=len(tasks))

        # Run inference
        y_pred = model.predict(dataset)

        # Get the output
        tox_liklihood = y_pred[:, :, 1]
        output = dict(zip(tasks, tox_liklihood.T))
        return output
    except:
        return ('Error in model evaluation')


def run_inference(smiles: List[str]) -> [dict]:
    """Run inference on the machine learning models
    Args:
        smiles ([str]): List of SMILES to evaluate
    Returns:
        ([dict]) Dictionary of the toxicity liklihoods
    """
    try:
        feats = compute_features(smiles)
        return invoke_model(feats, smiles)
    except:
        return ('Error in model inference')

#### Execution (TBD how in BE)
# smiles = ['C1=C(N=C(C(=O)N1)C(=O)N)F', 'CCC(CC)COC(=O)C(C)NP(=O)(OCC1C(C(C(O1)(C#N)C2=CC=C3N2N=CN=C3N)O)O)OC4=CC=CC=C4']

# run_inference(smiles)
