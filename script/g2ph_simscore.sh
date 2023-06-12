#! usr/bin/bash
split -l 100 ./count_HPO/G2Ph_genes.txt ./count_HPO/GENE; for i in $(cat ./count_HPO/GENE*) ; do python3 ./script/countsimilarity.py --gene $i --genedis ./count_HPO/G2Ph_MIM.csv --hpo ./count_HPO/terms_to_mim.txt; done > ./count_HPO/G2Ph_similarity.csv
sed 3~2d ./count_HPO/G2Ph_similarity.csv > ./count_HPO/G2Ph_simscore.csv
