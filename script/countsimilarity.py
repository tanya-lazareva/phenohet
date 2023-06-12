import argparse
import math
import subprocess
import csv
from pyhpo import HPOSet, Ontology


# search mims
def search_mims(gene_id, path_table):
    mims = {}
    with open(path_table) as table_id:
        for line in table_id:
            f_id = line.split('\t')
            f_id = [line.rstrip() for line in f_id]
            if gene_id == f_id[0]:
                mims[f_id[1]] = []
    return mims


# find all HPO terms for each MIM
def collect_hpo(mims_dict, path_hpo):
    with open(path_hpo) as table_hpo:
        for line in table_hpo:
            f_id = line.split('\t')
            f_id = [line.rstrip() for line in f_id]
            for mim in mims_dict:
                if mim == f_id[0]:
                    mims_dict[mim].append(f_id[1])
    return mims_dict


# calculate Jaccard index
def jaccard(mims_dict):
    first_val = list(mims_dict.values())[0]
    second_val = list(mims_dict.values())[1]

    intersection = len(list(set(first_val).intersection(second_val)))
    union = (len(first_val) + len(second_val)) - intersection

    return float(intersection) / union


# calculate distance between HP terms
def HPO_dist(mims_dict):
    _ = Ontology() # initilize the Ontology
    mim1 = HPOSet.from_queries(list(mims_dict.values())[0])
    mim2 = HPOSet.from_queries(list(mims_dict.values())[1])
    
    # and compare their similarity
    sim_score = mim1.similarity(mim2, method="dist")
    
    return sim_score


# calculate Resnik metric
def HPO_Resnik(mims_dict):
    _ = Ontology() # initilize the Ontology
    mim1 = HPOSet.from_queries(list(mims_dict.values())[0])
    mim2 = HPOSet.from_queries(list(mims_dict.values())[1])
    
    # and compare their similarity
    sim_score = mim1.similarity(mim2, method="resnik")
    
    return sim_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gene", type=str, help="Gene id")
    parser.add_argument("--genedis", type=str,
                        help="Path to gene-disease table")
    parser.add_argument("--hpo", type=str, help="Path to MIM-HPO table")
    args = parser.parse_args()

    gene = args.gene
    path_genedis = args.genedis
    mim2_dict = search_mims(gene, path_genedis)
    path_dishpo = args.hpo
    mim_hpo = collect_hpo(mim2_dict, path_dishpo)
    jaccard_index = jaccard(mim_hpo)
    HPO_simscore = HPO_dist(mim_hpo)
    HPO_resnik = HPO_Resnik(mim_hpo)


    print('GENE', 'MIM1', 'MIM2', 'Jaccard', 'HP_distance', 'Resnik', 'MIM1_terms', 'MIM2_terms', sep=',')
    print(gene, list(mim_hpo)[0], list(mim_hpo)[1], jaccard_index, HPO_simscore, HPO_resnik, len(list(mim_hpo.values())[0]),
          len(list(mim_hpo.values())[1]), sep=',')
