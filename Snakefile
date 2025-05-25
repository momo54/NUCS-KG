import os
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("XP")

# Récupère tous les fichiers PDF sous data/
xlsx_files = list(DATA_DIR.rglob("*.xlsx"))

print(xlsx_files)

# Crée une liste des fichiers cibles CSV en conservant la hiérarchie
relative_paths = [f.relative_to(DATA_DIR) for f in xlsx_files]
ttl_paths = [OUT_DIR / p.with_suffix(".ttl") for p in relative_paths]

print(ttl_paths)

# Fichier final fusionné et anonymisé
MERGED_FILE = OUT_DIR / "all.ttl"
ANONYMIZED_FILE = OUT_DIR / "all-anonymized.ttl"


rule all:
    input:
        [str(p) for p in ttl_paths]

rule extract_ues:
    input:
        "data/{path}.xlsx"
    output:
        "XP/{path}.ttl"
    shell:
        """
        mkdir -p $(dirname {output})
        python extract_ue_xlsx_uni.py  {input} {output}
        """

rule merge_ttls:
    input:
        [str(p) for p in ttl_paths]
    output:
        str(MERGED_FILE)
    shell:
        """
        python merge_ttl.py -o {output} {OUT_DIR}
        """

rule anonymize_ttl:
    input:
        str(MERGED_FILE)
    output:
        str(ANONYMIZED_FILE)
    shell:
        """
        python anonymize.py {input} {output}
        """
