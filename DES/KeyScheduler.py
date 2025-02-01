# Implements the PC-1 function. Permutates 64-bit key into 56-bits.
def pc1(key_block):
    PC1_TABLE = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]

    permuted_key = ''.join(key_block[pos - 1] for pos in PC1_TABLE)
    
    return permuted_key


# Implements the PC-2 functions. Permutates 56-bit key into 48-bits.
def pc2(shifted_keys):
    PC2_TABLE = [
        14, 17, 11, 24,  1,  5, 
        3, 28, 15,  6, 21, 10, 
        23, 19, 12,  4, 26,  8, 
        16,  7, 27, 20, 13,  2, 
        41, 52, 31, 37, 47, 55, 
        30, 40, 51, 45, 33, 48, 
        44, 49, 39, 56, 34, 53, 
        46, 42, 50, 36, 29, 32
    ]
    
    permuted_keys = []  # Used to store shifted keys

    # Iterate through list of keys and permutate.
    for key in shifted_keys:
        curr_key = ''.join(key[pos - 1] for pos in PC2_TABLE)
        permuted_keys.append(curr_key)

    return permuted_keys


# Performs left shift on a set of bits. Shift varies (1, 2) depending on the round.
def left_shift(bits, shifts):
    return bits[shifts:] + bits[:shifts]


# Perform Left Circular Shifts on each half for 16 rounds.
# Returns 16 [56-bit] keys shifted.
def lcs(permuted_key):
    SHIFT_PER_ROUND = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    
    shifted_keys = []  # Used to store shifted keys

    # Split key in half
    left = permuted_key[:28]
    right = permuted_key[28:]

    for round in range(16):  # 16 total rounds
        # Shift left and right sides
        left = left_shift(left, SHIFT_PER_ROUND[round])
        right = left_shift(right, SHIFT_PER_ROUND[round])
        
        # Append to list of keys
        shifted_keys.append(left + right)
    
    return shifted_keys




