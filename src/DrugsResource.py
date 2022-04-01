from typing import List


class DrugResource:
    def __init__(self, smiles: List[str], toxicity: dict, solubility: List[float], not_found_drugs: List[str]):
        self.smiles = smiles
        self.toxicity = toxicity
        self.solubility = solubility
        self.not_found_drugs = not_found_drugs


