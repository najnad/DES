import argparse
import KeyScheduler as ks
from Tables import P_TABLE, E_TABLE, IP_INVERSE_TABLE, IP_TABLE, S_BOXES


# Argument parser for command line args.
def get_args():
    parser = argparse.ArgumentParser(">>> DES Cipher")
    parser.add_argument("-p", "--plaintext", help="Plaintext input", required=True)
    parser.add_argument("-k", "--key", help="Key input", required=True)
    return parser.parse_args()


# Validates the plaintext and key.
# Returns True if validation passed.
def validate_input(plaintext, key):
    # Check if plaintext and key are 16 characters long.
    if len(plaintext) != 16 or len(key) != 16: 
        print(">>> Plaintext and key must be 16 characters long.")
        return False
    
    try:  # Check for invalid hex values.
        hexify(plaintext)
        hexify(key)
    except ValueError:
        print(">>> Invalid hex values found.")
        return False
    
    return True


# Converts binary to hexadecimal value. 
# Omits '0x' in output and adds leading zeros if length < 16.
def bin_to_hex(bin):
    bin = int(bin, 2)
    return hex(bin)[2:].zfill(16)


# Converts hex value to binary value. 
def hex_to_binary(hex):
    return f"{hex:064b}"


# Turns input into hexadecimal.
def hexify(pt):
    hex = "0x" + pt
    return int(hex, 16)


# Splits bit block into specified value.
def split_block(block, split_value):
    left = block[:split_value]
    right = block[split_value:]

    return left, right


# Applies specified permuation to the bit block given.
def permutation(table, block):
    permuted_block = ''.join(block[pos - 1] for pos in table)

    return permuted_block


# Implements the S-box substitution in DES.
def sbox_sub(expanded_bits):    
    output = ""  # Stores output value

    for i in range(8):
        # Extract 6 bits each iteration
        curr_6bits = expanded_bits[i * 6:(i + 1) * 6]

        # Get row from first and last bit
        row = int(curr_6bits[0] + curr_6bits[-1], 2)  

        # Get column from middle 4 bits
        col = int(curr_6bits[1:5], 2)  

        # Look up value, convert to 4 bits, and concat to output
        output += f"{S_BOXES[i][row][col]:04b}"
    
    return output


# XOR function that returns value in specified bit format.
def xor_function(bin1, bin2, bit_length):
    bin1, bin2 = int(bin1, 2), int(bin2, 2)
    xor_result = bin1 ^ bin2

    return f"{xor_result:{bit_length}}"


# Implements the F function in DES.
def function_f(prev_r, curr_key):
    # E-bit selection
    r_expansion_permutation = permutation(E_TABLE, prev_r)

    # Right bits XOR current key
    xor_r_key = xor_function(r_expansion_permutation, curr_key, '048b')

    # S-Box Substitution
    sbox = sbox_sub(xor_r_key)

    # P table permutation
    p_permutation = permutation(P_TABLE, sbox)
    
    return p_permutation


# Encodes and decodes using DES. 
def des(block, keys, encode):
    if encode:  # if encode == True, encrypt
        sequence = range(16)
    else:  # decrypt
        sequence = reversed(range(16))

    # Permutate using IP table
    ip_permutation = permutation(IP_TABLE, block)

    # Split block in half / 32 bits each
    l_prev, r_prev = split_block(ip_permutation, 32)

    for round in sequence:  # 16 rounds
        # Left = previous R
        curr_l = r_prev 

        # Right = previous L XOR F(previous R, current key)
        curr_r = xor_function(l_prev, function_f(r_prev, keys[round]), '032b')

        # Initialize prev variables
        r_prev = curr_r
        l_prev = curr_l

    # Permutate using the IP Inverse table and swap L and R.
    ip_inverse = permutation(IP_INVERSE_TABLE, curr_r + curr_l)
    
    return ip_inverse


# Function to print output in readable format.
def print_results(plaintext, key, encrypted_result, decrypted_result):
    print(f"Plaintext:  {plaintext}")
    print(f"Key:        {key}")
    print(f"Encrypted:  {encrypted_result}")
    print(f"Decrypted:  {decrypted_result}")


# Runs the program.
def main():
    args = get_args()

    if validate_input(args.plaintext, args.key):
        # Convert input to hexadecimals
        key = hexify(args.key)
        plaintext = hexify(args.plaintext)

        # Convert hex values to binary
        bin_key = hex_to_binary(key)
        bin_block = hex_to_binary(plaintext)

        # Create keys
        keys = ks.create_keys(bin_key)

        # DES functions
        encrpyted = des(bin_block, keys, True)  # Encrypt
        decrypted = des(encrpyted, keys, False)  # Decrypt

        # Print results
        print_results(args.plaintext, args.key, bin_to_hex(encrpyted), bin_to_hex(decrypted))


if __name__ == "__main__":
    main()