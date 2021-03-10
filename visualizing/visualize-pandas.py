#!/usr/bin/env python3
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

def main():
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    visualize_overlap_identity(scriptdir)
    # visualize_identity(scriptdir)
    # visualize_overlap(scriptdir)

def visualize_overlap_identity(scriptdir):
    x, y, z, union_similar = [], [], [], []

    df = pd.read_csv(scriptdir + '/../rearrange/rearranged_files/dataframe-all.tsv', sep='\t')
    identitydf = pd.read_csv(scriptdir + '/../clustering/components-filtered.tsv', sep='\t')

    ids_identity = identitydf[['id1', 'identity']].sort_values(by=['id1'])
    union_similar = df.loc[(df.d2 == 1) | (df.d1 == 1)].groupby('id1').size().to_frame('union-similar')
    m1 = pd.merge(ids_identity, union_similar, left_on='id1', right_on='id1', how='left')
    overlap_similar = df.loc[(df.d2 == 1) & (df.d1 == 1)].groupby('id1').size().to_frame('overlap-similar')
    m2 = pd.merge(m1, overlap_similar, left_on='id1', right_on='id1', how='left')
    overlap_match = df.loc[(df.d2 == 1) & (df.d1 == 1) & (df.s1 == df.s2)].groupby('id1').size().to_frame('overlap-match')
    m3 = pd.merge(m2, overlap_match, left_on='id1', right_on='id1', how='left')
    print(m3)

    for value in m3['identity'].values:
        num = int(value.split('/')[0])
        den = int(value.split('/')[1])
        value = 0
        if num != 0 and den !=0:
            value = round((num / den  * 100), 2)
        x.append(value)

    i = 0
    while i < len(m3['overlap-similar'].values):
        ov_sim = 0
        ov_match = 0

        den = m3['union-similar'].values[i]
        num_sim = m3['overlap-similar'].values[i]
        num_match = m3['overlap-match'].values[i]


        if np.isnan(den) == False:
            if not np.isnan(num_sim):
                ov_sim = round((num_sim / den),2)
            if not np.isnan(num_match):
                ov_match = round((num_match / den),2)
        z.append(ov_sim)
        y.append(ov_match)
        i += 1


    print(x)
    print(y)
    print(z)


    my_dpi = 50
    fig = plt.figure( figsize=(20, 10), dpi=my_dpi)
    print(fig)

    fig.suptitle('overlap/union', fontsize=24)
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_title('overlap/union similar - overlap', fontsize=20)
    ax1.set_xlabel('identity', fontsize=20)
    cm = plt.cm.get_cmap('seismic')
    sc = ax1.scatter(x, z, c=y, cmap=cm)
    plt.colorbar(sc)


    ax2 = fig.add_subplot(1, 2, 2)
    ax2.scatter(x, y)
    ax2.set_xlabel('identity', fontsize=20)
    ax2.set_title('overlap/union match', fontsize=20)

    # union = NormalizeData(union)
    # print(union)
    # ax3 = fig.add_subplot(1, 3, 2)
    # sc3 = ax3.scatter(x, z, c=union, cmap=cm)
    # plt.colorbar(sc3)
    #
    # ax3.set_xlabel('identity', fontsize=20)
    # ax3.set_title('overlap/union similar - union', fontsize=20)

    fig.savefig('identity-overlap-new-pandas.png')

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def visualize_identity(scriptdir):

    data = []
    dict = {}
    ids = []
    data_overlap = []

    for filename in os.listdir(scriptdir + '/../rearrange/rearranged_files'):
        with open(scriptdir + '/../rearrange/rearranged_files/' + filename) as file:
            filename = filename.split('.')[0]

            for line in file:
                if line.startswith('>identity: '):
                    identitynum = line.split('>identity: ')[1].replace('\n', '').split('/')[0]
                    identity = round(
                        int(identitynum) / int(line.split('>identity: ')[1].replace('\n', '').split('/')[1]), 2)
                    identity = identity * 100
                if line.startswith('>overlap/union_match: '):
                    overlap = 0
                    numoverlap = int(line.split('>overlap/union_match: ')[1].split('/')[0])
                    if numoverlap > 0:
                        overlap = round(numoverlap / int(line.split('>overlap/union_match: ')[1].split('/')[1]), 2)
                    data_overlap.append(overlap)
                if filename in dict:
                    dict[filename.split('_')[0]].append(identity)
                else:
                    dict[filename.split('_')[0]] = []
                    dict[filename.split('_')[0]].append(identity)

    for key in dict:
        maxval = max(dict[key])
        ids.append(key)
        data.append(round(maxval, 2))
    print(data_overlap)
    # TODO add axes
    # plt.hist(data, bins=20) # do not run both plots toghether or the results will overlap
    # plt.gcf().savefig('max-identity.png')

    plt.hist(data_overlap, bins=20)
    plt.gcf().savefig('overlap-match-hist.png')

