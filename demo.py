import matplotlib as plt
from visualization import plot_racetrack_sequences
from utils import *
from decode import *

def example_1():
    print("\n--- Example 1 ---")
    u = [0,0,1,1,0,1,0,1,1]
    l_u_1 = get_longest_run(u)
    sub = u[3:8]
    l_u_2 = get_longest_period_2(u)
    plot_racetrack_sequences([u], ["u"], "Example 1: Basic Sequence")

def example_2():
    print("\n--- Example 2 ---")
    u = [0,0,1,1,0,1,0,1,1]
    u_d4 = delete_bit(u, 4)
    u_multi = u.copy()
    for idx in sorted([4, 7, 9], reverse=True):
        u_multi = delete_bit(u_multi, idx)
    u_burst = delete_burst(u, 3, 4)

    plot_racetrack_sequences(
        [u, u_d4, u_multi, u_burst], 
        ["u", "u(d4)", "u({d4,d7,d9})", "u(d[3,4])"], 
        "Example 2: Deletions"
    )

def example_3():
    print("\n--- Example 3 ---")
    u = [0,0,1,1,0,1,0,1,1]
    t1 = 1
    t2 = 2
    h1 = delete_bit(u, 3)
    h2 = delete_bit(u, 3 + t1)
    h3 = delete_bit(u, 3 + t1 + t2)

    plot_racetrack_sequences(
        [u, h1, h2, h3], 
        ["u", "Head 1", "Head 2", "Head 3"], 
        "Example 3: Multiple Heads"
    )

def example_4():
    print("\n--- Example 4 ---")
    c = [0,0,1,1,0,1,0,1,1]
    c1 = delete_bit(c, 3)
    c2 = delete_bit(c, 6)
    
    decoded = decode_single_deletion(c1, c2)
    print(f"Decoded: {decoded}")
    print(f"Match: {decoded == c}")
    plot_racetrack_sequences(
        [c, c1, c2, decoded], 
        ["Original", "Head 1", "Head 2", "Decoded"], 
        "Example 4: Single Deletion Correction"
    )

def example_5():
    print("\n--- Example 5 ---")
    c = [0,0,1,1,0,1,1,0,1,1]
    c1 = delete_burst(c, 3, 2)
    c2 = delete_burst(c, 6, 2)
    
    decoded = decode_burst_deletion(c1, c2, burst_length=2)
    print(f"Decoded: {decoded}")
    print(f"Match: {decoded == c}")
    plot_racetrack_sequences(
        [c, c1, c2, decoded], 
        ["Original", "Head 1", "Head 2", "Decoded"], 
        "Example 5: Burst Deletion Correction"
    )

def example_6():
    print("\n--- Example 6 ---")
    c = [0,0,1,1,0,1,1,0,1,1,1,0,0,1]
    c1 = delete_bit(delete_bit(c.copy(), 5), 3)
    c2 = delete_bit(delete_bit(c.copy(), 9), 7)
    c3 = delete_bit(delete_bit(c.copy(), 13), 11)
    
    decoded = decode_multiple_deletions_3heads(c1, c2, c3)
    print(f"Decoded: {decoded}")
    print(f"Match: {decoded == c}")

    plot_racetrack_sequences(
        [c, c1, c2, c3, decoded], 
        ["Original", "Head 1", "Head 2", "Head 3", "Decoded"], 
        "Example 6: Multiple Deletions Correction"
    )

def example_7():
    print("\n--- Example 7 ---")
    u = [0,0,1,1,0,1,1]
    u_g4_3 = sticky_insertion(u, 4, 3)
    u_multi = sticky_insertion(sticky_insertion(u, 4, 2), 1, 1)

    plot_racetrack_sequences(
        [u, u_g4_3, u_multi], 
        ["u", "u(g[4,3])", "u(g[1,1],g[4,2])"], 
        "Example 7: Sticky Insertions"
    )

def example_8():
    print("\n--- Example 8 ---")
    c = [1,0,1,1,0,0,0,1,1,0,1,1,1,0,1,1,0,0,1,0]
    c1 = sticky_insertion(delete_bit(c, 5), 2, 1)
    c2 = sticky_insertion(delete_bit(c, 12), 9, 1)
    c3 = sticky_insertion(delete_bit(c, 19), 16, 1)
    j1 = 3
    bit_to_insert = c2[j1-1]
    c_1 = c1[:j1-1] + [bit_to_insert] + c1[j1-1:]
    j2 = find_first_diff(c_1, c2)
    c_double_1 = delete_bit(c_1, j2)
    sub_c_double_1 = c_double_1[:7]
    sub_c2 = c2[:7]
    
    if sub_c_double_1 != sub_c2:
        print("Deduce sticky insertion.")
        c_corrected_1 = delete_bit(c1, j1)
        print(f"Corrected c1 (c(delta5)) = {c_corrected_1}")
        c_delta_12 = delete_bit(c, 12)
        print(f"c(delta12) = {c_delta_12}")
        decoded = decode_single_deletion(c_corrected_1, c_delta_12)
        print(f"Decoded: {decoded}")
        print(f"Match: {decoded == c}")
        plot_racetrack_sequences(
            [c, c1, c2, c3, decoded], 
            ["Original", "Head 1", "Head 2", "Head 3", "Decoded"], 
            "Example 8: Deletion + Sticky Insertion"
        )

def example_9():
    print("\n--- Example 9 ---")
    c = [0,0,1,1,0,1,1,0,1,1,1,0,0,1]
    c1 = [0,0,0,1,1,1,0,1,1,1,0,0,1]
    c2 = [0,0,1,1,0,1,1,0,0,1,0,0,1]
    t = 6
    decoded = decode_substitution_deletion(c1, c2, t)
    
    if decoded:
        print(f"Decoded: {decoded}")
        print(f"Match: {decoded == c}")
        plot_racetrack_sequences(
            [c, c1, c2, decoded], 
            ["Original", "Head 1", "Head 2", "Decoded"], 
            "Example 9: Substitution + Deletion Correction"
        )
    else:
        print("Decoding failed.")

if __name__ == "__main__":
    example_1()
    example_2()
    example_3()
    example_4()
    example_5()
    example_6()
    example_7()
    example_8()
    example_9()