import sys
with open('parse_needle/needle-parsed-out.txt', 'w+') as output:
  output.write('sequence1,sequence2,id1,id2,lenght1,lenght2,identity,similarity,gaps,score \n')
  # with open(inputfile, 'r') as input:
  id1 = ''
  id2 = ''
  seq1 = ''
  seq2 = ''
  len1 = ''
  for line in sys.argv[0]:
    if line.startswith("# 1:"):
      id1 = line.split(":")[1].strip()
      continue
    elif line.startswith("# 2:"):
      id2 = line.split(":")[1].strip()
      continue
    elif line.startswith("# Identity:"):
      identity = line.split(":")[1].strip()
      identity = identity[identity.find("(") + 1:identity.find(")")]
      continue
    elif line.startswith("# Similarity:"):
      similarity = line.split(":")[1].strip()
      similarity = similarity[similarity.find("(")+1:similarity.find(")")]
      continue
    elif line.startswith("# Gaps:"):
      gaps = line.split(":")[1].strip()
      gaps = gaps[gaps.find("(") + 1:gaps.find(")")]
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

  with open('disordered_sequences_splitted_fasta/' + id1 + '.fasta', 'r') as inputseq:
    for row in inputseq:
      if not row.startswith('>'):
        len1 = str(len(row))
        break
    inputseq.close()
    with open('disordered_sequences_splitted_fasta/' + id2 + '.fasta', 'r') as inputseq:
      for row in inputseq:
        if not row.startswith('>'):
          len2 = str(len(row))
          break
      inputseq.close()
      out = len1 + ',' + len2 + ',' + id1 + ',' + id2 + ',' + identity + ',' + similarity + ',' + gaps + ',' + score + ',' + seq1 + ',' + seq2
      print(out)
    output.write(out)
