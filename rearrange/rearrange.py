#!/usr/bin/env python3

import argparse
import os
import sys
import networkx as nx
import pandas as pd

from clustering.cluster import transform_region


def main():
    create_tables()




def create_tables():

    scriptdir = os.path.dirname(os.path.realpath(__file__))
    dataframes = []

    with open(scriptdir + '/../clustering/components-filtered.tsv', 'r') as alignments:
        for line in alignments:
            d = {'s1': [], 's2': [], 'd1': [], 'd2': []}
            id1 = line.split('\t')[2]
            id2 = line.split('\t')[3]
            align1 = ''
            align2 = ''
            alignoutput = line.split('#=')[1].split('/n')
            for row in alignoutput:
                if row.startswith(id1):
                    row = row.split(id1)[1].strip()
                    row = ''.join([i for i in row if not i.isdigit()]).strip()
                    align1 += row
            for row in alignoutput:
                if row.startswith(id2):
                    row = row.split(id2)[1].strip()
                    row = ''.join([i for i in row if not i.isdigit()]).strip()
                    align2 += row

            i = 0
            j = 1
            # print(align1)
            # print(align2)
            if len(align1) == len(align2):
                while i < len(align1):
                    # print(align1[i] + '_' + str(j))
                    if align1[i] != '-':
                        d['s1'].append(align1[i] + '_' + str(j))
                    elif align1[i] == '-':
                        d['s1'].append('-')
                    if align2[i] != '-':
                        d['s2'].append(align2[i] + '_' + str(j))
                    elif align2[i] == '-':
                        d['s2'].append('-')
                    j += 1
                    i += 1
            else:
                print("Alignment to be checked")


            reg1 = expand_regions(line.split('\t')[12].split(','))
            reg2 = expand_regions(line.split('\t')[13].split(','))

            for el in d['s1']:
                if el == '-':
                    d['d1'].append('na')
                elif int(el.split('_')[1]) in reg1:
                    d['d1'].append(str(1))
                else:
                    d['d1'].append(0)

            for el in d['s2']:
                if el == '-':
                    d['d2'].append('na')
                elif int(el.split('_')[1]) in reg2:
                    d['d2'].append(str(1))
                else:
                    d['d2'].append(0)

            title = id1 + '_' + id2
            with open(scriptdir + '/rearranged_files' + title + '.tsv', 'w+') as out:
                out.write('\t'.join('s1' + 's2' + 'd1' + 'd2') + '\n')

                counter = 0
                while counter < len(d['s1']):
                    out.write('\t'.join(d['s1'] + d['s2'] + str(d['d1']) + str(d['d2']) + '\n')


def expand_regions(regions):
    transformed_regions = []
    for reg in regions:
        start = int(reg.split('_')[1].split('-')[0])
        end = int(reg.split('_')[1].split('-')[1])
        while start <= end:
            transformed_regions.append(start)
            start += 1
    return transformed_regions

if __name__ == '__main__':
    sys.exit(main())
