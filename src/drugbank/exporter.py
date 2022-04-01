import csv

from flask import send_file

from src.shared import database


def execute():
    db = database.get_connection()
    drugs = db.drugs.find({}, ['carriers', 'enzymes', 'targets', 'calculated_properties'])
    header = ['smiles', 'amino_acid_sequence']

    with open('export.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        for drug in drugs:
            if "calculated_properties" not in drug \
                    or drug["calculated_properties"] is None \
                    or "SMILES" not in drug["calculated_properties"]:
                continue

            smiles = drug["calculated_properties"]["SMILES"]

            amino_acid_sequences = get_amino_acid_sequences(drug)

            for sequence in amino_acid_sequences:
                writer.writerow([smiles, sequence])

    return send_file('export.csv',
                     mimetype='text/csv',
                     attachment_filename='export.csv',
                     as_attachment=True)


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
