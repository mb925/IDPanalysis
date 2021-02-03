import argparse
import os
import sys

def main():
  parse_file()


def parse_file():
  curdir = os.getcwd()
  args = parse_arguments()


  id1 = ''
  id2 = ''
  seq1 = ''
  seq2 = ''
  len1 = ''
  with open(args.i, 'r') as input:
    for line in input:
      if line.startswith("# 1:"):

        id1 = line.split(":")[1].strip()
        continue
      elif line.startswith("# 2:"):
        id2 = line.split(":")[1].strip()
        continue
      elif line.startswith("# Identity:"):
        identity = line.split(":")[1].strip()
        identity = identity.split('(')[0].strip()
        continue
      elif line.startswith("# Similarity:"):
        similarity = line.split(":")[1].strip()
        similarity = similarity.split('(')[0].strip()
        continue
      elif line.startswith("# Gaps:"):
        gaps = line.split(":")[1].strip()
        gaps = gaps.split('(')[0].strip()
        continue
      elif line.startswith("# Score:"):
        score = line.split(":")[1].strip()
        continue
      elif id1 != '' and line.startswith(id1):
        sequence = line.split(id1)[1]
        seq1 += ''.join([i for i in sequence if not i.isdigit()]).strip()
        continue
      elif id2 != '' and line.startswith(id2):
        sequence = line.split(id2)[1]
        seq2 += ''.join([i for i in sequence if not i.isdigit()]).strip()
        continue

    with open(curdir + '/disordered_sequences_splitted_fasta/' + id1 + '.fasta', 'r') as inputseq:
      for row in inputseq:
        if not row.startswith('>'):
          len1 = str(len(row))
          break

    with open(curdir + '/disordered_sequences_splitted_fasta/' + id2 + '.fasta', 'r') as inputseq:
      for row in inputseq:
        if not row.startswith('>'):
          len2 = str(len(row))
          break

  out = id1 + ',' + id2 + ',' + len1 + ',' + len2 + ',' + identity + ',' + similarity + ',' + gaps + ',' + score + ',' + seq1 + ',' + seq2
  print(out) # script output


def parse_arguments(initargs=None):
  if initargs is None:
    initargs = []
  parser = argparse.ArgumentParser(description="Parse input alignment file.")
  parser.add_argument('-i', required=True, help="Input alignment file")
  if not initargs or len(sys.argv) > 1:
    args = parser.parse_args()
  else:
    args = parser.parse_args(initargs)
  return args


if __name__ == '__main__':
  sys.exit(main())
