import argparse
import math
import subprocess
from pybedtools import BedTool
import csv
from itertools import zip_longest



def search_canonical_transcript(gene_id, path_table):
    with open(path_table) as table_id:
        for line in table_id:
            if gene_id in line:
                f_id = line.split(',')
                f_id = [line.rstrip() for line in f_id]
                tr_id = f_id[1]
    return tr_id


def create_list_cds(can_tr_id, path_gencode):
    cds_list = open('./VarCount/list_of_CDS.gtf', 'w+')
    with open(path_gencode) as gencode:
        for line in gencode:
            elements = line.split()
            if len(elements) > 3 and elements[2] == 'CDS':
                if can_tr_id in line:
                    cds_list.write(line)
    return cds_list


def filter_bed():
    filter_res = open('./VarCount/filt_choice.bed', 'w+')
    with open('./VarCount/filt_choice1.bed') as filt_choice:
        filt_choice = BedTool(filt_choice)
        for feature in filt_choice:
            coords = BedTool(f'{feature.chrom} {feature.start} {feature.stop} .', from_string=True)
            filter_res.write(str(coords))
    return filter_res


def count_tr_length(filtered_bed):
    cds_bed = BedTool(filtered_bed)
    tr_len = 0
    for feature in cds_bed:
        tr_len += feature.stop - feature.start
    #print(f'Length of transcript = {tr_len}')
    return tr_len, cds_bed


# split CDSs on n bins
def split_intervals(tr_len, file_cds):
    num_bins = args.bin   # number of intervals
    n = math.ceil(tr_len / num_bins)   # sum of nucl. per interval
    #print(n)
    a = 0
    bins = open('./VarCount/bin.bed', 'w+')
    for feature in file_cds:
        if a + feature.stop - feature.start == n:
            a += feature.stop - feature.start
            cds_split = BedTool(f'{feature.chrom} {feature.start} {feature.stop} +',
                                 from_string=True)
            bins.write(str(cds_split))
            a = 0

        elif a + feature.stop - feature.start < n:
            a += feature.stop - feature.start
            bins.write(str(feature))

        elif a + feature.stop - feature.start > n and a < n:
            a1 = n - a  
            delta = feature.stop - feature.start - a1  
            a += a1
            cds_split0 = BedTool(f'{feature.chrom} {feature.start} {feature.start + a1} +', from_string=True)
            bins.write(str(cds_split0))
            a = 0

            if delta == n:
                a += delta
                cds_split1 = BedTool(f'{feature.chrom} {feature.start + a1} {feature.stop} +',
                                     from_string=True)
                bins.write(str(cds_split1))
                a = 0

            elif delta < n:
                a += delta
                cds_split1 = BedTool(f'{feature.chrom} {feature.start + a1} {feature.stop} .',
                                     from_string=True)
                bins.write(str(cds_split1))

            elif delta > n:

                while delta > n:
                    a += n
                    delta = delta - n
                    a = 0
                    cds_split2 = BedTool(f'{feature.chrom} {feature.start + a1} {feature.start + a1 + n} +',
                                         from_string=True)
                    bins.write(str(cds_split2))
                    a1 += n

                if delta < n:
                    a += delta
                    cds_split3 = BedTool(
                        f'{feature.chrom} {feature.start + a1} {feature.stop} .', from_string=True)
                    bins.write(str(cds_split3))

                if delta == n:
                    a += delta
                    a = 0
                    cds_split4 = BedTool(f'{feature.chrom} {feature.start + a1} {feature.stop} +', from_string=True)
                    bins.write(str(cds_split4))
    return bins


# mark last bine
def last_line():
    with open('./VarCount/bin.bed', 'r') as bins:
        bins_read = bins.readlines()   
        last_line = bins_read[-1]  
        bins_line = last_line.split()
        last = len(bins_read)-1   
        bins_read[last] = str(BedTool(f'{bins_line[0]}  {bins_line[1]}  {bins_line[2]}  +', from_string=True))
       

    bins = open('./VarCount/bin.bed', 'w')
    for line in bins_read:
        bins.write(str(line))   

    return bins


def count_intersects(int_result):
    int_count = 0  
    list_count_intersect = []  
    for feature in int_result:
        feature = feature.split()
        if "+" not in feature[3]:
            int_count += int(feature[4])
        if "+" in feature[3]:
            int_count += int(feature[4])
            list_count_intersect.append(int_count)
            int_count = 0
            continue
    return list_count_intersect


def create_csv_result(result_d1, result_d2):
    total_list = [result_d1, result_d2]
    export_data = zip_longest(*total_list, fillvalue='')
    with open('./VarCount/final_table.csv', 'w', encoding="ISO-8859-1", newline='') as filnal_table:
        wr = csv.writer(filnal_table)
        wr.writerow(("D1", "D2"))
        wr.writerows(export_data)
    return export_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gene", type=str, help="Gene id")   
    parser.add_argument("--can", type=str, help="Path to canonical transcripts table")
    parser.add_argument("--ann", type=str, help="Path to gencode annotation")  
    parser.add_argument("--gff2bed", type=str, help="Path to gff2bed")  
    parser.add_argument("--bin", type=int, help="Number of intervals")  
    parser.add_argument("--dis1", type=str, help="Path to dis1 variants") 
    parser.add_argument("--dis2", type=str, help="Path to dis2 variants")
    args = parser.parse_args()

    gene = args.gene  
    path_can_table = args.can  

    transcript_id = search_canonical_transcript(gene, path_can_table)

    path_gencode_ann = args.ann
    list_cds = create_list_cds(transcript_id, path_gencode_ann)
    list_cds.flush()

    gff2bed=args.gff2bed
    p_1 = subprocess.Popen(f"{gff2bed} < ./VarCount/list_of_CDS.gtf > ./VarCount/filt_choice1.bed",
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p_1.communicate()

    filt = filter_bed()
    filt.flush()

    transcript_len, cds = count_tr_length('./VarCount/filt_choice.bed')

    bins = split_intervals(transcript_len, cds)
    bins.flush()

    bins = last_line()
    bins.flush()
    
    bins = BedTool('./VarCount/bin.bed')
    dis1 = args.dis1

    dis1_result = bins.intersect(dis1, c=True, output='./VarCount/dis1_intersect.bed')

    dis2 = args.dis2  
    dis2_result = bins.intersect(dis2, c=True, output='./VarCount/dis2_intersect.bed')

    dis1_intersect = open('./VarCount/dis1_intersect.bed')
    list_dis1 = count_intersects(dis1_intersect)
    dis2_intersect = open('./VarCount/dis2_intersect.bed')
    list_dis2 = count_intersects(dis2_intersect)

    export_data_csv = create_csv_result(list_dis1, list_dis2)

    print('Ensembl', 'D_1', *[' ' for _ in range(len(list_dis1)-1)], 'D_2',
          *[' ' for _ in range(len(list_dis2)-1)], sep=',') 

    print(gene, *list_dis1, *list_dis2, sep=',')

