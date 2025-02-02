import argparse
import KeyScheduler as ks
import Tables as tables


# Argument parser for command line args.
def get_args():
    parser = argparse.ArgumentParser(">>> DES Cipher")
    parser.add_argument("-p", "--plaintext", help="Plaintext input", required=False, default="02468aceeca86420")
    parser.add_argument("-k", "--key", help="Key input", required=False, default="0f1571c947d9e859")
    return parser.parse_args()


# Converts binary to hexadecimal value. Omits '0x' in output.
def bin_to_hex(bin):
    bin = int(bin, 2)

    return hex(bin)[2:]


# Converts hex value to binary value. 
def hex_to_binary(hex):
    return f"{hex:064b}"


# Turns input (plaintext) into hexadecimal.
def hexify(pt):
    hex = "0x" + pt

    return int(hex, 16)


# Splits bit block into specified value.
def split_block(block, split_value):
    left = block[:split_value]
    right = block[split_value:]

    return left, right


def permutation(table, block):
    # Apply the permutation
    permuted_block = ''.join(block[pos - 1] for pos in table)

    return permuted_block


# # Applies the initial permutation using the ip table.
# def initial_permutation(block):
#     IP_TABLE = [
#         58, 50, 42, 34, 26, 18, 10, 2,
#         60, 52, 44, 36, 28, 20, 12, 4,
#         62, 54, 46, 38, 30, 22, 14, 6,
#         64, 56, 48, 40, 32, 24, 16, 8,
#         57, 49, 41, 33, 25, 17, 9, 1,
#         59, 51, 43, 35, 27, 19, 11, 3,
#         61, 53, 45, 37, 29, 21, 13, 5,
#         63, 55, 47, 39, 31, 23, 15, 7
#     ]

#     # Apply the permutation
#     permuted_block = ''.join(block[pos - 1] for pos in IP_TABLE)

#     return permuted_block


def sbox_sub(expanded_bits):
    S_BOXES = [
        # S1
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        # S2
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        # S3
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        # S4
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        # S5
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        # S6
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        # S7
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        # S8
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    ]
    
    output = ""  # Stores output value

    for i in range(8):
        # Extract 6 bits each iteration
        curr_6bits = expanded_bits[i * 6:(i + 1) * 6]

        row = int(curr_6bits[0] + curr_6bits[-1], 2)  # Get row from first and last bit

        col = int(curr_6bits[1:5], 2)  # Get column from middle 4 bits

        # Look up value, convert to 4 bits, and concat to output
        output += f"{S_BOXES[i][row][col]:04b}"
    
    return output


def xor_function(bin1, bin2, bit_length):
    bin1, bin2 = int(bin1, 2), int(bin2, 2)
    xor_result = bin1 ^ bin2

    return f"{xor_result:{bit_length}}"


def function_f(prev_r, curr_key):
    r_expansion_permutation = permutation(tables.E_TABLE, prev_r) 
    xor_r_key = xor_function(r_expansion_permutation, curr_key, '048b')
    sbox = sbox_sub(xor_r_key)
    p_permutation = permutation(tables.P_TABLE, sbox)
    
    return p_permutation


def des(block, keys):
    # Split block in half / 32 bits each
    l_prev, r_prev = split_block(block, 32)

    for n in range(16):  # 16 rounds
        # Left = previous R
        curr_l = r_prev 

        # Right = previous L XOR F(previous R, current key)
        curr_r = xor_function(l_prev, function_f(r_prev, keys[n]), '032b')

        # Initialize prev variables
        r_prev = curr_r
        l_prev = curr_l

    # Permutate using the IP Inverse table and swap L and R.
    binary_result = permutation(tables.IP_INVERSE_TABLE, curr_r + curr_l)
    
    return binary_result


# Runs the program.
def main():
    args = get_args()

    # Convert input to hexadecimals
    key = hexify(args.key)
    hex = hexify(args.plaintext)

    # Convert hex values to binary
    key = hex_to_binary(key)
    bin_block = hex_to_binary(hex)

    # Create subkeys from main key
    kplus = ks.pc1(key)
    shifted_keys = ks.lcs(kplus) 
    pc2_keys = ks.pc2(shifted_keys)


    ip_permutation = permutation(tables.IP_TABLE, bin_block)
    result = des(ip_permutation, pc2_keys)

    print(result)
    print(bin_to_hex(result))

    

if __name__ == "__main__":
    main()