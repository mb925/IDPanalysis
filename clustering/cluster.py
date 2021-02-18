#!/usr/bin/env python3

import argparse
import os
import sys
import networkx as nx
import pandas as pd


def main():
    # cluster_file()
    filter_cluster()
#     calculate_union_overlap()
#
# def calculate_union_overlap():




# remove uniprots that do not have a structural state region associated
def filter_cluster():
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    dictregions = {}
    with open(scriptdir + '/../sequences_regions/search-disprot-filtered.tsv', 'r') as regions:

            for line in regions:

                regionstart = line.split('\t')[6]
                regionend = line.split('\t')[7]
                uniprot = line.split('\t')[0]
                dictregions[uniprot] = [regionstart, regionend]

    with open(scriptdir + '/components-filtered.tsv', 'w+') as outcomponents:

        with open(scriptdir + '/components.tsv', 'r') as alignments:
            for alignment in alignments:

                id1 = alignment.split('\t')[2]
                id2 = alignment.split('\t')[3]

                if id1 in dictregions and id2 in dictregions:
                    outcomponents.write(alignment)


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
            count +=1

    d = {"id1": pd.Series(idOne, index=index),"id2": pd.Series(idTwo, index=index)}
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
