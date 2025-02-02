from Tables import PC1_TABLE, PC2_TABLE
from DES import permutation


# Implements the PC-2 functions. 
# Permutates 56-bit key into 48-bits.
# Returns list of 16 [48-bit] keys, permutated using PC2 table.
def pc2(shifted_keys):
    permuted_keys = []  # Used to store shifted keys

    # Iterate through list of keys and permutate.
    for key in shifted_keys:
        curr_key = ''.join(key[pos - 1] for pos in PC2_TABLE)
        permuted_keys.append(curr_key)

    return permuted_keys


# Performs left shift on a set of bits. 
# Shift varies (1, 2) depending on the round.
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


# Function to create subkeys from the original key.
# Returns list of keys.
def create_keys(key):
    # Permutate using PC-1 table
    kplus = permutation(PC1_TABLE, key)

    # Generate 16 keys using left circular shift
    shifted_keys = lcs(kplus)

    # 56 -> 48 bits using PC-2
    pc2_keys = pc2(shifted_keys)

    return pc2_keys

