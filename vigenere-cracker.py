#!/usr/bin/env python3

from __future__ import division
import re
import string
import sys, getopt
import json

DEFAULT_PLAINTEXT="WEHAVESEENTHATMONOALPHABETICCIPHERSAREPRONETOSTATISTICALATTACKSSINCETHEYPRESERVETHESTATISTICALSTRUCTUREOFTHEPLAINTEXTTOOVERCOMETHISISSUEITISIMPORTANTTHATTHESAMEPLAINSYMBOLISNOTALWAYSMAPPEDTOTHESAMEENCRYPTEDSYMBOLWHENTHISHAPPENSTHECIPHERISCALLEDPOLYALPHABETIC"
DEFAULT_CI_LIMIT=0.052

# GENERAL UTILITIES

def shift_letter(n, c):
  return chr(int(((ord(c) - 65 + n) % 26) + 65))

def shift_text(text, n):
  new_text = ""
  for c in text:
    new_text += shift_letter(n, c)
  return new_text

def get_subcyphers(cypher, m):
  i = 0;
  subcyphers = []
  for s in range(m):
    subcyphers.append("")
  for c in cypher:
    subcyphers[i % m] += c
    i += 1
  return subcyphers

def get_letter_frequency_in_text(letter, text):
  frequency = 0
  for c in text:
    if c == letter:
      frequency += 1
  return frequency

# KEY LENGTH

def get_coincidence_index(text):
  text = text.upper()
  total_frequency = 0
  for c in string.ascii_uppercase:
    frequency = get_letter_frequency_in_text(c, text)
    total_frequency += (frequency * (frequency - 1))
  return total_frequency / (len(text) * (len(text) - 1))

def get_key_length(cypher, limit):
  m = 1
  found = False
  while (not found):
    found = True
    subcyphers = get_subcyphers(cypher, m)
    for sub in subcyphers:
      index = get_coincidence_index(sub)
      if index < limit:
        found = False
        m += 1
        break
  return m

# ARRAY OF SHIFTS

def get_mutual_coincidence_index(text1, text2):
  text1 = text1.upper()
  text2 = text2.upper()
  frequency = 0
  for c in string.ascii_uppercase:
    frequency += (get_letter_frequency_in_text(c, text1) * get_letter_frequency_in_text(c, text2))
  return frequency / (len(text1) * len(text2))

def get_relative_shift(text1, text2):
  k = 0
  mick = 0
  for j in range(0,26):
    mic = get_mutual_coincidence_index(text1, shift_text(text2, j))
    if mic > mick:
      k = j
      mick = mic
  return k

def get_shift_list(cypher, m):
  key = []
  subcyphers = get_subcyphers(cypher, m)
  for i in range(0,m):
    k = get_relative_shift(subcyphers[0], subcyphers[i])
    key.append(k)
  return key

# DECRYPTION

def decrypt(cypher, shifts, plaintext):
  index = 0
  text = ""
  new_shifts = []
  decrypted_text = ""
  for c in cypher:
    text += shift_letter(shifts[index % len(shifts)], c)
    index += 1
  final_shift = get_relative_shift(text, plaintext)
  for s in shifts:
    new_shifts.append((s - final_shift) % 26)
  index = 0
  for c in cypher:
    decrypted_text += shift_letter(new_shifts[index % len(new_shifts)], c)
    index += 1

  return {
    "key": "".join(map(lambda x: chr(int((26-x) + 65)), new_shifts)),
    "decrypted_text": decrypted_text
  }

# MAIN FUNCTION

def main(argv):
  cypher=""
  finput=""
  foutput=""
  fplaintext=""
  plaintext=DEFAULT_PLAINTEXT
  coincidence_limit=DEFAULT_CI_LIMIT
  alphabetic_chars_only = re.compile('[^a-zA-Z]')
  usage_message = "Usage: vigenere-cracker.py -i <input_file> [-o <output_file>] [-p <plaintext_example_file>] [-c <coincidence_limit>]"

  try:
    opts, args = getopt.getopt(argv, "hi:o:p:f:c:")
  except getopt.GetoptError:
    print(usage_message)
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print(usage_message)
      sys.exit()
    elif opt == '-i':
      finput = arg
    elif opt == '-o':
      foutput = arg
    elif opt == '-p':
      fplaintext = arg
      file = open(fplaintext, "r")
      plaintext = alphabetic_chars_only.sub('', file.read().upper())
      file.close()
    elif opt == '-c':
      coincidence_limit = float(arg)

  if finput == "":
    print("Error: must provide input file")
    print(usage_message)
    sys.exit(2)
  else:
    file = open(finput, "r")
    cypher = alphabetic_chars_only.sub('', file.read().upper())

  m = get_key_length(cypher, coincidence_limit)
  shifts = get_shift_list(cypher, m)
  result = decrypt(cypher, shifts, plaintext)

  if foutput != "":
    file = open(foutput, 'w')
    file.write(json.dumps(result))
    file.close()
  else:
    print(result)

if __name__ == "__main__":
  main(sys.argv[1:])
