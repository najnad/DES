import argparse
import KeyScheduler as ks


# Argument parser for command line args.
def get_args():
    parser = argparse.ArgumentParser(">>> DES Cipher")
    parser.add_argument("-p", "--plaintext", help="Plaintext input", required=False)
    parser.add_argument("-k", "--key", help="Key input", required=False)
    return parser.parse_args()


# Converts hex value to binary value. 
def hex_to_binary(hex):
    return f"{hex:064b}"


# Turns input (plaintext) into hexadecimal.
def hexify(pt):
    hex = "0x" + pt
    return int(hex, 16)


# Applies the initial permutation using the ip table.
def initial_permutation(block):
    IP_TABLE = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

    # Apply the permutation
    permuted_block = ''.join(block[pos - 1] for pos in IP_TABLE)

    return permuted_block


def des(block):
    pass


# Runs the program.
def main():
    args = get_args()

    # hex = hexify(args.plaintext)
    # bin_block = hex_to_binary(hex)

    # test = initial_permutation(bin_block)

    key = hexify(args.key)
    key = hex_to_binary(key)
    kplus = ks.pc1(key)

    shifted_keys = ks.lcs(kplus)
    pc2_keys = ks.pc2(shifted_keys)


if __name__ == "__main__":
    main()
    