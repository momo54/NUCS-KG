import pdfplumber
import re
import json
import os
import argparse

def is_valid_ku_title(line):
    line = line.strip()
    if re.search(r'\.{4,}', line):  # Sommaire
        return False
    if re.search(r'\s\d{1,3}\s*$', line):  # Page #
        return False
    if len(line) < 10:
        return False
    # Nouveau : on exclut les titres contenant des numéros internes (ex: 2b i.)
    if re.match(r'^[A-Z]{2,3}-.*\d+[a-z]?', line):
        return False
    return True


def extract_all_ku_titles(pdf_path):
#    ku_title_pattern = re.compile(r'^([A-Z]{2,3}-[^:\n:]+:\s?.+)$')
    ku_title_pattern = re.compile(
    r'^([A-Z]{2,3}-[^:\n]+:\s?.+|MSF-Calculus|SPD-SEP/Web)$'
)
    titles = []

    # with pdfplumber.open(pdf_path) as pdf:
    #     for page in pdf.pages:
    #         text = page.extract_text()
    #         if not text:
    #             continue
    #         for line in text.splitlines():
    #             if ku_title_pattern.match(line.strip()) and is_valid_ku_title(line):
    #                 titles.append(line.strip())

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.splitlines()

            # 🔧 Patch pour corriger la ligne corrompue
            for i, line in enumerate(lines):
                if "SEC-Foundatio22ns: Foundational Security" in line:
                    print("[⚠️] Auto-correcting corrupted SEC-Foundations KU title.")
                    lines[i] = "SEC-Foundations: Foundational Security"

            # Lecture des lignes après correction
            for line in lines:
                if ku_title_pattern.match(line.strip()) and is_valid_ku_title(line):
                    titles.append(line.strip())

    print(f"[🔎] Detected {len(titles)} KU titles.")
    return titles

