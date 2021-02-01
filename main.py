# This is a sample Python script.
import os
import pathlib

from Bio.Emboss.Applications import NeedleCommandline
from Bio.Emboss.Applications import WaterCommandline


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
  # Use a breakpoint in the code line below to debug your script.
  print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# create the couples
# creating a triangular matrix
def create_pairwise_sequences():
  curdir = pathlib.Path().absolute()
  curpath = str(curdir) + "/disordered_sequences_splitted_fasta"

  totalfiles = []
  pairwise_sequences = {}
  # with open('alignments_global_needle/global_triangular_matrix.csv', 'w+') as global_triangular_matrix:
  #   global_triangular_matrix.write(f'protein1, protein2 \n')
  with open('alignments_global_needle/global_triangular_matrix.csv', 'w') as global_triangular_matrix:
    global_triangular_matrix.write(f'protein1,protein2 \n')
    for filename1 in os.listdir(curpath):

      totalfiles.append(filename1.split(".")[0])
      i = os.listdir(curpath).index(filename1)
      for filename2 in os.listdir(curpath)[i:-1]:
          if pairwise_sequences.get(filename1.split(".")[0], -1) == -1:
            pairwise_sequences[filename1.split(".")[0]] = []
          else:
            pairwise_sequences[filename1.split(".")[0]].append(filename2.split(".")[0])
            global_triangular_matrix.write(filename1.split(".")[0]+ ',' + filename2.split(".")[0] + '\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
  # create_pairwise_sequences()
  needle_cline = NeedleCommandline(asequence="beta.faa", bsequence="alpha.faa", gapopen=10, gapextend=0.5,
                                   outfile="needle2.txt")  # output stringa unica in file
  print(needle_cline)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
