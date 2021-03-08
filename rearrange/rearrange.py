#!/usr/bin/env python3

import argparse
import os
import sys
import networkx as nx
import pandas as pd

def main():
    create_tables()




def create_tables():

    scriptdir = os.path.dirname(os.path.realpath(__file__))
    dataframes = []

    with open(scriptdir + '/../clustering/components-filtered.tsv', 'r') as alignments:
        for line in alignments:
            overlap = 0
            union = 0
            d = {'s1': [], 'p1': [], 'p2': [], 's2': [], 'd1': [], 'd2': []}
            id1 = line.split('\t')[2]
            id2 = line.split('\t')[3]
            align1 = ''
            align2 = ''
            alignoutput = line.split('#=')[1].split('/n')
            for row in alignoutput:
                if row.startswith(id1 + ' '):
                    row = row.split(id1 + ' ')[1].strip()
                    row = ''.join([i for i in row if not i.isdigit()]).strip()
                    align1 += row
            for row in alignoutput:
                if row.startswith(id2 + ' '):
                    row = row.split(id2 + ' ')[1].strip()
                    row = ''.join([i for i in row if not i.isdigit()]).strip()
                    align2 += row

            i = 0
            j = 1

            if len(align1) == len(align2):
                while i < len(align1):
                    # print(align1[i] + '_' + str(j))
                    if align1[i] != '-':
                        d['s1'].append(align1[i])
                        d['p1'].append(str(j))
                    elif align1[i] == '-':
                        d['s1'].append('-')
                        d['p1'].append('na')

                    if align2[i] != '-':
                        d['s2'].append(align2[i])
                        d['p2'].append(str(j))
                    elif align2[i] == '-':
                        d['s2'].append('-')
                        d['p2'].append('na')

                    j += 1
                    i += 1
            else:
                print("Alignment to be checked")
                print(id1)
                print(id2)
                print(align1)
                print(align2)

            reg1 = expand_regions(line.split('\t')[12].split(','))
            reg2 = expand_regions(line.split('\t')[13].split(','))

            # print(reg1)

            for index, el in enumerate(d['s1']):
                # print(d['p1'][index])
                if el == '-': # if you have a gap you can't have disprot region
                    d['d1'].append('na')
                elif int(d['p1'][index]) in reg1:
                    d['d1'].append(str(1))
                else:
                    d['d1'].append(0)

            for index, el in enumerate(d['s2']):
                if el == '-':
                    d['d2'].append('na')
                elif int(d['p2'][index]) in reg2:
                    d['d2'].append(str(1))
                else:
                    d['d2'].append(0)

            title = id1 + '_' + id2
            overlap, union = calc_overlap_mismatch(d)
            overlap_match, union_match = calc_overlap_match(d)
            print(overlap, union)
            with open(scriptdir + '/rearranged_files/' + title + '.tsv', 'w+') as out:
                out.write('>identity: ' + line.split('\t')[6] + '\n')
                out.write('>overlap/union: ' + overlap + '/' + union + '\n')
                out.write('>overlap/union_match: ' + overlap_match + '/' + union_match + '\n')
                out.write('s1' + '\t' + 's2' + '\t' + 'p1' + '\t' + 'p2' + '\t' + 'd1' + '\t' + 'd2' + '\n')


                counter = 0
                while counter < len(d['s1']):
                    out.write(d['s1'][counter] + '\t' + d['s2'][counter]  + '\t' + d['p1'][counter] + '\t' + d['p2'][counter] + '\t' + str(d['d1'][counter]) + '\t' + str(d['d2'][counter]) + '\n')
                    counter += 1

def calc_overlap_mismatch(df):
    # for filename in os.listdir(scriptdir + '/rearranged_files'):
    #     print(pd.read_csv(scriptdir + '/rearranged_files/' + filename, sep='\t', header=0))
    #     df = pd.read_csv(scriptdir + '/rearranged_files/' + filename, sep='\t', header=0)
    overlap = 0
    union = 0
    for index, d1 in enumerate(df['d1']):
        if d1 and df['d2'][index] == '1':
            overlap += 1
        if d1 or df['d2'][index] == '1':
            union += 1
    return [str(overlap), str(union)]

def calc_overlap_match(df):
    overlap = 0
    union = 0
    for index, d1 in enumerate(df['d1']):
        if d1 and df['d2'][index] == '1' and d1 == df['d2'][index]:
            overlap += 1
        if d1 or df['d2'][index] == '1' and d1 == df['d2'][index]:
            union += 1
    return [str(overlap), str(union)]

def expand_regions(regions):
    transformed_regions = []
    for reg in regions:
        start = int(reg.split('_')[1].split('-')[0])
        end = int(reg.split('_')[1].split('-')[1])
        while start <= end:
            transformed_regions.append(start)
            start += 1
    return set(transformed_regions)

if __name__ == '__main__':
    sys.exit(main())
