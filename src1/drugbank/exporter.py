import csv
from random import randint
from flask import send_file

from src.shared import database


def export_smiles_amino_acid_sequences():
    db = database.get_connection()
    drugs = db.drugs.find({}, ['carriers', 'enzymes', 'targets', 'calculated_properties'])
    header = ['smiles', 'amino_acid_sequence']
    smiles_sequences = get_smile_sequence(drugs)
    return create_csv(smiles_sequences, header)


def export_false_smiles_amino_acid_sequences():
    db = database.get_connection()
    drugs = db.drugs.find({}, ['carriers', 'enzymes', 'targets', 'calculated_properties'])
    header = ['smiles', 'amino_acid_sequence']
    smiles_sequences = get_smile_sequence(drugs)
    fake_smiles_sequences = generate_fake_smile_sequences(smiles_sequences)
    return create_csv(fake_smiles_sequences, header)


def create_csv(fake_smiles_sequences, header):
    with open('export.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for smile_sequence in fake_smiles_sequences:
            writer.writerow(smile_sequence)
    return send_file('export.csv',
                     mimetype='text/csv',
                     attachment_filename='export.csv',
                     as_attachment=True)


def generate_fake_smile_sequences(smiles_sequences):
    fake_smiles_sequences = list()
    for smile_sequence in smiles_sequences:
        ran1 = randint(0, len(smiles_sequences)-1)
        ran2 = randint(0, len(smiles_sequences)-1)
        while [smiles_sequences[ran1][0], smiles_sequences[ran2][1]] in smile_sequence:
            ran1 = randint(0, len(smiles_sequences))
            ran2 = randint(0, len(smiles_sequences))
        fake_smiles_sequences.append([smiles_sequences[ran1][0], smiles_sequences[ran2][1]])
    return fake_smiles_sequences


def get_smile_sequence(drugs):
    data = list()
    for drug in drugs:
        if "calculated_properties" not in drug \
                or drug["calculated_properties"] is None \
                or "SMILES" not in drug["calculated_properties"]:
            continue

        smiles = drug["calculated_properties"]["SMILES"]

        amino_acid_sequences = get_amino_acid_sequences(drug)

        for sequence in amino_acid_sequences:
            data.append([smiles, sequence])
    return data


def get_amino_acid_sequences(drug):
    amino_acid_sequences = list()
    attributes = ["carriers", "targets", "enzymes"]
    for attribute in attributes:
        if attribute in drug:
            for attr in drug[attribute]:
                for polypeptide in attr["polypeptides"]:
                    if polypeptide["amino_acid_sequence"] not in amino_acid_sequences:
                        amino_acid_sequences.append(polypeptide["amino_acid_sequence"].split("\n", 1)[1])

    return amino_acid_sequences
