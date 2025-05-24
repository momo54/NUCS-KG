from langchain.llms import Ollama  # Remplace par ChatGroq si besoin
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from extract_ues import extract_text_blocks
import re
import pdfplumber
import json

import re
import json

def extract_json_from_response(raw_response):
    # Supprimer texte avant le JSON
    match = re.search(r"{\\s*\"code\"", raw_response)
    if match:
        json_text = raw_response[match.start():]
    else:
        json_text = raw_response

    # Supprimer les commentaires de type `// ...`
    json_text = re.sub(r"//.*", "", json_text)

    # Supprimer les backticks éventuels
    json_text = json_text.strip().strip("`")

    return json_text


# === PARAMÈTRES ===
PDF_PATH = "data/master2025/M1/ALMA_M1.pdf"
MODEL_NAME = "llama3.1:latest"  # ou "mixtral", "llama2", etc.

# === INITIALISATION DU LLM ===
llm = Ollama(model=MODEL_NAME)

# === PROMPT TEMPLATE ===
base_prompt = """Tu es un assistant chargé d'extraire une fiche de cours à partir d’un texte brut extrait d’un PDF.

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

prompt = PromptTemplate(input_variables=["bloc"], template=base_prompt)
chain = LLMChain(llm=llm, prompt=prompt)


blocs = extract_text_blocks(PDF_PATH)

# === TRAITEMENT DES BLOCS ===
results = []
for bloc in blocs:
    bloc = bloc.strip()
    if not bloc:
        continue
    try:
        print(f"⏳ Traitement : {bloc[:50]}...")
        json_result = chain.run({"bloc": bloc})

        print("✅ Réponse LLM obtenue.")
        print("JSON brut :", json_result)

        clean_json = extract_json_from_response(json_result)
        data = json.loads(clean_json)

        results.append(data)
    except Exception as e:
        print("❌ Erreur de parsing pour un bloc :", e)

# === EXPORT FINAL ===
with open("ue_extraction_output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ Export terminé : ue_extraction_output.json")