def extract_knowledge_units(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        lines = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                page_lines = text.splitlines()

                # 🔧 PATCH : corriger la ligne corrompue si présente
                for i, line in enumerate(page_lines):
                    if "SEC-Foundatio22ns: Foundational Security" in line:
                        print("[⚠️] Auto-correcting corrupted SEC-Foundations KU title.")
                        page_lines[i] = "SEC-Foundations: Foundational Security"

                lines.extend(page_lines)

    # 🎯 Motif pour détecter les titres de KUs
    ku_title_pattern = re.compile(
        r'^([A-Z]{2,3}-[^:\n]+:\s?.+|MSF-Calculus|SPD-SEP/Web|SEC-Foundations: Foundational Security)$'
    )

    # 🔎 Motif pour les sections (core blocks)
    section_match = re.compile(
        r'^(CS|KA|Non)[ -]?Core:|^Illustrative Learning Outcomes:',
        re.IGNORECASE
    )

    ku_indices = []

    for i, line in enumerate(lines):
        if ku_title_pattern.match(line.strip()) and is_valid_ku_title(line):
            window = lines[i+1:i+30]  # fenêtre de 30 lignes pour détecter la section
            if any(section_match.search(l.strip()) for l in window):
                ku_indices.append(i)

    knowledge_units = []

    for idx, start in enumerate(ku_indices):
        end = ku_indices[idx + 1] if idx + 1 < len(ku_indices) else len(lines)
        title = lines[start].strip()
        ku_block = "\n".join(lines[start+1:end])
        sections = extract_sections(ku_block)
        knowledge_units.append({
            "title": title,
            **sections
        })

    print(f"[✔] Total valid KUs found: {len(knowledge_units)}")
    return knowledge_units

def extract_knowledge_units_almost(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        lines = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines.extend(text.splitlines())
                # for i, line in enumerate(lines):
                #     if ": Foundational Security"  in line:
                #         print(f"[DEBUG] Line {i}: {repr(line)}")

    # Motif pour identifier un titre de KU : XX-...: ... ou XXX-...: ...
    ku_title_pattern = re.compile(r'^([A-Z]{2,3}-[^:\n]+:\s?.+|MSF-Calculus|SPD-SEP/Web)$')

    # Motif pour identifier les sections à suivre (CS Core, KA Core, Non-core, etc.)
    section_match = re.compile(
        r'^(CS|KA|Non)[ -]?Core:|^Illustrative Learning Outcomes:',
        re.IGNORECASE
    )

    ku_indices = []

    for i, line in enumerate(lines):
        if ku_title_pattern.match(line.strip()) and is_valid_ku_title(line):
            window = lines[i+1:i+30]
            if any(section_match.search(l.strip()) for l in window):
                ku_indices.append(i)

    knowledge_units = []

    for idx, start in enumerate(ku_indices):
        end = ku_indices[idx + 1] if idx + 1 < len(ku_indices) else len(lines)
        title = lines[start].strip()
        ku_block = "\n".join(lines[start+1:end])
        sections = extract_sections(ku_block)
        knowledge_units.append({
            "title": title,
            **sections
        })

    print(f"[✔] Total valid KUs found: {len(knowledge_units)}")
    return knowledge_units

def extract_knowledge_units_nearly(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        lines = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines.extend(text.splitlines())

    # On détecte les titres de la forme XX-...: ... ou XXX-...: ...
    ku_title_pattern = re.compile(r'^([A-Z]{2,3}-[^:\n]+:\s?.+)$')
    ku_indices = []

    # Détection des lignes contenant un titre de KU suivi de n'importe quelle section "* Core:"
    for i, line in enumerate(lines):
        if ku_title_pattern.match(line.strip()) and is_valid_ku_title(line):
            # Cherche une section * Core: dans les 10 lignes suivantes
            window = lines[i+1:i+11]
            if any(re.match(r'^\s*(CS|KA) Core:', l.strip(), re.IGNORECASE) for l in window):
                ku_indices.append(i)

    knowledge_units = []

    for idx, start in enumerate(ku_indices):
        end = ku_indices[idx + 1] if idx + 1 < len(ku_indices) else len(lines)
        title = lines[start].strip()
        ku_block = "\n".join(lines[start+1:end])
        sections = extract_sections(ku_block)

        knowledge_units.append({
            "title": title,
            **sections
        })

    print(f"[✔] Total valid KUs found: {len(knowledge_units)}")
    return knowledge_units



def extract_knowledge_units_orig(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(page.extract_text() for page in pdf.pages)

    ku_pattern = re.compile(
        r'^([A-Z]{2,3}-[^\n:]+:\s?.+?)\s*\n\s*CS Core:',
        re.MULTILINE
    )     
    ku_starts = list(ku_pattern.finditer(full_text))

    knowledge_units = []

    for i, ku_match in enumerate(ku_starts):
        ku_title = ku_match.group(1).strip()
        ku_start = ku_match.end()
        ku_end = ku_starts[i + 1].start() if i + 1 < len(ku_starts) else len(full_text)
        ku_block = full_text[ku_start:ku_end]

        sections = extract_sections(ku_block)

        knowledge_units.append({
            "title": ku_title,
            **sections
        })

    return knowledge_units

def extract_sections(ku_text):
    section_titles = ["CS Core:", "KA Core:", "Non-core:", "Illustrative Learning Outcomes:"]
    pattern = "|".join(re.escape(title) for title in section_titles)
    section_pattern = re.compile(rf"({pattern})")

    sections = {}
    matches = list(section_pattern.finditer(ku_text))

    # Tri naturel par ordre de position
    seen = set()
    for i, match in enumerate(matches):
        label = match.group(1).rstrip(":")
        if label in seen:
            continue  # Ignore doublon
        seen.add(label)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(ku_text)
        content = ku_text[start:end].strip()
        if content:
            sections[label] = content

    return sections



def extract_sections_orig(ku_text):
    section_titles = ["CS Core:", "KA Core:", "Non-core:", "Illustrative Learning Outcomes:"]
    pattern = "|".join(re.escape(title) for title in section_titles)
    section_pattern = re.compile(rf"({pattern})")

    sections = {}
    matches = list(section_pattern.finditer(ku_text))

    for i, match in enumerate(matches):
        label = match.group(1).rstrip(":")
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(ku_text)
        sections[label] = ku_text[start:end].strip()

    return sections


def save_as_json(kus, output_file):
    with open(output_file, "w") as f:
        json.dump(kus, f, indent=2, ensure_ascii=False)


def save_as_txt(kus, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for i, ku in enumerate(kus, 1):
        filename = f"KU_{i:02d}_{ku['title'].replace(' ', '_').replace(':','')}.txt"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            f.write(f"{ku['title']}\n\n")
            for sec in ["CS Core", "KA Core", "Non-core", "Illustrative Learning Outcomes"]:
                content = ku.get(sec)
                if content:
                    f.write(f"--- {sec} ---\n{content}\n\n")

def main_orig():
    import argparse
    import os
    import json

    parser = argparse.ArgumentParser(description="Extract Knowledge Units from PDF")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("--outdir", default="output", help="Output directory")
    parser.add_argument("--json", default="kus.json", help="JSON output file name")
    parser.add_argument("--compare", action="store_true", help="Compare title-only vs full KU extraction")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    # Étape 1 : Extraire tous les titres (bruts, sans sections)
    print("\n[1] Extracting all KU titles (title-only)...")
    all_titles = extract_all_ku_titles(args.pdf)
    with open(os.path.join(args.outdir, "ku_titles_detected.txt"), "w") as f:
        for t in all_titles:
            f.write(t + "\n")
    print(f"[✔] Saved {len(all_titles)} KU titles to ku_titles_detected.txt")

    # Étape 2 : Extraire les KUs complètes (avec sections)
    print("\n[2] Extracting full KU blocks (with CS/KA/Non/ILO sections)...")
    kus = extract_knowledge_units(args.pdf)
    with open(os.path.join(args.outdir, args.json), "w") as f:
        json.dump(kus, f, indent=2, ensure_ascii=False)
    print(f"[✔] Saved {len(kus)} full KUs to {os.path.join(args.outdir, args.json)}")

    # Étape 3 : Comparaison facultative
    if args.compare:
        print("\n[3] Comparing title-only and full KU extraction...")
        found_titles = set(t["title"] for t in kus)
        all_titles_set = set(all_titles)

        missing = all_titles_set - found_titles
        extra = found_titles - all_titles_set

        print(f"\n[🔍] Comparison result:")
        print(f" - ✅ Total KU titles (title-only): {len(all_titles_set)}")
        print(f" - ✅ Total full KUs (with sections): {len(found_titles)}")

        if missing:
            print(f"\n❗ Missing from full KU extraction: {len(missing)} ({len(missing)/len(all_titles_set)*100:.1f}%)")
            for t in sorted(missing):
                print(f"   - {t}")
            with open(os.path.join(args.outdir, "missing_titles.txt"), "w") as f:
                for t in sorted(missing):
                    f.write(t + "\n")
            print(f"📝 Saved missing titles to {args.outdir}/missing_titles.txt")

        if extra:
            print(f"\n⚠️ Unexpected titles in full extraction (not found in title-only): {len(extra)}")
            for t in sorted(extra):
                print(f"   + {t}")

def main():
    import argparse
    import os
    import json
    from collections import Counter

    parser = argparse.ArgumentParser(description="Extract Knowledge Units from PDF")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("--outdir", default="XP", help="Output directory")
    parser.add_argument("--json", default="kus.json", help="JSON output file name")
    parser.add_argument("--compare", action="store_true", help="Compare title-only vs full KU extraction")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    # Étape 1 : Extraire tous les titres (title-only)
    print("\n[1] Extracting all KU titles (title-only)...")
    all_titles = extract_all_ku_titles(args.pdf)
    with open(os.path.join(args.outdir, "ku_titles_detected.txt"), "w") as f:
        for t in all_titles:
            f.write(t + "\n")
    print(f"[✔] Saved {len(all_titles)} KU titles to ku_titles_detected.txt")

    # Étape 2 : Extraction complète avec sections
    print("\n[2] Extracting full KU blocks (with CS/KA/Non/ILO sections)...")
    kus = extract_knowledge_units(args.pdf)
    with open(os.path.join(args.outdir, args.json), "w") as f:
        json.dump(kus, f, indent=2, ensure_ascii=False)
    print(f"[✔] Saved {len(kus)} full KUs to {os.path.join(args.outdir, args.json)}")

    # Étape 3 : Comparaison optionnelle
    if args.compare:
        print("\n[3] Comparing title-only and full KU extraction...")
        found_titles = set(t["title"] for t in kus)
        all_titles_set = set(all_titles)

        missing = all_titles_set - found_titles
        extra = found_titles - all_titles_set

        print(f"\n[🔍] Comparison result:")
        print(f" - ✅ Total KU titles (title-only): {len(all_titles_set)}")
        print(f" - ✅ Total full KUs (with sections): {len(found_titles)}")

        if missing:
            print(f"\n❗ Missing from full KU extraction: {len(missing)} ({len(missing)/len(all_titles_set)*100:.1f}%)")
            for t in sorted(missing):
                print(f"   - {t}")
            with open(os.path.join(args.outdir, "missing_titles.txt"), "w") as f:
                for t in sorted(missing):
                    f.write(t + "\n")
            print(f"📝 Saved missing titles to {args.outdir}/missing_titles.txt")

        if extra:
            print(f"\n⚠️ Unexpected titles in full extraction (not found in title-only): {len(extra)}")
            for t in sorted(extra):
                print(f"   + {t}")

    # Étape 4 : Comptage par Knowledge Area
    print("\n[4] Verifying Knowledge Unit counts per Knowledge Area...")
    expected_per_area = {
        "AI": 12, "AL": 5, "AR": 11, "DM": 13, "FPL": 22,
        "GIT": 12, "HCI": 6, "MSF": 5, "NC": 8, "OS": 14,
        "PDC": 5, "SDF": 5, "SE": 9, "SEC": 7, "SEP": 11,
        "SF": 9, "SPD": 8,
    }

    title_counts = Counter(ku['title'].split('-')[0] for ku in kus)

    print("\n[📊] Knowledge Units count per Knowledge Area:\n")
    missing_report = {}
    for area, expected_count in expected_per_area.items():
        found = title_counts.get(area, 0)
        diff = expected_count - found
        status = "✅" if diff == 0 else f"❗ MISSING {diff}"
        print(f" - {area:<4}: {found:>2} / {expected_count} {status}")
        if diff > 0:
            missing_report[area] = diff

    if missing_report:
        print("\n❗ Areas with missing KUs:")
        for area, diff in missing_report.items():
            print(f"   - {area}: {diff} missing")

        with open(os.path.join(args.outdir, "missing_per_area.json"), "w") as f:
            json.dump(missing_report, f, indent=2)
        print(f"📝 Saved per-area missing report to {args.outdir}/missing_per_area.json")


if __name__ == "__main__":
    main()
