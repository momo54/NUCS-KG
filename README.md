# Generate from PDF, Knowledge Graph of Graduate programs...

## get the data

* execute `python download_pdf.py`
* pdf2excel with ilovepdf

## Generate KG

* execute `snakemake -c1`

Pb VICO:
```
python extract_ue_xlsx_vico.py ./data/master2025/M2/VICO_M2.xlsx ./XP/master2025/M2/VICO_M2.ttl
``` 

## Check TTL ok

* execute `python merge_ttl.py XP -o ./XP/all.ttl`
  
