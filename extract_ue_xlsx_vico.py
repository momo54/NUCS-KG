import pandas as pd
import re
import json
import os
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS
from urllib.parse import quote
import uuid


def normalize(text):
    text = str(text).strip().lower()
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = re.sub(r"\s+", " ", text)
    return text

def extract_ues_from_excel(filepath, output_json, output_ttl=None):
    df = pd.read_excel(filepath, sheet_name=0, header=None)
    filename = os.path.basename(filepath)
    level_match = re.search(r"_(L[123]|M[12])", filename)
    parcours_level = level_match.group(1) if level_match else "UNKNOWN"
    parcours_code = filename.split("_")[0] if "_" in filename else "UNKNOWN"

    ues = []
    raw_metadata_fields = {
        "langue d'enseignement": "language",
        "lieu d'enseignement": "location",
        "niveau": "level",
        "semestre": "semester",
        "responsable de la matière": "responsible",
        "responsable de l’ue": "responsible",
        "volume horaire total": "hours",
        "objectifs (résultats d'apprentissage)": "objective",
        "contenu": "content",
        "méthodes d’enseignement": "methods",
        "bibliographie": "bibliography",
        "ue pré-requise": "prerequisite",
        "ue pré-requise(s)": "prerequisite",
        "parcours d’études comprenant l’ue": "parcours",
        "pondération pour chaque matière": "evaluation",
        "obtention de l’ue": "obtention"
    }
    metadata_fields = {normalize(k): v for k, v in raw_metadata_fields.items()}

    current_ue = None
    start_parsing = False
    for i in range(len(df) - 1):
        row = df.iloc[i]
        next_row = df.iloc[i + 1]

        row_values = row.dropna().astype(str).tolist()
        next_first_col = str(next_row[0]).strip().lower() if pd.notna(next_row[0]) else ""

        if not start_parsing:
            if row_values and 'description des ue' in normalize(row_values[0]):
                start_parsing = True
            continue

        first_col = row_values[0] if len(row_values) > 0 else ""
        second_col = row_values[1] if len(row_values) > 1 else ""

        if normalize(next_first_col) in ["lieu d'enseignement", "langue d'enseignement"]:
            if current_ue:
                ues.append(current_ue)
            code = first_col if first_col else f"GEN-{uuid.uuid4().hex[:8]}"
            label = second_col if second_col else ""
            current_ue = {
                "code": code,
                "label": label,
                "parcours_level": parcours_level,
                "parcours_code": parcours_code
            }
        elif current_ue:
            key = normalize(first_col)
            value = second_col
            print(f"Checking key: '{key}' (raw: '{first_col}') — matches? {key in metadata_fields}")
            if not key:
                continue
            if key in metadata_fields:
                pred = metadata_fields[key]
                print(f"Parsed field: {pred} -> {value}")
                if pred in current_ue:
                    current_ue[pred] += f" / {value}"
                else:
                    current_ue[pred] = value

    if current_ue:
        ues.append(current_ue)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(ues, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(ues)} UEs written to {output_json}")

    if output_ttl:
        EX = Namespace("http://example.org/course/")
        g = Graph()
        g.bind("ex", EX)
        g.bind("rdfs", RDFS)

        for ue in ues:
            code = ue.get("code", "UNKNOWN")
            subj = URIRef(f"{EX}UE_{quote(code)}")
            g.add((subj, RDF.type, EX.UE))
            g.add((subj, EX.code, Literal(code)))
            label = ue.get("label", "") or code
            g.add((subj, RDFS.label, Literal(label)))
            for key, value in ue.items():
                if key in ["code", "label"]:
                    continue
                pred = EX[key]
                if " / " in value:
                    for v in value.split(" / "):
                        g.add((subj, pred, Literal(v.strip())))
                else:
                    g.add((subj, pred, Literal(value)))

        g.serialize(destination=output_ttl, format="turtle")
        print(f"✅ RDF TTL exported to {output_ttl}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract UE data from Excel and export as JSON or TTL")
    parser.add_argument("excel_file", help="Path to Excel file")
    parser.add_argument("output", help="Output file (.json or .ttl")
    args = parser.parse_args()

    if args.output.endswith(".json"):
        extract_ues_from_excel(args.excel_file, args.output)
    elif args.output.endswith(".ttl"):
        extract_ues_from_excel(args.excel_file, "_tmp_ue.json", args.output)
        os.remove("_tmp_ue.json")
    else:
        print("❌ Unsupported output format. Use .json or .ttl")
