#! usr/bin/bash
wget -O ./data/genncode.v43.annotation.gtf.gz https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_43/gencode.v43.basic.annotation.gtf.gz
gzip -d ./data/genncode.v43.annotation.gtf.gz 
split -l 100 ./VarCount/G2Ph_ensembl_list.csv ./VarCount/GENE; for i in $(cat ./VarCount/GENE*) ; do python3 ./script/countvariants.py --gene $i --can ./data/canonical_transcripts.txt --ann ./data/genncode.v43.annotation.gtf --gff2bed /usr/bin/gff2bed --bin 1 --dis1 ./VarCount/G2Ph_dis1_miss.vcf --dis2 ./VarCount/G2Ph_dis2_miss.vcf; done > ./VarCount/G2Ph_miss_variants.csv
sed 3~2d ./VarCount/G2Ph_miss_variants.csv > ./VarCount/G2Ph_miss.csv
rm ./VarCount/G2Ph_miss_variants.csv

split -l 100 ./VarCount/G2Ph_ensembl_list.csv ./VarCount/GENE; for i in $(cat ./VarCount/GENE*) ; do python3 ./script/countvariants.py --gene $i --can ./data/canonical_transcripts.txt --ann ./data/genncode.v43.annotation.gtf --gff2bed /usr/bin/gff2bed --bin 1 --dis1 ./VarCount/G2Ph_dis1_plof.vcf --dis2 ./VarCount/G2Ph_dis2_plof.vcf; done > ./VarCount/G2Ph_plof_variants.csv
sed 3~2d ./VarCount/G2Ph_plof_variants.csv > ./VarCount/G2Ph_plof.csv
rm ./VarCount/G2Ph_plof_variants.csv

