import re
import json
import click
from pathlib import Path
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS
from extract_ues import extract_text_blocks

def extract_json_from_response(raw_response):
    match = re.search(r"{\s*\"code\"", raw_response)
    if match:
        json_text = raw_response[match.start():]
    else:
        json_text = raw_response
    json_text = re.sub(r"//.*", "", json_text)
    json_text = json_text.strip().strip("`")
    return json_text

def build_prompt():
    return PromptTemplate(
        input_variables=["bloc"],
        template="""Tu es un assistant chargé d'extraire une fiche de cours à partir d’un texte brut extrait d’un PDF.

Voici le texte :

{bloc}

Retourne un objet JSON strictement structuré avec les champs suivants (même si vides) :

- code
- label
- location
- level
- semester
- responsible (liste)
- hours
- prerequisite
- parcours
- evaluation
- obtention
- objective
- content
- methods
- language
- bibliography (liste)

Format attendu :

{{
  "code": "...",
  "label": "...",
  "location": "...",
  "level": "...",
  "semester": "...",
  "responsible": ["..."],
  "hours": "...",
  "prerequisite": "...",
  "parcours": "...",
  "evaluation": "...",
  "obtention": "...",
  "objective": "...",
  "content": "...",
  "methods": "...",
  "language": "...",
  "bibliography": ["..."]
}}

IMPORTANT : Ne réponds qu'avec l'objet JSON demandé.
N’ajoute aucun commentaire, explication, ou texte avant ou après.
Ne commence pas par "Voici la fiche" ni par "JSON brut :", ni par des triples backticks ```json.
"""
    )

def convert_json_to_ttl(data, ttl_file_path):
    EX = Namespace("http://example.org/course/")
    g = Graph()
    g.bind("ex", EX)
    g.bind("rdfs", RDFS)

    for ue in data:
        code = ue.get("code", "UNKNOWN")
        subj = URIRef(f"{EX}UE_{code}")
        g.add((subj, RDF.type, EX.UE))
        g.add((subj, EX.code, Literal(code)))
        g.add((subj, RDFS.label, Literal(ue.get("label", ""))))

        for field in ["location", "level", "semester", "hours", "prerequisite",
                      "parcours", "evaluation", "obtention", "objective",
                      "content", "methods", "language"]:
            if ue.get(field):
                g.add((subj, EX[field], Literal(ue[field])))

        for field in ["responsible", "bibliography"]:
            for item in ue.get(field, []):
                g.add((subj, EX[field], Literal(item)))

    g.serialize(destination=ttl_file_path, format="turtle")
    print(f"✅ Export RDF terminé : {ttl_file_path}")

def process_pdf(pdf_path, model_name, output_file, export_ttl):
    llm = Ollama(model=model_name)
    chain = LLMChain(llm=llm, prompt=build_prompt())
    blocs = extract_text_blocks(pdf_path)

    results = []
    for bloc in blocs:
        bloc = bloc.strip()
        if not bloc:
            continue
        try:
            print(f"⏳ Traitement : {bloc[:50]}...")
            json_result = chain.run({"bloc": bloc})
            clean_json = extract_json_from_response(json_result)
            data = json.loads(clean_json)
            results.append(data)
        except Exception as e:
            print("❌ Erreur de parsing :", e)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✅ Export JSON terminé : {output_file}")

    if export_ttl:
        ttl_file = Path(output_file).with_suffix(".ttl")
        convert_json_to_ttl(results, ttl_file)

@click.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option("--model", default="llama3.1:latest", help="Nom du modèle Ollama à utiliser.")
@click.option("--output", default="ue_extraction_output.json", help="Fichier de sortie JSON.")
@click.option("--to-ttl", is_flag=True, help="Exporter également en RDF Turtle (.ttl).")
def main(pdf_path, model, output, to_ttl):
    process_pdf(pdf_path, model, output, to_ttl)

if __name__ == "__main__":
    main()