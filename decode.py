from utils import delete_bit

def find_first_diff(seq1, seq2):
    limit = min(len(seq1), len(seq2))
    for i in range(limit):
        if seq1[i] != seq2[i]:
            return i + 1
    if len(seq1) != len(seq2):
        return limit + 1
    return -1

def decode_single_deletion(c1, c2):
    j1 = find_first_diff(c1, c2)
    if j1 == -1:
        return c1
    return c2[:j1] + c1[j1-1:]

def decode_burst_deletion(c1, c2, burst_length=2):
    j1 = find_first_diff(c1, c2)
    if j1 == -1:
        return c1
    if burst_length == 2:
        return c2[:j1+1] + c1[j1-1:]
    else:
        return c2[:j1+burst_length-1] + c1[j1-1:]

def decode_multiple_deletions_3heads(c1, c2, c3):
    j1 = find_first_diff(c1, c2)
    c_delta_12 = c2[:j1] + c1[j1-1:]

    j2 = find_first_diff(c2, c3)
    c_delta_23 = c3[:j2] + c2[j2-1:]

    j3 = find_first_diff(c_delta_12, c_delta_23)
    decoded = c_delta_23[:j3] + c_delta_12[j3-1:]
    
    return decoded

def decode_deletion_sticky_insertion(c, c1, c2, c3):
    j1 = 3 
    bit_to_insert = c2[j1-1]
    c_1 = c1[:j1-1] + [bit_to_insert] + c1[j1-1:]
    
    j2 = find_first_diff(c_1, c2)
    c_double_1 = delete_bit(c_1, j2)
    
    sub_c_double_1 = c_double_1[:7]
    sub_c2 = c2[:7]
    
    if sub_c_double_1 != sub_c2:
        c_corrected_1 = delete_bit(c1, j1)
        return c_corrected_1
        
    return c1

def decode_substitution_deletion(c1, c2, t):
    j1 = find_first_diff(c1, c2)
    
    c_1 = c1.copy()
    if 0 <= j1-1 < len(c_1):
        c_1[j1-1] = 1 - c_1[j1-1]
        
    c_2 = c2.copy()
    idx_2 = j1 + t - 1
    if 0 <= idx_2 < len(c_2):
        c_2[idx_2] = 1 - c_2[idx_2]
        
    j2 = find_first_diff(c_1, c_2)
    
    j3 = -1
    min_len = min(len(c_1), len(c_2))
    for i in range(min_len - 1, -1, -1):
        if c_1[i] != c_2[i]:
            j3 = i + 1
            break
            
    c_double_1 = c_2[:j2] + c_1[j2-1:]
    c_double_2 = c_2[:j3] + c_1[j3-1:]
    
    if c_double_1 == c_double_2:
        return c_double_1
    else:
        return None
