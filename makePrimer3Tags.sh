#!/bin/bash

seqkit fx2tab CNV_s_HilliardRef.sorted.fasta > CNV_s_HilliardRef.sorted.fasta.txt

> busco_primer3_tags.txt
while read line; do
  name="SEQUENCE_ID="
  name+=`echo "$line" | cut -f 1`
  sequence="SEQUENCE_TEMPLATE="
  sequence+=`echo "$line" | cut -f 2`
  echo $name >> busco_primer3_tags.txt
  echo $sequence >> busco_primer3_tags.txt
  echo "PRIMER_TASK=generic" >> busco_primer3_tags.txt
  echo "PRIMER_PICK_LEFT_PRIMER=1" >> busco_primer3_tags.txt
  echo "PRIMER_PICK_INTERNAL_OLIGO=1" >> busco_primer3_tags.txt
  echo "PRIMER_PICK_RIGHT_PRIMER=1" >> busco_primer3_tags.txt
  echo "PRIMER_EXPLAIN_FLAG=1" >> busco_primer3_tags.txt
  echo "=" >> busco_primer3_tags.txt
done < CNV_s_HilliardRef.sorted.fasta.txt
