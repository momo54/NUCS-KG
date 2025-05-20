# Generate from PDF, Knowledge Graph of Graduate programs...

## get the data

* execute `python download_pdf.py`

## Generate KG

* execute `snakemake -c1`

## Check TTL ok

* execute `python merge_ttl.py XP -o ./XP/all.ttl`
  
  