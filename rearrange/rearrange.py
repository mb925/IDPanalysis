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
    # with open(scriptdir + '/outtest.tsv', 'w+') as out:
    with open(scriptdir + '/all-dataframe.tsv', 'w+') as out:
        out.write('id1' + '\t' + 'id2' + '\t' + 's1' + '\t' + 's2' + '\t' + 'p1' + '\t' + 'p2' + '\t' + 'd1' + '\t' + 'd2' + '\n')
        count = 0
        # with open(scriptdir + '/testinp.tsv', 'r') as alignments:

        with open(scriptdir + '/../clustering/components-filtered.tsv', 'r') as alignments:
            next(alignments)

            for line in alignments:
                d = {'id1': [], 'id2': [], 's1': [], 'p1': [], 'p2': [], 's2': [], 'd1': [], 'd2': []}

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
                        d['id1'].append(id1)
                        d['id2'].append(id2)
                        if align1[i] != '-':
                            d['s1'].append(align1[i])
                            d['p1'].append(str(j))
                        elif align1[i] == '-':
                            d['s1'].append('-')
                            d['p1'].append('') # na

                        if align2[i] != '-':
                            d['s2'].append(align2[i])
                            d['p2'].append(str(j))
                        elif align2[i] == '-':
                            d['s2'].append('-')
                            d['p2'].append('')

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
                        d['d1'].append('')
                    elif int(d['p1'][index]) in reg1:
                        d['d1'].append(1)
                    else:
                        d['d1'].append(0)

                for index, el in enumerate(d['s2']):
                    if el == '-':
                        d['d2'].append('')
                    elif int(d['p2'][index]) in reg2:
                        d['d2'].append(1)
                    else:
                        d['d2'].append(0)


                count += 1
                print(count)


                x = 0
                while x < len(d['id2']):

                    out.write(d['id1'][x] + '\t' + d['id2'][x] + '\t' + d['s1'][x] + '\t' + d['s2'][
                        x] + '\t' + d['p1'][x] + '\t' + d['p2'][x] + '\t' + str(d['d1'][x]) + '\t' + str(
                        d['d2'][x]) + '\n')
                    x += 1


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
