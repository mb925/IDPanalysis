#!/usr/bin/env python3

import argparse
import os
import sys

def main():
    # parse_alignment_file()
    # parse_seqres_file()
    convert_regions()



def convert_regions():
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    dictregions = {}


    with open(scriptdir + '/../sequences_regions/search-disprot-filtered.tsv', 'r') as regions:

            for line in regions:

                regionid = line.split('\t')[5]
                regionstart = line.split('\t')[6]
                regionend = line.split('\t')[7]
                uniprot = line.split('\t')[0]
                if uniprot in dictregions:
                    dictregions[uniprot].append(regionid + '_' + regionstart + '-' + regionend)
                else:
                    dictregions[uniprot] = []
                    dictregions[uniprot].append(regionid + '_' + regionstart + '-' + regionend)

    # with open(scriptdir + '/../clustering/components-converted.tsv', 'w+') as convertedreg:

    with open(scriptdir + '/../clustering/components-filtered.tsv', 'r') as alignments:
        for alignment in alignments:
            id1 = alignment.split('\t')[2]
            id2 = alignment.split('\t')[3]
            sequence1 = alignment.split('\t')[10]
            sequence2 = alignment.split('\t')[11]
            print(alignment)
            print(alignment.split('\t')[11])
            converted1 = []
            converted2 = []

            for region1 in dictregions[id1]:

                start1 = region1.split('_')[1].split('-')[0]
                end1 = region1.split('_')[1].split('-')[1]
                regionid1 = region1.split('_')[0]
                convertstartend1 = convert_region(start1, end1, sequence1)
                converted1.append(regionid1 + '_' + str(convertstartend1[0]) + '-' + str(convertstartend1[1]))

            for region2 in dictregions[id2]:
                start2 = region2.split('_')[1].split('-')[0]
                end2 = region2.split('_')[1].split('-')[1]
                regionid2 = region2.split('_')[0]

                convertstartend2 = convert_region(start2, end2, sequence2)
                print(start2)
                print(end2)
                print(sequence2) # MISSING
                print(convertstartend2)
                print(regionid2)
                print(id2)
                converted2.append(regionid2 + '_' + str(convertstartend2[0]) + '-' + str(convertstartend2[1]))


                # convertedreg.write(alignment.split('\t')[0] + '\t' + alignment.split('\t')[1] + '\t' +
                #                    id1 + '\t' + id2 + '\t'
                #                    + alignment.split('\t')[4] + '\t' + alignment.split('\t')[5] + '\t'
                #                    + alignment.split('\t')[6] + '\t' + alignment.split('\t')[7] + '\t'
                #                    + alignment.split('\t')[8] + '\t' + alignment.split('\t')[9] + '\t'
                #                    + alignment.split('\t')[10] + '\t' + alignment.split('\t')[11] + '\t'
                #
                #                    + ','.join(converted1) + '\t'
                #                    + ','.join(converted2) + '\t'
                #                    + alignment.split('\t')[14])



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


def parse_seqres_file():
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    uniprots = []
    with open(scriptdir + '/../clustering/components.tsv', 'r') as tablecomp:
        for line in tablecomp:
            id1 = line.split('\t')[2]
            id2 = line.split('\t')[3]
            if id1 in uniprots:
                pass
            else:
                uniprots.append(id1)
            if id2 in uniprots:
                pass
            else:
                uniprots.append(id2)

    with open(scriptdir + '/../sequences_regions/search-disprot-filtered.tsv', 'w+') as output:

      with open(scriptdir + '/../sequences_regions/search_in_disprot.tsv', 'r') as input:
         for row in input:
             if row.split('\t')[8] == 'Structural state':
                 if row.split('\t')[0] in uniprots:
                    output.write(row)


def parse_alignment_file():
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    with open(scriptdir + '/filter-needle-identity.txt', 'w+') as output:
      with open(scriptdir + '/../results_needle/all-global-needle.txt', 'r') as input:
            for row in input:
                if row.startswith("#") == False:
                    identityNum = int(row.split('\t')[6].split('/')[0])

                #     id1 = row.split('\t')[2]
                #     id2 = row.split('\t')[3]
                    if identityNum >= 30:
                #         output.write(str(percentIdentity) + '\n')
                        output.write(row)


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
