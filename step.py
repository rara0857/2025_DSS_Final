import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Cambria Math', 'Cambria', 'Times New Roman', 'DejaVu Serif', 'serif']
plt.rcParams['axes.unicode_minus'] = False 
plt.rcParams['mathtext.fontset'] = 'stix' 

def delete_bit(u, index_1based):
    if index_1based < 1 or index_1based > len(u): return u
    return u[:index_1based-1] + u[index_1based:]

def delete_burst(u, start_index_1based, length):
    if start_index_1based < 1: return u
    start = start_index_1based - 1
    return u[:start] + u[start + length:]

def sticky_insertion(u, index_1based, length=1):
    if index_1based < 1 or index_1based > len(u): return u
    idx = index_1based - 1
    bit = u[idx]
    return u[:idx+1] + [bit]*length + u[idx+1:]

def find_first_diff(seq1, seq2):
    limit = min(len(seq1), len(seq2))
    for i in range(limit):
        if seq1[i] != seq2[i]: return i + 1
    if len(seq1) != len(seq2): return limit + 1
    return -1

def plot_with_highlights(sequences, labels, highlights, title, filename):
    valid_seqs = [s for s in sequences if s is not None]
    if not valid_seqs: return
    max_len = max(len(s) for s in valid_seqs)
    n_rows = len(sequences)
    
    fig, ax = plt.subplots(figsize=(14, n_rows * 0.8 + 1.5))
    
    for r, seq in enumerate(sequences):
        y = n_rows - 1 - r
        label_text = labels[r] if labels[r] is not None else ""
        ax.text(-0.2, y + 0.5, label_text, va='center', ha='right', fontsize=15, fontweight='bold', color='#333333')
        
        if seq is None: continue
        for c in range(max_len):
            if c < len(seq):
                val = seq[c]
                facecolor = '#003366' if val == 1 else '#ffffff'
                textcolor = 'white' if val == 1 else 'black'
                edgecolor = 'gray'
                rect = patches.Rectangle((c, y), 1, 1, linewidth=1, edgecolor=edgecolor, facecolor=facecolor)
                ax.add_patch(rect)
                ax.text(c + 0.5, y + 0.5, str(val), va='center', ha='center', color=textcolor, fontsize=12, fontweight='bold')
    
    for h in highlights:
        r, c = h['row'], h['col']
        if r >= len(sequences) or sequences[r] is None: continue
        y = n_rows - 1 - r
        rect = patches.Rectangle((c, y), 1, 1, linewidth=h.get('lw', 3), edgecolor=h.get('color', 'red'), facecolor='none', zorder=10)
        ax.add_patch(rect)

    ax.set_xlim(-0.5, max_len)
    ax.set_ylim(0, n_rows)
    ax.set_aspect('equal')
    ax.axis('off')
    
    for c in range(max_len):
        ax.text(c + 0.5, n_rows + 0.1, str(c + 1), ha='center', fontsize=9, color='black')
    
    plt.subplots_adjust(left=0.25)
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

def visualize_ex1_step():
    plot_with_highlights([[0,0,1,1,0,1,0,1,1]], [r"$\mathbf{u}:$"], [], "", "step_img/ex1_step.png")

def visualize_ex2_step():
    u = [0,0,1,1,0,1,0,1,1]
    u_d4 = delete_bit(u, 4)
    u_multi = u.copy()
    for idx in sorted([4, 7, 9], reverse=True):
        u_multi = delete_bit(u_multi, idx)
    u_burst = delete_burst(u, 3, 4) 

    seqs = [u, u_d4, u_multi, u_burst]
    labels = [r"$\mathbf{u}:$", r"$\mathbf{u}(\delta_4):$", r"$\mathbf{u}(\delta_{\{4,7,9\}}):$", r"$\mathbf{u}(\delta_{[3,4]}):$"]
    
    hlights = [
        {'row': 1, 'col': 3},
        {'row': 2, 'col': 3}, {'row': 2, 'col': 6}, {'row': 2, 'col': 8},
        {'row': 3, 'col': 2}, {'row': 3, 'col': 3}, {'row': 3, 'col': 4}, {'row': 3, 'col': 5}
    ]
    plot_with_highlights(seqs, labels, hlights, "", "step_img/ex2_step.png")

