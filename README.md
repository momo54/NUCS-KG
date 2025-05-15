# Generate from PDF, Knowledge Graph of Graduate programs...

## get the data

* `wget https://sciences-techniques.univ-nantes.fr/programme-l3-informatique-parcours-informatique -O./data/licence2025/l3.pdf`
* `wget https://sciences-techniques.univ-nantes.fr/programme-du-m1-alma -O  ./data/master2025/ALMA.PDF`

## Generate KG

* `python extract_ues.py ./data/master2025/ALMA.PDF ./XP/master2025/ALMA.csv`
* `python extract_ues.py ./data/licence2025/L3.pdf ./XP/licence2025/L3.csv`