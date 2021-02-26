#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

import argparse
import os
import sys


def main():
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    visualize_overlap_identity(scriptdir)
    # visualize_alignments(scriptdir)


def visualize_alignments(scriptdir):
    with open(scriptdir + '/../filter/components-filtered.tsv', 'r') as input:
        for line in input:
            print(line.split('\t')[10].split('/n'))

def visualize_overlap_identity(scriptdir):

        flag = 0
        with open(scriptdir + '/../clustering/components-union-overlap.tsv', 'r') as input:
            x, y = [], []
            count = 0

            for line in input:
                id1 = line.split('\t')[0]
                id2 = line.split('\t')[2]
                count +=1

                identity = round(int(line.split('\t')[6].split('/')[0]) / int(
                        line.split('\t')[6].split('/')[1]), 2)
                identity = identity * 100
                # identity = int(line.split('\t')[6].split('/')[0])
                if identity > flag:
                    flag = identity
                    # print(flag)

                numoverlap = int(line.split('\t')[14].split('/')[0])
                if numoverlap > 0:

                    overlap = round(int(line.split('\t')[14].split('/')[0]) / int(
                        line.split('\t')[14].split('/')[1]), 2)

                else:
                    overlap = 0
                # print(str(identity) + ' ' + str(overlap))

                # print(count)
                x.append(identity)
                y.append(overlap)

            # print(y)


            plt.scatter(x, y, alpha=0.5)
            plt.xlabel("identity")
            plt.ylabel("overlap")
            plt.savefig('identity-overlap.png')


if __name__ == '__main__':
    sys.exit(main())