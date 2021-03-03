#!/usr/bin/env python3
import numpy as np
import statistics
import matplotlib.pyplot as plt

import argparse
import os
import sys


import numpy as np
import matplotlib.pyplot as plt


def main():
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    # visualize_overlap_identity(scriptdir)
    visualize_alignments(scriptdir)
    # visualize_identity(scriptdir)
    # visualize_overlap(scriptdir)

def visualize_overlap(scriptdir):
    plt.style.use('seaborn-white')
    with open(scriptdir + '/../clustering/components-union-overlap.tsv', 'r') as input:
        data = []

        for line in input:
            numoverlap = int(line.split('\t')[15].split('/')[0])
            overlap = 0
            if numoverlap > 0:

                overlap = round(int(line.split('\t')[15].split('/')[0]) / int(
                    line.split('\t')[15].split('/')[1]), 2)

            if overlap >= 0.3:
                data.append(overlap)


def visualize_identity(scriptdir):

    with open(scriptdir + '/../clustering/components-union-overlap.tsv', 'r') as input:
        data = []
        dict = {}
        ids = []


        for line in input:
            id1 = line.split('\t')[2]
            id2 = line.split('\t')[3]
            # numoverlap = int(line.split('\t')[14].split('/')[0])
            # overlap = 0
            # if numoverlap > 0:
            #     overlap = round(int(line.split('\t')[14].split('/')[0]) / int(
            #         line.split('\t')[14].split('/')[1]), 2)
            identity = round(int(line.split('\t')[6].split('/')[0]) / int(
                line.split('\t')[6].split('/')[1]), 2)
            identity = identity * 100
            # if overlap >= 0.3:

            if id1 in dict:
                dict[id1].append(identity)
                #     dict[id1].append(overlap)
            else:
                dict[id1] = []
                dict[id1].append(identity)

                # dict[id1].append(overlap)

            if id2 in dict:

                dict[id2].append(identity)
                #     dict[id2].append(overlap)
            else:
                dict[id2] = []
                dict[id1].append(identity)
                # dict[id2].append(overlap)

        for key in dict:
            maxval = max(dict[key])
            ids.append(key)
            data.append(maxval)
    i = 0
    lenids = len(ids)
    while i < lenids:

        stop = i + 50
        subsetids = ids[i:stop]
        subsetdata = data[i:stop]
        y_pos = np.arange(len(subsetids))

        # Create bars
        plt.bar(y_pos, subsetdata)

        # Create names on the x-axis
        plt.xticks(y_pos, subsetids, rotation=90)

        plt.savefig('hist_identity/subset' + str(i) + '.png')
        i += 50
        plt.clf()
        print(i)


def visualize_alignments(scriptdir):
    # with open(scriptdir + '/alignments.tsv', 'w+') as out:
    with open(scriptdir + '/../filter/filtered-components-region.tsv', 'r') as input:
        for line in input:
            # print(line)
            print(line.split('\t')[15].split('/n'))
            print(line.split('\t')[11].split('/n'))
            reg1 = line.split('\t')[11].split(',')
            reg1conv = []
            for reg in reg1:
                start1 = reg.split('_')[1].split('-')[0]
                end1 = reg.split('_')[1].split('-')[1]
                regconv = list(range(int(start1), int(end1)))
                reg1conv.append(regconv)
            j = 0
            seq = ''
            while j < regconv[-1]:
                if j in regconv:
                    seq += '1'
                else:
                    seq += '-'
                j += 1

            print(line.split('\t')[12].split('/n'))

            reg2 = line.split('\t')[12].split(',')
            reg2conv = []
            for reg in reg2:
                start2 = reg.split('_')[1].split('-')[0]
                end2 = reg.split('_')[1].split('-')[1]
                regconv2 = list(range(int(start2), int(end2)))
                reg2conv.append(regconv2)
            i = 0
            seq2 = ''
            while i < regconv2[-1]:
                if i in regconv2:
                    seq2 += '1'
                else:
                    seq2 += '-'
                i += 1
            print(seq)
            print(seq2)


            # print(line.split('\t')[12].split('/n'))
            for el in line.split('\t')[10].split('/n'):
                print(el)

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

                numoverlap = int(line.split('\t')[15].split('/')[0])
                overlap = 0
                if numoverlap > 0:

                    overlap = round(int(line.split('\t')[15].split('/')[0]) / int(
                        line.split('\t')[15].split('/')[1]), 2)


                # lenghts = statistics.mean([int(line.split('\t')[4]),int(line.split('\t')[5])] )
                # print(count)
                x.append(identity)
                # x.append(identity)
                # y.append(overlap)
                y.append(overlap)

            # print(y)


            plt.scatter(x, y, alpha=0.5)
            plt.xlabel("identity")
            plt.ylabel("overlap/shortest region")
            plt.savefig('identity-region.png')


if __name__ == '__main__':
    sys.exit(main())