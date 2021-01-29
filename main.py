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


needle_cline = NeedleCommandline(asequence="beta.faa", bsequence="alpha.faa", gapopen=10, gapextend=0.5,
                                 outfile="needle2.txt")
print(needle_cline)


def create_pairwise_sequences():
  curdir = pathlib.Path().absolute()
  curpath = str(curdir) + "/disordered_sequences_splitted_fasta"
  print(os.listdir(curpath))  # Press Ctrl+F8 to toggle the breakpoint.

  totalfiles = []
  pairwise_sequences = {}
  for filename1 in os.listdir(curpath):
    totalfiles.append(filename1.split(".")[0])
    for filename2 in os.listdir(curpath):
        pairwise = filename1.split(".")[0] + "_" + filename2.split(".")[0]
        pairwise_reverse = filename2.split(".")[0] + "_" + filename1.split(".")[0]
        # if filename1 != filename2:
        if pairwise_sequences.get(pairwise, -1) == -1:
          if pairwise_sequences.get(pairwise_reverse, -1) == -1:
            pairwise_sequences[pairwise] = ''

  print(len(totalfiles))
  print(len(pairwise_sequences))


# needle_cline = NeedleCommandline(asequence="beta.faa", bsequence="alpha.faa", gapopen=10, gapextend=0.5,
#                                  outfile="needle2.txt")
# print(needle_cline)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
  create_pairwise_sequences()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
