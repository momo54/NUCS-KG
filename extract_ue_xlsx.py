import pandas as pd
import re
import json
import os
import sys
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS

def extract_ues_from_excel(excel_path, output_json, output_ttl=None):
    df = pd.read_excel(excel_path, sheet_name=0, header=None)
    filename = os.path.basename(excel_path)
    level_match = re.search(r"_(L[123]|M[12])", filename)
    parcours_level = level_match.group(1) if level_match else "UNKNOWN"
    parcours_code = filename.split("_")[0] if "_" in filename else "UNKNOWN"

    code_regex = re.compile(r"[XY][A-Z0-9]{6}")
    champ_to_predicate = {
        "Langue d’enseignement": "language",
        "Lieu d’enseignement": "location",
        "Responsable de la matière": "responsible",
        "Responsable de l’UE": "responsible",
        "Volume horaire total": "hours",
        "Objectifs (résultats d'apprentissage)": "objective",
        "Contenu": "content",
        "Méthodes d’enseignement": "methods",
        "Bibliographie": "bibliography",
        "Niveau": "level",
        "Semestre": "semester",
        "UE pré-requise": "prerequisite",
        "UE pré-requise(s)": "prerequisite",
        "Parcours d’études comprenant l’UE": "parcours",
        "Pondération pour chaque matière": "evaluation",
        "Obtention de l’UE": "obtention"
    }

    start_index = df[df.apply(lambda row: row.astype(str).str.contains("Description des UE").any(), axis=1)].index
    start_row = start_index[0] + 1 if not start_index.empty else 0

    ues = []
    current_ue = None

    for i in range(start_row, len(df)):
        row = df.iloc[i]
        row_values = row.dropna().astype(str).tolist()
        if not row_values:
            continue

        matched_code = next((val for val in row_values if code_regex.match(val.strip())), None)
        if matched_code or (not current_ue):
            if current_ue:
                ues.append(current_ue)
            current_ue = {"parcours_level": parcours_level, "parcours_code": parcours_code}
            if matched_code:
                current_ue["code"] = matched_code
                try:
                    label_index = row_values.index(matched_code) + 1
                    if label_index < len(row_values):
                        current_ue["label"] = row_values[label_index].strip()
                except:
                    pass
            continue

        if current_ue and len(row_values) >= 2:
            key, value = row_values[0].strip(), row_values[1].strip()
            if key in champ_to_predicate:
                predicate = champ_to_predicate[key]
                current_ue[predicate] = value
            else:
                current_ue.setdefault("autre", []).append({"key": key, "value": value})

    if current_ue:
        ues.append(current_ue)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(ues, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(ues)} fiches UE extraites et enregistrées dans {output_json}")

    if output_ttl:
        EX = Namespace("http://example.org/course/")
        g = Graph()
        g.bind("ex", EX)
        g.bind("rdfs", RDFS)

        for ue in ues:
            code = ue.get("code", "UNKNOWN")
            subj = URIRef(f"{EX}UE_{code}")
            g.add((subj, RDF.type, EX.UE))
            g.add((subj, EX.code, Literal(code)))
            if "label" in ue:
                g.add((subj, RDFS.label, Literal(ue["label"])))
            for k, v in ue.items():
                if k in ["code", "label"]:
                    continue
                if k == "autre":
                    for pair in v:
                        alt_key = pair['key'].replace("’", "'").replace("‘", "'").replace("ʼ", "'").strip()
                        pred_name = alt_key.lower().replace(" ", "_").replace("’", "").replace("'", "").replace("(", "").replace(")", "").replace("-", "_")
                        pred = EX[pred_name]
                        g.add((subj, pred, Literal(pair['value'])))
                else:
                    pred = EX[k]
                    g.add((subj, pred, Literal(v)))

        g.serialize(destination=output_ttl, format="turtle")
        print(f"✅ Export RDF TTL dans {output_ttl}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract UE data from Excel and export as JSON or TTL")
    parser.add_argument("excel_file", help="Path to Excel file")
    parser.add_argument("output", help="Output file (either .json or .ttl)")
    args = parser.parse_args()

    if args.output.endswith(".json"):
        extract_ues_from_excel(args.excel_file, args.output, None)
    elif args.output.endswith(".ttl"):
        extract_ues_from_excel(args.excel_file, "_tmp_ue.json", args.output)
        os.remove("_tmp_ue.json")
    else:
        print("❌ Format de sortie non supporté. Utilisez .json ou .ttl")
