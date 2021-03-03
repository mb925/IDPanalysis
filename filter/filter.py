#!/usr/bin/env python3

import argparse
import os
import sys

def main():
    # parse_alignment_file()
    # parse_seqres_file()     # to be executed after having clustered
    filter_components()

def filter_components():
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    with open(scriptdir + '/filtered-components-region.tsv', 'w+') as output:
        with open(scriptdir + '/../clustering/components-union-overlap.tsv', 'r') as input:
            for row in input:
                identity = round(int(row.split('\t')[6].split('/')[0]) / int(
                    row.split('\t')[6].split('/')[1]), 2)
                identity = identity * 100

                numoverlap = int(row.split('\t')[15].split('/')[0])
                overlap = 0
                if numoverlap > 0:

                    overlap = round(int(row.split('\t')[15].split('/')[0]) / int(
                        row.split('\t')[15].split('/')[1]), 2)

                if identity >= 0:
                    if overlap <= 10:
                        output.write(row)

# filter >= 30% identity
def parse_alignment_file():
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    with open(scriptdir + '/filter-needle-identity.txt', 'w+') as output:
      with open(scriptdir + '/../results_needle_al/all-global-needle.txt', 'r') as input:
            for row in input:
                if row.startswith("#") == False:
                    identity = int(row.split('\t')[6].split('/')[0])
                    # identity = round(int(row.split('\t')[6].split('/')[0]) / int(
                    #     row.split('\t')[6].split('/')[1]), 2)
                    # identity = identity * 100

                    # if identity >= 30:
                    if identity >= 0.03:
                        output.write(row)

# to be executed after having clustered
# filter structural state
# filter uniprots, keeping the one that are in the clusters
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
