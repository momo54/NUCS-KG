import os
from pathlib import Path

PDF_DIR = Path("data")
CSV_DIR = Path("XP")

# Récupère tous les fichiers PDF sous data/
pdf_files = list(PDF_DIR.rglob("*.PDF"))

# Crée une liste des fichiers cibles CSV en conservant la hiérarchie
relative_paths = [f.relative_to(PDF_DIR) for f in pdf_files]
csv_paths = [CSV_DIR / p.with_suffix(".csv") for p in relative_paths]

rule all:
    input:
        [str(p) for p in csv_paths]

rule extract_ues:
    input:
        "data/{path}.PDF"
    output:
        "XP/{path}.csv"
    shell:
        """
        mkdir -p $(dirname {output})
        python extract_ues.py {input} {output}
        """
