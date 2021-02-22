#!/usr/bin/env python3

import argparse
import os
import sys

def main():
    # parse_alignment_file()
    parse_seqres_file()     # to be executed after having clustered

# filter >= 30 identity
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

# to be executed after having clustered
# filter structural state
# filter uniprots from clusters
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
