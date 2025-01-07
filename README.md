# cnv-primer-design

## Methods:

1. Use R script to extract fasta sequences from BUSCO output.
2. Snakemake
	1. Extract gene multifasta from reference fasta using bedtools and R script output.
	2. Align common BUSCO output by clustal.
	3. Extract consensus sequences from clustal alignment.
	4. Design primers by Primer3.
	5. Test primers by UCSC/isPCR.
