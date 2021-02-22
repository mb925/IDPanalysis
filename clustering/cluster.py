#!/usr/bin/env python3

import argparse
import os
import sys
import networkx as nx
import pandas as pd


def main():
    # cluster_file()
    # filter_cluster()
    # convert_regions()
    calculate_union_overlap()


def calculate_union_overlap():
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    with open(scriptdir + '/components-union-overlap.tsv', 'w+') as unionoverlap:
        with open(scriptdir + '/components-converted.tsv', 'r') as components:
            for line in components:
                # print(line)
                reg1 = line.split('\t')[12].split(',')
                reg2 = line.split('\t')[13].split(',')

                len1 = int(line.split('\t')[4])
                len2 = int(line.split('\t')[5])


                align1 = line.split('\t')[10]
                align2 = line.split('\t')[10]
                lenalign1 = int(len(line.split('\t')[10]))
                lenalign2 = int(len(line.split('\t')[11]))
                arrlen = []
                arrlen.append(lenalign1)
                arrlen.append(lenalign2)
                arrlen.append(len1)
                arrlen.append(len2)

                sequencesunp = sum_seq(align1, align2, max(arrlen))
                sequencesreg = sum_reg(reg1 + reg2, max(arrlen))

                union_overlap = merge_seq(max(arrlen), sequencesreg + sequencesunp)

                # for i, elem in enumerate(finalseq):
                #     if elem == '1':
                #         print(i + 1) # array starts from 0


                union = union_overlap[0].count('1')
                overlap = union_overlap[1].count('1')

                # value to be printed into new components file
                overlapunion = str(overlap) + '/' +  str(union)

                if round((overlap / union), 2) > 0.03:
                    print(reg2)
                    print(reg1)
                    print(overlapunion)
                unionoverlap.write(''.join([line.strip(), overlapunion, '\n'] ))





def sum_seq(align1, align2, maxlen):
    sequences = []
    alignseq1 = ''
    alignseq2 = ''
    for amino in align1:
        if amino == '-':
            alignseq1 += '0'
        else:
            alignseq1 += '1'

    for amino in align2:
        if amino == '-':
            alignseq2 += '0'
        else:
            alignseq2 += '1'

    i = len(align1)
    j = len(align1)
    while i < maxlen:
        alignseq1 += '0'
    while j < maxlen:
        alignseq2 += '0'
    sequences.append(alignseq1)
    sequences.append(alignseq2)
    return sequences

def merge_seq(maxlen, sequences):
    j = 0
    union = ''
    overlap = ''
    while j < maxlen:
        elements = []
        for seq in sequences:
            elements.append(seq[j])
        if '1' in elements:
            union += '1'
        else:
            union += '0'
        setelements = set(elements)
        if len(setelements) == 1 and elements[0] == '1':
            overlap += '1'
        else:

            overlap += '0'
        j += 1

    return [union, overlap]


# perform regions union
def sum_reg(regions, maxlen):
    sequences = []
    for reg in regions:
        i = 0
        seq = ''
        end = int(reg.split('_')[1].split('-')[1]) - 1
        start = int(reg.split('_')[1].split('-')[0]) - 1  # array starts from 0
        while i <= maxlen:
            if i < start:
                seq += '0'
            elif i >= start and i <= end:
                seq += '1'
            elif i > end:
                seq += '0'
            i += 1
        sequences.append(seq)

    return sequences


# convert start end
def convert_regions():
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    with open(scriptdir + '/components-converted.tsv', 'w+') as convertedreg:

        with open(scriptdir + '/components-filtered.tsv', 'r') as alignments:
            for alignment in alignments:
                print(alignment)
                sequence1 = alignment.split('\t')[10]
                sequence2 = alignment.split('\t')[11]
                converted1 = []
                converted2 = []

                for region1 in alignment.split('\t')[12].split(','):
                    start1 = region1.split('_')[1].split('-')[0]
                    end1 = region1.split('_')[1].split('-')[1]
                    regionid1 = region1.split('_')[0]
                    convertstartend1 = convert_region(start1, end1, sequence1)
                    converted1.append(regionid1 + '_' + str(convertstartend1[0]) + '-' + str(convertstartend1[1]))

                for region2 in alignment.split('\t')[13].split(','):
                    start2 = region2.split('_')[1].split('-')[0]
                    end2 = region2.split('_')[1].split('-')[1]
                    regionid2 = region2.split('_')[0]
                    convertstartend2 = convert_region(start2, end2, sequence2)

                    converted2.append(regionid2 + '_' + str(convertstartend2[0]) + '-' + str(convertstartend2[1]))

                convertedreg.write(alignment.split('\t')[0] + '\t' + alignment.split('\t')[1] + '\t' +
                                   alignment.split('\t')[2] + '\t' + alignment.split('\t')[3] + '\t'
                                   + alignment.split('\t')[4] + '\t' + alignment.split('\t')[5] + '\t'
                                   + alignment.split('\t')[6] + '\t' + alignment.split('\t')[7] + '\t'
                                   + alignment.split('\t')[8] + '\t' + alignment.split('\t')[9] + '\t'
                                   + alignment.split('\t')[10] + '\t' + alignment.split('\t')[11] + '\t'

                                   + ','.join(converted1) + '\t'
                                   + ','.join(converted2) + '\t'
                                   + alignment.split('\t')[14])


