#!/bin/sh

#bedtools getfasta -fi Hilliard.MW.scaffold.fasta -bed CNV_HilliardRef.bed -name > CNV_HilliardRef.fasta
#seqkit sort CNV_HilliardRef.fasta > CNV_HilliardRef.sorted.fasta

bedtools getfasta -fi Hilliard.MW.scaffold.fasta -bed CNV_s_HilliardRef.bed -name > CNV_s_HilliardRef.fasta
seqkit sort CNV_s_HilliardRef.fasta > CNV_s_HilliardRef.sorted.fasta
