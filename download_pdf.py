import os
import requests
from urllib.parse import unquote

# Liste des PDF à télécharger
PDF_URLS = [
    # Licence
    ("https://sciences-techniques.univ-nantes.fr/programme-l1-mip-parcours-informatique", "./data/licence2025/INFO_L1.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l1-informatique-pa","./data/licence2025/INFOPA_L1.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l1-mip-parcours-math-informatique", "./data/licence2025/INFOMATH_L1.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l1-info-maths-pa", "./data/licence2025/INFOMATHPA_L1.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l2-informatique-parcours-informatique", "./data/licence2025/INFO_L2.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l2-informatique-parcours-math-informatique", "./data/licence2025/INFOMATH_L2.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l2-informatique-parcours-cmi-optim", "./data/licence2025/CMI_L2.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l-as-2-info", "./data/licence2025/INFO_L2AS.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l3-informatique-parcours-informatique", "./data/licence2025/INFO_L3.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l3-informatique-parcours-math-informatique", "./data/licence2025/INFOMATH_L3.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l-as-3-info", "./data/licence2025/INFO_L3AS.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l3-cmi-optim", "./data/licence2025/CMI_L3.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l3-informatique-parcours-miage-classique", "./data/licence2025/MIAGE_L3.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l3-informatique-parcours-miage-alternance", "./data/licence2025/MIAGEALTERNANCE_L3.pdf"),
    ("https://sciences-techniques.univ-nantes.fr/programme-l-as-3-info", "./data/licence2025/INFO_L3AS.pdf"),


    # Masters M1
    ("https://sciences-techniques.univ-nantes.fr/programme-du-m1-alma", "./data/master2025/M1/ALMA_M1.PDF"),
    ("https://sciences-techniques.univ-nantes.fr/programme-du-m1-atal", "./data/master2025/M1/ATAL_M1.PDF"),
    ("https://sciences-techniques.univ-nantes.fr/programme-du-m1-oro", "./data/master2025/M1/ORO_M1.PDF"),
    ("https://sciences-techniques.univ-nantes.fr/programme-du-m1-data-sciences-ds", "./data/master2025/M1/DS_M1.PDF"),
    ("https://sciences-techniques.univ-nantes.fr/programme-du-m1-visual-computing-vico", "./data/master2025/M1/VICO_M1.PDF"),
    ("https://sciences-techniques.univ-nantes.fr/programme-m1-cmi-optim", "./data/master2025/M1/CMI_M1.PDF"),
    ("https://sciences-techniques.univ-nantes.fr/medias/fichier/m1-smart-computing-mention-informatique_1732713726216-pdf?ID_FICHE=2080272&INLINE=FALSE", "./data/master2025/M1/CMD_M1.PDF"),

    # Masters M2
    ("https://sciences-techniques.univ-nantes.fr/programme-du-m2-atal", "./data/master2025/M2/ATAL_M2.PDF"),
    ("https://sciences-techniques.univ-nantes.fr/programme-du-m2-alma", "./data/master2025/M2/ALMA_M2.PDF"),
    ("https://sciences-techniques.univ-nantes.fr/programme-du-m2-oro", "./data/master2025/M2/ORO_M2.PDF"),
    ("https://sciences-techniques.univ-nantes.fr/programme-du-m2-data-sciences-ds-polytech", "./data/master2025/M2/DS_M2.PDF"),
    ("https://sciences-techniques.univ-nantes.fr/programme-du-m2-visual-computing-vico-polytech", "./data/master2025/M2/VICO_M2.PDF"),
    ("https://sciences-techniques.univ-nantes.fr/programme-m2-cmi-optim", "./data/master2025/M2/CMI_M2.PDF")
]

def download_pdf(url, filepath):
    print(f"download {url} to {filepath}")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"✅ Enregistré : {filepath}")
    except Exception as e:
        print(f"❌ Échec pour {url} : {e}")

#print(PDF_URLS)

# Télécharger tous les fichiers
for url, path in PDF_URLS:
    download_pdf(url, path)
