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
python DES.py -p 1234567890CADEF5 -k 12DD55678001FE11
IP: L:ecdfc680    R:f08a6865
R0:   K:362408062514011B      L:f08a6865       R:f7bcc510 
R1:   K:0D10392338103F04      L:f7bcc510       R:fca59a0c 
R2:   K:3837020016080A1B      L:fca59a0c       R:60dbf745 
R3:   K:06081F141535100D      L:60dbf745       R:21c969dc 
R4:   K:1505001B02230728      L:21c969dc       R:0f35c458 
R5:   K:09380524280F2425      L:0f35c458       R:e2b32ef8 
R6:   K:2224220718203A32      L:e2b32ef8       R:b56b8c6d 
R7:   K:0E120C383710241B      L:b56b8c6d       R:dcbb449a 
R8:   K:183D220C29181C24      L:dcbb449a       R:bc860bc2 
R9:   K:060A070236003B02      L:bc860bc2       R:a55a47c6 
R10:   K:0C04303B170C081D      L:a55a47c6       R:20e0ae5d
R11:   K:3912040404371308      L:20e0ae5d       R:030c64a8
R12:   K:00283A152A0B0421      L:030c64a8       R:0d7241f8
R13:   K:1713003228263826      L:0d7241f8       R:c9b2b098
R14:   K:292813281F002E12      L:c9b2b098       R:0bf78ee2
R15:   K:200B0613212A0434      L:0bf78ee2       R:ce0352c2
IP inverse: L:b0ff68c8  R:2422676b

Plaintext:  1234567890CADEF5
Key:        12DD55678001FE11
Encrypted:  b0ff68c82422676b
Decrypted:  1234567890cadef5
```