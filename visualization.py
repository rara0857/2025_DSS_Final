import matplotlib.pyplot as plt
import numpy as np

def plot_racetrack_sequences(sequences, labels, title="Racetrack Memory Decoding Step"):
    max_len = max(len(s) for s in sequences)
    padded_seqs = []
    
    for s in sequences:
        padded = s + [-1] * (max_len - len(s))
        padded_seqs.append(padded)
        
    data = np.array(padded_seqs)
    
    fig, ax = plt.subplots(figsize=(12, max(len(sequences) * 1.2, 3)))
    
    masked_data = np.ma.masked_where(data == -1, data)
    
    cax = ax.imshow(masked_data, cmap='Blues', aspect='equal', vmin=0, vmax=1)
    
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels, fontsize=12, fontweight='bold')
    
    ax.set_xticks(np.arange(max_len))
    ax.set_xticklabels(np.arange(1, max_len + 1))
    ax.set_xlabel("Bit Position", fontsize=10)
    
    for i in range(len(sequences)):
        for j in range(len(sequences[i])):
            val = sequences[i][j]
            text_color = 'white' if val == 1 else 'black'
            ax.text(j, i, str(val), ha='center', va='center', color=text_color, fontsize=12, fontweight='bold')

    ax.set_xticks(np.arange(-.5, max_len, 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(sequences), 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=1)
    ax.tick_params(which='minor', bottom=False, left=False)
    ax.tick_params(which='major', bottom=True, left=False)
    
    plt.title(title, fontsize=14, pad=20)
    plt.tight_layout()
    plt.show()