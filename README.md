# Generate from PDF, Knowledge Graph of Graduate programs...

## get the data

* `wget https://sciences-techniques.univ-nantes.fr/programme-l3-informatique-parcours-informatique -O./data/licence2025/l3.pdf`

programme des masters M1: 

* `wget https://sciences-techniques.univ-nantes.fr/programme-du-m1-alma -O  ./data/master2025/M1/ALMA_M1.PDF`
* `wget https://sciences-techniques.univ-nantes.fr/programme-du-m1-atal -O ./data/master2025/M1/ATAL_M1.PDF`
* `wget https://sciences-techniques.univ-nantes.fr/programme-du-m1-oro -O ./data/master2025/M1/ORO_M1.PDF`
* `wget https://sciences-techniques.univ-nantes.fr/programme-du-m1-data-sciences-ds -O ./data/master2025/M1/DS_M1.PDF`
* `wget https://sciences-techniques.univ-nantes.fr/programme-du-m1-visual-computing-vico -O ./data/master2025/M1/VICO_M1.PDF`
* `wget https://sciences-techniques.univ-nantes.fr/programme-m1-cmi-optim -O ./data/master2025/M1/CMI_M1.PDF`
* ` curl -L \
  'https://sciences-techniques.univ-nantes.fr/medias/fichier/m1-smart-computing-mention-informatique_1732713726216-pdf?ID_FICHE=2080272&INLINE=FALSE' \
  -o ./data/master2025/M1/CMD_M1.PDF ` 
 

programme des masters M2 :

* `wget https://sciences-techniques.univ-nantes.fr/programme-du-m2-atal -O  ./data/master2025/M2/ATAL_M2.PDF`
* `wget https://sciences-techniques.univ-nantes.fr/programme-du-m2-alma -O  ./data/master2025/M2/ALMA_M2.PDF`
* `wget https://sciences-techniques.univ-nantes.fr/programme-du-m2-oro -O  ./data/master2025/M2/ORO_M2.PDF`
* `wget https://sciences-techniques.univ-nantes.fr/programme-du-m2-data-sciences-ds-polytech -O  ./data/master2025/M2/DS_M2.PDF`
* `wget https://sciences-techniques.univ-nantes.fr/programme-du-m2-visual-computing-vico-polytech -O  ./data/master2025/M2/VICO_M2.PDF`
* `wget https://sciences-techniques.univ-nantes.fr/programme-m2-cmi-optim -O  ./data/master2025/M2/CMI_M2.PDF`


## Generate KG
pour les masters M1:
* `python extract_ues.py ./data/master2025/M1/ALMA_M1.PDF ./XP/master2025/M1/ALMA_M1.csv`
* `python extract_ues.py ./data/master2025/M1/ATAL_M1.PDF ./XP/master2025/M1/ATAL_M1.csv`
* `python extract_ues.py ./data/master2025/M1/ORO_M1.PDF ./XP/master2025/M1/ORO_M1.csv`
* `python extract_ues.py ./data/master2025/M1/DS_M1.PDF ./XP/master2025/M1/DS_M1.csv`
* `python extract_ues.py ./data/master2025/M1/VICO_M1.PDF ./XP/master2025/M1/VICO_M1.csv`
* `python extract_ues.py ./data/master2025/M1/CMI_M1.PDF ./XP/master2025/M1/CMI_M1.csv`
* `python extract_ues.py ./data/master2025/M1/CMD_M1.PDF ./XP/master2025/M1/CMD_M1.csv`

pour les masters M2:
* `python extract_ues.py ./data/master2025/M2/ATAL_M2.PDF ./XP/master2025/M2/ATAL_M2.csv`
* `python extract_ues.py ./data/master2025/M2/ALMA_M2.PDF ./XP/master2025/M2/ALMA_M2.csv`
* `python extract_ues.py ./data/master2025/M2/ORO_M2.PDF ./XP/master2025/M2/ORO_M2.csv`
* `python extract_ues.py ./data/master2025/M2/DS_M2.PDF ./XP/master2025/M2/DS_M2.csv`
* `python extract_ues.py ./data/master2025/M2/DS_M2.PDF ./XP/master2025/M2/VICO_M2.csv`
* `python extract_ues.py ./data/master2025/M2/DS_M2.PDF ./XP/master2025/M2/CMI_M2.csv`


pour les licences : 
* `python extract_ues.py ./data/licence2025/L3.pdf ./XP/licence2025/L3.csv`

## Check TTL ok
pour les masters M1: 

* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M1/ALMA_M1.ttl', format='turtle'); print(len(g))"`
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M1/ATAL_M1.ttl', format='turtle'); print(len(g))"`
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M1/ORO_M1.ttl', format='turtle'); print(len(g))"`
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M1/DS_M1.ttl', format='turtle'); print(len(g))"`
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M1/VICO_M1.ttl', format='turtle'); print(len(g))"`
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M1/CMI_M1.ttl', format='turtle'); print(len(g))"`
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M1/CMD_M1.ttl', format='turtle'); print(len(g))"`

pour les masters M2: 
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M2/ATAL_M2.ttl', format='turtle'); print(len(g))"`
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M2/ALMA_M2.ttl', format='turtle'); print(len(g))"`
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M2/ORO_M2.ttl', format='turtle'); print(len(g))"`
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M2/DS_M2.ttl', format='turtle'); print(len(g))"`
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M2/VICO_M2.ttl', format='turtle'); print(len(g))"`
* `python -c "from rdflib import Graph; g = Graph(); g.parse('./XP/master2025/M2/CMI_M2.ttl', format='turtle'); print(len(g))"`
