# py-vigenere-cracker
A simple python cracker for Vigenére ciphers.

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://gitHub.com/Mr5he11/py-vigenere-cracker/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Mr5he11/py-vigenere-cracker/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://gitHub.com/Mr5he11/py-vigenere-cracker/releases/)

### Usage

`py-vigenere-cracker.py -i <input_file> [-o <output_file>][-p <plaintext_file>][-c <coincidence_index_value>]`

For the cracking algorithm is based on the coincidence index of a language (each language has a characteristic coincidence index) - representing the different letters distribution -, it is needed a coincidence index value (by default it is 0.052 for english). 

Also, a plaintext in the text language is needed, by default it is an english plaintext.
