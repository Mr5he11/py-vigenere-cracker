#!/usr/bin/env python
from __future__ import division
import string

def get_subcyphers(cypher, m):
  i = 0;
  subcyphers = range(m)
  for s in range(m):
    subcyphers[s] = ""
  for c in cypher:
    subcyphers[i % m] += c
    i += 1
  return subcyphers

def shift_letter(n, c):
  return chr(((ord(c) - 65 + n) % 26) + 65)

def shift_text(text, n):
  new_text = ""
  for c in text:
    new_text += shift_letter(n, c)
  return new_text

def get_letter_frequency_in_text(letter, text):
  frequency = 0
  for c in text:
    if c == letter:
      frequency += 1
  return frequency

def get_coincidence_index(text):
  text = text.upper()
  total_frequency = 0
  for c in string.ascii_uppercase:
    frequency = get_letter_frequency_in_text(c, text)
    total_frequency += (frequency * (frequency - 1))
  return total_frequency / (len(text) * (len(text) - 1))

def get_mutual_coincidence_index(text1, text2):
  text1 = text1.upper()
  text2 = text2.upper()
  frequency = 0
  for c in string.ascii_uppercase:
    frequency += (get_letter_frequency_in_text(c, text1) * get_letter_frequency_in_text(c, text2))
  return frequency / (len(text1) * len(text2))

def get_key_length(cypher):
  LIMIT = 0.052
  m = 1
  found = False
  while (not found):
    found = True
    subcyphers = get_subcyphers(cypher, m)
    for sub in subcyphers:
      index = get_coincidence_index(sub)
      if index < LIMIT:
        found = False
        m += 1
        break
  return m

def get_shift_list(cypher, m):
  key = []
  subcyphers = get_subcyphers(cypher, m)
  for i in range(0,m):
    k = 0
    mick = 0
    for j in range(0,26):
      mic = get_mutual_coincidence_index(subcyphers[0], shift_text(subcyphers[i], j))
      if mic > mick:
        k = j
        mick = mic
    key.append(k)
  return key

def decrypt(cypher, shifts):
  for i in range(0, 26):
    new_shifts = []
    for s in shifts:
      new_shifts.append(s + i)
    index = 0
    decrypted_text = ""
    for c in cypher:
      decrypted_text += shift_letter(new_shifts[index % len(shifts)], c)
      index += 1
    decrypted_text += "\n"
    separator = ""
    print "key: " + separator.join(map(lambda x: chr(x + 65), new_shifts))
    print "decrypted text: " + decrypted_text



def main():
  cypher = "WTTNRAVWSKAMFFEVREBKZXMKLCLANMOZSWDXKOHKTQDMCDVWOIIUHXZWXIYVNRYSWNUZAFCVZEUMIKKUXSGFYMZCGADGVYBIZSZXPPCIYMEZIXZWXWZVUIMWZYNIJOWACPNHDRXHOXALDIOYBTDGKALIKGNKZYIIMWRZCSFKEVTENRYAYGNMKLDMFDRSAESUIOLZKCRSGEGMTKQMLZKCEAVGOYIKMSJUKVGPEWVXZUHWGKDMHLFGJRJOXIJAJOTYUIMSNTGMFVWAHPYPVWJNYGGMHLQZEXCIYUNHSQIIOPUIMJVKFZWJUAWPRTTEEJMXMHELHSRXCIIZBIHDAIDFEIJJDGEMFYWLLTFCXLROHAGMHLMPJSMXYZBILJKCMWRSAKVZNMFYQXLYQTDGBOHKLZALLTFMZWNNYRKMZLPYYCVAYONIJSXJTEJMOLGOHOWQAACLAGGSJKVCZWNBSPEIREJTIXZAJODZIIMCIKGEJCWJWPVROLRZHSJVELLWVGZXYOHOALOWGPECHYTNIYLGBBSPJETXFNYEJLDMCLOFDXJGSXGAPAPWSSCHVGLSZVAICTFLVPCHYPSLAESPAWCIKNIYYZPQEZIIMEWZYVOSNLDTGSXGLXLIVLKPPCGLVXJNYSMYDBEZUEQINUHHWJALLEGLDWSANELLDMETZIDXRRFWWWIMOBHMOIEGNYJSHJFEJLZRKNYVSTXQELPXPECRSXGGGIHLGGCSLZIJALOELTFXXSRZJSUCABLYQPJSBKXELAPIYOGLZRYALVAWZWYLYMXIJZUVLWZBZSRVAIVZZSJAPNWLFLZHRILSKKDMCXVRYXYGNWZWDIOYRZZVSKZSJWOMPYNVVFSONAALDMTEUIMENGCWLUKIEABGFIKULEOSPKSEBXVOVUOXGXEBLYQFPVEOHKOAPPNFEMJWZZSWZWNIYLPVJWJZBIXAATOLSXZVZZURVXKZEFAEOICEQEKBQAETAXDQVZIWWWEBAZCHJAEGFEJYAZLMOMOLFRYYFVAZESRLZHXK"
  m = get_key_length(cypher)
  shifts = get_shift_list(cypher, m)
  decrypt(cypher, shifts)

if __name__ == "__main__":
  main()