import time
import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from hvlcs import parse_input, hvlcs

data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
test_files = sorted(f for f in os.listdir(data_dir) if f.endswith('.in'))

labels = []
runtimes = []
sizes = []

for fname in test_files:
    path = os.path.join(data_dir, fname)
    values, A, B = parse_input(path)

    start = time.perf_counter()
    max_val, subseq = hvlcs(A, B, values)
    elapsed = time.perf_counter() - start

    size = len(A) * len(B)
    labels.append(fname.replace('.in', ''))
    runtimes.append(elapsed * 1000)  # ms
    sizes.append(size)

    print(f"{fname}: |A|x|B|={size}  time={elapsed*1000:.3f}ms  val={max_val}  seq_len={len(subseq)}")

#plot
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

#bar chart: runtime per test file
axes[0].bar(labels, runtimes, color='steelblue', edgecolor='black')
axes[0].set_xlabel('Test File')
axes[0].set_ylabel('Runtime (ms)')
axes[0].set_title('HVLCS Runtime per Test File')
axes[0].tick_params(axis='x', rotation=45)
for idx, v in enumerate(runtimes):
    axes[0].text(idx, v + 0.001, f'{v:.2f}', ha='center', va='bottom', fontsize=8)

#scatter: runtime vs. m*n
axes[1].scatter(sizes, runtimes, color='tomato', edgecolors='black', s=80, zorder=3)
for i, lbl in enumerate(labels):
    axes[1].annotate(lbl, (sizes[i], runtimes[i]), textcoords='offset points',
                     xytext=(5, 3), fontsize=7)
axes[1].set_xlabel('|A| × |B| (DP table cells)')
axes[1].set_ylabel('Runtime (ms)')
axes[1].set_title('Runtime vs. DP Table Size (O(mn) behaviour)')
axes[1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
out_path = os.path.join(os.path.dirname(__file__), '..', 'runtime_plot.png')
plt.savefig(out_path, dpi=150)
print(f"\nPlot saved to {out_path}")
