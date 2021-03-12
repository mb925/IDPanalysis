#!/usr/bin/env python3
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # visualize_overlap_identity(script_dir)
    # visualize_overlap_identity_hist(script_dir)
    visualize_alignments(script_dir)


def visualize_overlap_identity(script_dir):
    ident, over_mat, over_mis, union_similar = [], [], [], []

    df = pd.read_csv(script_dir + '/../rearrange/all-dataframe.tsv', sep='\t')
    # print(df)
    identity_df = pd.read_csv(script_dir + '/../clustering/components-filtered.tsv', sep='\t')

    ids_identity = identity_df[['id1', 'id2', 'identity']].sort_values(by=['id1'])
    union_similar = df.loc[(df.d2 == 1) | (df.d1 == 1)].groupby(['id1', 'id2']).size().to_frame('union-similar')

    m1 = pd.merge(ids_identity, union_similar, on=['id1', 'id2'])
    # print(m1)
    overlap_similar = df.loc[(df.d2 == 1) & (df.d1 == 1)].groupby(['id1', 'id2']).size().to_frame('overlap-similar')
    m2 = pd.merge(m1, overlap_similar, on=['id1', 'id2'], how='outer')
    # print(m2)
    overlap_match = df.loc[(df.d2 == 1) & (df.d1 == 1) & (df.s1 == df.s2)].groupby(['id1', 'id2']).size().to_frame(
        'overlap-match')
    m3 = pd.merge(m2, overlap_match, on=['id1', 'id2'], how='outer')
    print(m3)

    for value in m3['identity'].values:
        num = int(value.split('/')[0])
        den = int(value.split('/')[1])

        value = 0
        if num != 0:
            value = (num / den) * 100
        ident.append(round(value, 2))

    m3['identity'] = m3['identity'].replace(m3['identity'].values, ident)

    i = 0
    while i < len(m3['overlap-similar'].values):
        ov_sim = 0
        ov_match = 0
        num_sim = 0
        num_match = 0
        den = m3['union-similar'].values[i]

        if not np.isnan(m3['overlap-similar'].values[i]):
            num_sim = int(m3['overlap-similar'].values[i])
        if not np.isnan(m3['overlap-match'].values[i]):
            num_match = int(m3['overlap-match'].values[i])

        if num_sim != 0:
            ov_sim = round((num_sim / den), 2)
        if num_match != 0:
            ov_match = round((num_match / den), 2)
        over_mis.append(ov_sim)
        over_mat.append(ov_match)
        i += 1

    m3['overlap-similar/union'] = over_mis

    m3.to_csv(script_dir + '/overlap-union-identity.csv', index=None, sep='\t')

    fig = plt.figure(figsize=(20, 10), dpi=50)

    fig.suptitle('overlap/union', fontsize=24)
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.set_title('colored by overlap match')
    ax1.set_ylabel('overlap/union similar', fontsize=20)
    ax1.set_xlabel('identity', fontsize=20)
    cm = plt.cm.get_cmap('seismic')
    sc = ax1.scatter(ident, over_mis, c=over_mat, cmap=cm)
    plt.colorbar(sc)
    plt.show()

    ax2 = fig.add_subplot(1, 3, 2)
    ax2.scatter(ident, over_mat)
    ax2.set_xlabel('identity', fontsize=20)
    ax2.set_ylabel('overlap/union match', fontsize=20)

    union = normalize_data(m3['union-similar'])
    ax3 = fig.add_subplot(1, 3, 3)
    sc3 = ax3.scatter(ident, over_mis, c=union, cmap=cm)
    plt.colorbar(sc3)

    ax3.set_xlabel('identity', fontsize=20)
    ax3.set_title('overlap/union similar - union similar', fontsize=20)

    fig.savefig('identity-overlap.png')


def normalize_data(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def visualize_overlap_identity_hist(script_dir):
    data = []
    dict = {}
    ids = []
    data_overlap = []

    df = pd.read_csv(script_dir + '/overlap-union-identity.csv', sep='\t')
    for i, id1 in enumerate(df['id1']):
        data_overlap.append(df['overlap-similar/union'][i])

        if id1 in dict:
            dict[id1].append(df['identity'][i])

        else:
            dict[id1.split('_')[0]] = []
            dict[id1.split('_')[0]].append(df['identity'][i])
    print(dict)
    for key in dict:
        max_val = max(dict[key])
        ids.append(key)
        data.append(round(max_val, 2))

    print(sorted(data_overlap))

    # plt.hist(data, bins=20) # !!!do not run both plots together or the results will overlap
    # plt.xlabel('max identity')
    # plt.ylabel('# proteins')
    # plt.gcf().savefig('max-identity.png')

    plt.xlabel('overlap')
    plt.ylabel('# pairs')
    plt.hist(data_overlap, bins=20)
    plt.gcf().savefig('overlap-similar-hist.png')


def visualize_alignments(script_dir):
    df = pd.read_csv(script_dir + '/../rearrange/all-dataframe.tsv', sep='\t')
    m3 = pd.read_csv(script_dir + '/overlap-union-identity.csv', sep='\t')
    improvable_regions = m3.loc[(m3['overlap-similar/union'] <= 0.5) & (m3['identity'] >= 80)][['id1', 'id2']]
    bad_alignments_dataset = df.merge(improvable_regions, on=['id1', 'id2'], how='right')
    bad_alignments_dataset.to_csv(script_dir + '/improvable_regions.csv', index=None, sep='\t')


if __name__ == '__main__':
    sys.exit(main())