# def visualize_identity(scriptdir):
#
#         data = []
#         dict = {}
#         ids = []
#
#         for filename in os.listdir(scriptdir + '/../rearrange/rearranged_files'):
#             with open(scriptdir + '/../rearrange/rearranged_files/' + filename) as file:
#                 filename = filename.split('.')[0]
#
#                 for line in file:
#                     if line.startswith('>identity: '):
#                         identitynum = line.split('>identity: ')[1].replace('\n', '').split('/')[0]
#                         identity = round(
#                             int(identitynum) / int(line.split('>identity: ')[1].replace('\n', '').split('/')[1]), 2)
#                         identity = identity * 100
#
#                     elif line.startswith('>overlap/union: '):
#                         overlap = 0
#                         numoverlap = int(line.split('>overlap/union: ')[1].split('/')[0])
#                         if numoverlap > 0:
#                             overlap = round(numoverlap / int(line.split('>overlap/union: ')[1].split('/')[1]), 2)
#                         if overlap >= 0.3:
#
#                             if filename in dict:
#                                 dict[filename].append(identity)
#                                 # dict[filename].append(overlap)
#                             else:
#                                 dict[filename] = []
#                                 dict[filename].append(identity)
#
#                                 # dict[filename].append(overlap)
#
#         for key in dict:
#             maxval = max(dict[key])
#             ids.append(key)
#             data.append(maxval)
#         print(dict)
#         i = 0
#         lenids = len(ids)
#         while i < lenids:
#
#             stop = i + 50
#             subsetids = ids[i:stop]
#             subsetdata = data[i:stop]
#             y_pos = np.arange(len(subsetids))
#
#             # Create bars
#             plt.bar(y_pos, subsetdata)
#
#             # Create names on the x-axis
#             plt.xticks(y_pos, subsetids, rotation=90)
#
#             plt.savefig('hist_identity/subset' + str(i) + '.png')
#             # plt.savefig('hist_overlap/subset' + str(i) + '.png')
#             i += 50
#             plt.clf()
#             print(i)