def visualize_ex3_step():
    u = [0,0,1,1,0,1,0,1,1]
    h1, h2, h3 = delete_bit(u, 3), delete_bit(u, 5), delete_bit(u, 7)
    labels = [r"$\mathbf{u}:$", r"$\text{Head}_1:$", r"$\text{Head}_2:$", r"$\text{Head}_3:$"]
    hlights = [{'row': 1, 'col': 2}, {'row': 2, 'col': 4}, {'row': 3, 'col': 6}]
    plot_with_highlights([u, h1, h2, h3], labels, hlights, "", "step_img/ex3_step.png")

def visualize_ex4_step():
    c = [0,0,1,1,0,1,0,1,1]
    c1, c2 = delete_bit(c, 3), delete_bit(c, 6)
    j1 = find_first_diff(c1, c2)
    decoded = c2[:j1] + c1[j1-1:]
    labels = [r"$\text{Origin}:$", r"$\mathbf{c}_1:$", r"$\mathbf{c}_2:$", None, r"$\text{Decode Result}:$"]
    hlights = [{'row': 1, 'col': j1-1}, {'row': 2, 'col': j1-1}, {'row': 4, 'col': j1-1, 'color': 'green'}]
    plot_with_highlights([c, c1, c2, None, decoded], labels, hlights, "", "step_img/ex4_step.png")

def visualize_ex5_step():
    c = [0,0,1,1,0,1,1,0,1,1]
    c1, c2 = delete_burst(c, 3, 2), delete_burst(c, 6, 2)
    j1 = find_first_diff(c1, c2)
    decoded = c2[:j1+1] + c1[j1-1:]
    labels = [r"$\text{Origin}:$", r"$\mathbf{c}_1:$", r"$\mathbf{c}_2:$", None, r"$\text{Decode Result}:$"]
    hlights = [{'row': 1, 'col': 2}, {'row': 2, 'col': 2}, {'row': 4, 'col': 2, 'color': 'green'}, {'row': 4, 'col': 3, 'color': 'green'}]
    plot_with_highlights([c, c1, c2, None, decoded], labels, hlights, "", "step_img/ex5_step.png")

def visualize_ex6_step():
    c = [0,0,1,1,0,1,1,0,1,1,1,0,0,1]
    c1 = delete_bit(delete_bit(list(c), 5), 3)
    c2 = delete_bit(delete_bit(list(c), 9), 7)
    c3 = delete_bit(delete_bit(list(c), 13), 11)
    j1, j2 = find_first_diff(c1, c2), find_first_diff(c2, c3)
    c_delta_12, c_delta_23 = c2[:j1] + c1[j1-1:], c3[:j2] + c2[j2-1:]
    j3 = find_first_diff(c_delta_12, c_delta_23)
    decoded = c_delta_23[:j3] + c_delta_12[j3-1:]
    labels = [r"$\text{Origin}:$", r"$\mathbf{c}_1:$", r"$\mathbf{c}_2:$", r"$\mathbf{c}_3:$", None, r"$\text{Merge } \mathbf{c}_1, \mathbf{c}_2:$", r"$\text{Merge } \mathbf{c}_2, \mathbf{c}_3:$", None, r"$\text{Decode Result}:$"]
    hlights = [{'row': 5, 'col': j1-1, 'color': 'green'}, {'row': 6, 'col': j2-1, 'color': 'green'}, {'row': 8, 'col': j3-1, 'color': 'green'}]
    plot_with_highlights([c, c1, c2, c3, None, c_delta_12, c_delta_23, None, decoded], labels, hlights, "", "step_img/ex6_step.png")

