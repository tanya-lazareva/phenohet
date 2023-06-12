#! usr/bin/bash
repeats=530
for i in $(seq $repeats); do python3 ./script/countsimilarity_random.py --genedis ./count_HPO/G1Ph_MIM.csv --hpo ./count_HPO/terms_to_mim.txt; done > ./count_HPO/G1Ph_similarity_r.csv
sed 3~2d ./count_HPO/G1Ph_similarity_r.csv > ./count_HPO/G1Ph_simscore.csv
rm ./count_HPO/G1Ph_similarity_r.csv