# def visualize_alignments(scriptdir):
#
#     with open(scriptdir + '/alignments.tsv', 'w+') as out:
#         with open(scriptdir + '/../clustering/components-union-overlap.tsv', 'r') as input:
#             for line in input:
#
#                 id2 = line.split('\t')[3].split(',')[0]
#                 id1 = line.split('\t')[2].split(',')[0]
#                 align1 = ''
#                 align2 = ''
#                 alignoutput = line.split('#=')[1].split('/n')
#                 for row in alignoutput:
#                     if row.startswith(id1):
#                         row = row.split(id1)[1].strip()
#                         row = ''.join([i for i in row if not i.isdigit()]).strip()
#                         align1 += row
#                 for row in alignoutput:
#                     if row.startswith(id2):
#                         row = row.split(id2)[1].strip()
#                         row = ''.join([i for i in row if not i.isdigit()]).strip()
#                         align2 += row
#                 m = max([len(align1), len(align2)])
#
#                 # print(line)
#                 print(line.split('\t')[15].split('/n'))
#                 print(line.split('\t')[11].split('/n'))
#                 reg1 = line.split('\t')[11].split(',')
#                 reg1conv = []
#                 for reg in reg1:
#                     start1 = reg.split('_')[1].split('-')[0]
#                     end1 = reg.split('_')[1].split('-')[1]
#                     regconv = list(range(int(start1), int(end1)))
#                     reg1conv.append(regconv)
#                 j = 0
#                 seq = ''
#
#                 # print(regconv)
#                 if type(regconv[0]) is not int:
#                     joined1 = []
#                     for lista2 in reg2conv:
#                         for el in lista2:
#                             joined1.append(el)
#                     while j < m:
#
#                         if j in joined1:
#                             seq += '1'
#                         else:
#                             seq += '0'
#                         j += 1
#                 else:
#                     while j < m:
#
#                         if j in regconv:
#                             seq += '1'
#                         else:
#                             seq += '0'
#                         j += 1
#
#                 print(line.split('\t')[12].split('/n'))
#
#                 reg2 = line.split('\t')[12].split(',')
#                 reg2conv = []
#                 for reg in reg2:
#                     start2 = reg.split('_')[1].split('-')[0]
#                     end2 = reg.split('_')[1].split('-')[1]
#                     regconv2 = list(range(int(start2), int(end2)))
#                     reg2conv.append(regconv2)
#                 i = 0
#                 seq2 = ''
#                 # print(reg2conv)
#                 # print( regconv2[len(regconv2)-1])
#
#                 if type(reg2conv[0]) is not int:
#
#                     i = 1
#                     joined = []
#                     for lista2 in reg2conv:
#                         for el in lista2:
#                             joined.append(el)
#
#
#                     while i <= m:
#
#                         if i in joined:
#                             seq2 += '1'
#                         else:
#                             seq2 += '0'
#                         i += 1
#
#                 else:
#                     while i <= m:
#                             if i in reg2conv:
#                                 seq2 += '1'
#                             else:
#                                 seq2 += '0'
#                             i += 1
#
#
#
#
#                 print(seq)
#                 print(seq2)
#                 k = 1
#                 start = 0
#                 end = 150
#                 out.write("overlap/union: " + line.split('\t')[14].split('/n')[0] + '\n')
#                 out.write("overlap/shortest region: " + line.split('\t')[15].split('/n')[0])
#                 l = max([len(align1), len(align2), len(seq), len(seq2)])
#                 out.write(id1 + ' ' + id2 + '\n')
#                 out.write(str(reg1) + '\n')
#                 out.write(str(reg2) + '\n')
#
#                 while k < l:
#                     while start < l:
#                         print(start)
#                         print(end)
#
#                         out.write(seq[start:end] + '\n')
#                         out.write(align1[start:end] + '\n')
#                         out.write(align2[start:end] + '\n')
#                         out.write(seq2[start:end] + '\n' + '\n')
#                         start += 150
#                         end += 150
#                     k += 1


# def visualize_overlap_identity(scriptdir):
#
#         flag = 0
#         with open(scriptdir + '/../clustering/components-union-overlap.tsv', 'r') as input:
#             x, y = [], []
#             count = 0
#
#             for line in input:
#                 id1 = line.split('\t')[0]
#                 id2 = line.split('\t')[2]
#                 count +=1
#
#                 identity = round(int(line.split('\t')[6].split('/')[0]) / int(
#                         line.split('\t')[6].split('/')[1]), 2)
#                 identity = identity * 100
#                 # identity = int(line.split('\t')[6].split('/')[0])
#                 if identity > flag:
#                     flag = identity
#
#                 # numoverlap = int(line.split('\t')[15].split('/')[0])
#                 numoverlap = int(line.split('\t')[14].split('/')[0])
#                 overlap = 0
#                 if numoverlap > 0:
#
#                     # overlap = round(int(line.split('\t')[15].split('/')[0]) / int(
#                     #     line.split('\t')[15].split('/')[1]), 2)
#                     overlap = round(int(line.split('\t')[14].split('/')[0]) / int(
#                         line.split('\t')[14].split('/')[1]), 2)
#
#
#                 # lenghts = statistics.mean([int(line.split('\t')[4]),int(line.split('\t')[5])] )
#                 # print(count)
#                 x.append(identity)
#                 # x.append(identity)
#                 # y.append(overlap)
#                 y.append(overlap)
#
#             # print(y)
#
#
#             plt.scatter(x, y, alpha=0.5)
#             plt.xlabel("identity")
#             # plt.ylabel("overlap/shortest region")
#             plt.ylabel("overlap/union region")
#             # plt.savefig('identity-region.png')
#             plt.savefig('identity-overlap.png')


if __name__ == '__main__':
    sys.exit(main())