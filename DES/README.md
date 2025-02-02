# Feistel-based Cipher (DES) Encryption and Decryption

This program implements a Feistel-based cipher for data excryption and decryption. 

The program takes a hexadecimal (size 16) plaintext and key, runs it through DES, and outputs the encrypted hexadecimal value. 

The program then takes the encrypted result and runs it through the decryption algorithm and outputs the plaintext value.

## Required Programs

- Python

## Running the program

### Files needed

- DES.py
- KeyScheduler.py
- Tables.py

Note: all files must be in the same directory.

Open a terminal and navigate to the file's location. 

```bash
python DES.py -p <plaintext_hex_value> -k <key_hex_value>
```

- p: plaintext hexadecimal
- k: key hexadecimal

Both plaintext and key must be of size 16 and valid hexadecimal values.

## Sample Input

```bash
python DES.py -p AD120028749AE219 -k 7920CDA123449021
```

## Sample Output

```bash
python DES.py -p 1234567890CADEF5 -k 12DD556780091FE1
Plaintext:  1234567890CADEF5
Key:        12DD556780091FE1
Encrypted:  7881802b8fb09155
Decrypted:  1234567890cadef5
```