def convert_region(start, end, sequence):
    converted = []
    count = 1
    for i, amino in enumerate(sequence):

        if amino != '-':
            if start == str(count):
                converted.append(i + 1)
            if end == str(count):
                converted.append(i + 1)
            count += 1
    return converted


# remove uniprots that do not have a structural state region associated
def filter_cluster():
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    removedproteins = 0
    regionsarr = []
    uniprots = []
    with open(scriptdir + '/../sequences_regions/search-disprot-filtered.tsv', 'r') as regions:

        for line in regions:
            region = line.split('\t')[5]
            uniprot = line.split('\t')[0]
            uniprots.append(uniprot)
            regionsarr.append(region)
    print(regionsarr)
    with open(scriptdir + '/components-filtered.tsv', 'w+') as outcomponents:

        with open(scriptdir + '/components.tsv', 'r') as alignments:
            for alignment in alignments:

                id1 = alignment.split('\t')[2]
                id2 = alignment.split('\t')[3]
                reg1 = alignment.split('\t')[12]
                reg2 = alignment.split('\t')[13]
                filteredreg1 = []
                filteredreg2 = []

                if id1 in uniprots and id2 in uniprots:

                    for reg in reg1.split(','):
                        if reg.split('_')[0] in regionsarr:
                            filteredreg1.append(reg)
                    for reg in reg2.split(','):
                        if reg.split('_')[0] in regionsarr:
                            filteredreg2.append(reg)

                    outcomponents.write(alignment.split('\t')[0] + '\t' + alignment.split('\t')[1] + '\t' +
                                        alignment.split('\t')[2] + '\t' + alignment.split('\t')[3] + '\t'
                                        + alignment.split('\t')[4] + '\t' + alignment.split('\t')[5] + '\t'
                                        + alignment.split('\t')[6] + '\t' + alignment.split('\t')[7] + '\t'
                                        + alignment.split('\t')[8] + '\t' + alignment.split('\t')[9] + '\t'
                                        + alignment.split('\t')[10] + '\t' + alignment.split('\t')[11] + '\t'

                                        + ','.join(filteredreg1) + '\t'
                                        + ','.join(filteredreg2) + '\t'
                                        + alignment.split('\t')[14])
                else:
                    removedproteins += 1
    print('Removed after filtering: ' + str(removedproteins))


# to be executed after having filtered the results
def cluster_file():
    args = parse_arguments()
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    index = []
    idOne = []
    idTwo = []
    with open(scriptdir + '/../filter/filter-needle-identity.txt', 'r') as input:
        count = 0

        for row in input:
            idOne.append(row.split('\t')[2])
            idTwo.append(row.split('\t')[3])
            index.append(count)
            count += 1

    d = {"id1": pd.Series(idOne, index=index), "id2": pd.Series(idTwo, index=index)}
    df = pd.DataFrame(d)
    G = nx.from_pandas_edgelist(df, 'id1', 'id2')

    components = {}
    count = 0
    for comp in list(nx.connected_components(G)):
        components[count] = comp
        count += 1

    componentsDict = {}
    for key in components:
        for value in components[key]:
            componentsDict[value] = key
    print(componentsDict)

    with open(scriptdir + '/../filter/filter-needle-identity.txt', 'r') as table:
        with open(scriptdir + '/components.tsv', 'w+') as tablecomp:
            for line in table:
                id = line.split('\t')[2]
                compVal = componentsDict[id]
                print(compVal)
                tablecomp.write(line.strip() + '\t' + str(compVal) + '\n')


def parse_arguments(initargs=None):
    if initargs is None:
        initargs = []
    parser = argparse.ArgumentParser(description="Parse input alignment file.")
    parser.add_argument('-i', help="Input alignment file")
    if not initargs or len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        args = parser.parse_args(initargs)
    return args


if __name__ == '__main__':
    sys.exit(main())