def visualize_ex7_step():
    u = [0,0,1,1,0,1,1]
    u_g4_3 = sticky_insertion(u, 4, 3)
    u_temp = sticky_insertion(u, 4, 2)
    u_multi = sticky_insertion(u_temp, 1, 1)
    
    labels = [r"$\mathbf{u}:$", r"$\mathbf{u}(\gamma_{[4,3]}):$", r"$\mathbf{u}(\gamma_{\{ [1,1], [4,2] \}}):$"]
    
    hlights = [
        {'row': 1, 'col': 4, 'color': 'green'}, {'row': 1, 'col': 5, 'color': 'green'}, {'row': 1, 'col': 6, 'color': 'green'},
        {'row': 2, 'col': 1, 'color': 'green'}, 
        {'row': 2, 'col': 5, 'color': 'green'}, {'row': 2, 'col': 6, 'color': 'green'}
    ]
    plot_with_highlights([u, u_g4_3, u_multi], labels, hlights, "", "step_img/ex7_step.png")

def visualize_ex8_step():
    c = [1,0,1,1,0,0,0,1,1,0,1,1,1,0,1,1,0,0,1,0]
    c1, c2, c3 = sticky_insertion(delete_bit(c, 5), 2, 1), sticky_insertion(delete_bit(c, 12), 9, 1), sticky_insertion(delete_bit(c, 19), 16, 1)
    j1 = 3; bit_to_insert = c2[j1-1]; c_test = c1[:j1-1] + [bit_to_insert] + c1[j1-1:]; j2 = find_first_diff(c_test, c2)
    c_double_1, c_corrected_1, c_delta_12 = delete_bit(c_test, j2), delete_bit(c1, j1), delete_bit(c, 12)
    j_step = find_first_diff(c_corrected_1, c_delta_12); decoded = c_delta_12[:j_step] + c_corrected_1[j_step-1:]
    seqs = [c, c1, c2, c3, None, c_test, None, c_corrected_1, c_delta_12, decoded]
    labels = [r"$\text{Origin}:$", r"$\mathbf{c}_1:$", r"$\mathbf{c}_2:$", r"$\mathbf{c}_3:$", None, r"$\text{Insert } 1 \text{ at index } 3:$", None, r"$\text{Delete bit at index } 3:$", r"$\text{Head Alignment}:$", r"$\text{Decode Result}:$"]
    hlights = [{'row': 1, 'col': 2, 'color': 'red'}, {'row': 5, 'col': 2, 'color': 'orange', 'lw': 4}, {'row': 7, 'col': 2, 'color': 'green'}, {'row': 8, 'col': 4, 'color': 'green'}, {'row': 9, 'col': 4, 'color': 'green'}]
    plot_with_highlights(seqs, labels, hlights, "", "step_img/ex8_step.png")

def visualize_ex9_step():
    c = [0,0,1,1,0,1,1,0,1,1,1,0,0,1]
    c1, c2 = [0,0,0,1,1,1,0,1,1,1,0,0,1], [0,0,1,1,0,1,1,0,0,1,0,0,1]
    t, j1 = 6, find_first_diff(c1, c2)
    c_1 = list(c1); c_1[j1-1] = 1 - c_1[j1-1]; c_2 = list(c2); idx_2 = j1 + t - 1; c_2[idx_2] = 1 - c_2[idx_2]
    j2 = find_first_diff(c_1, c_2); decoded = c_2[:j2] + c_1[j2-1:]
    labels = [r"$\text{Origin}:$", r"$\mathbf{c}_1:$", r"$\mathbf{c}_2:$", None, r"$\text{Flip } \mathbf{c}_1 \text{ at } j_1:$", r"$\text{Flip } \mathbf{c}_2 \text{ at } j_1+t:$", None, r"$\text{Decode Result}:$"]
    hlights = [{'row': 1, 'col': 2, 'color': 'red'}, {'row': 2, 'col': 2, 'color': 'red'}, {'row': 4, 'col': 2, 'color': 'green'}, {'row': 5, 'col': 8, 'color': 'green'}, {'row': 7, 'col': 2, 'color': 'green'}]
    plot_with_highlights([c, c1, c2, None, c_1, c_2, None, decoded], labels, hlights, "", "step_img/ex9_step.png")

if __name__ == "__main__":
    funcs = [visualize_ex1_step, visualize_ex2_step, visualize_ex3_step, visualize_ex4_step, 
             visualize_ex5_step, visualize_ex6_step, visualize_ex7_step, visualize_ex8_step, visualize_ex9_step]
    for f in funcs: f()