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
            amino_acid_sequences = list()

            if "carriers" in drug:
                for carrier in drug["carriers"]:
                    for polypeptide in carrier["polypeptides"]:
                        amino_acid_sequences.append(polypeptide["amino_acid_sequence"])
            if "targets" in drug:
                for target in drug["targets"]:
                    for polypeptide in target["polypeptides"]:
                        amino_acid_sequences.append(polypeptide["amino_acid_sequence"])

            if "enzymes" in drug:
                for enzyme in drug["enzymes"]:
                    for polypeptide in enzyme["polypeptides"]:
                        amino_acid_sequences.append(polypeptide["amino_acid_sequence"])

            for sequence in amino_acid_sequences:
                writer.writerow([smiles, sequence])

    return send_file('export.csv',
                     mimetype='text/csv',
                     attachment_filename='export.csv',
                     as_attachment=True)
