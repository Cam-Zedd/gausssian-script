import matplotlib.pyplot as plt
import numpy as np
import time
import re
import math

# ===============================
# PARAMETRES UTILISATEUR
# ===============================
LOWEST_OCCUPIED = "HOMO-2"
HIGHEST_VIRTUAL = "LUMO+1"


# ===============================
# Parsing des fichiers txt
# ===============================
def parse_orbitals(filename):

    energies = {}
    gap = None

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:

            if any(key in line for key in ["HOMO","LUMO"]):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    label = parts[0]
                    try:
                        energies[label] = float(parts[2])
                    except:
                        pass

            if "Gap HOMO-LUMO" in line:
                gap = float(re.search(r"=\s*([0-9.]+)", line).group(1))

    return energies, gap


# ===============================
# Label -> index
# ===============================
def orbital_index(label):

    if label == "HOMO":
        return 0
    if label.startswith("HOMO-"):
        return -int(label.split("-")[1])

    if label == "LUMO":
        return 0
    if label.startswith("LUMO+"):
        return int(label.split("+")[1])

    return None


# ===============================
# Fichiers
# ===============================
files = ["5a.txt","5b.txt","5c.txt","5d.txt"]
complexes = [r'5a', r'5b', r'5c', r'5d']

all_data = []
all_gaps = []

for f in files:
    energies, gap = parse_orbitals(f)
    all_data.append(energies)
    all_gaps.append(gap)


# ===============================
# Détection automatique OMs
# ===============================
all_labels = set()
for d in all_data:
    all_labels.update(d.keys())

occupied_labels = sorted(
    [l for l in all_labels if l.startswith("HOMO")],
    key=orbital_index
)

virtual_labels = sorted(
    [l for l in all_labels if l.startswith("LUMO")],
    key=orbital_index
)

occ_min_index = orbital_index(LOWEST_OCCUPIED)
virt_max_index = orbital_index(HIGHEST_VIRTUAL)

occupied_labels = [
    l for l in occupied_labels
    if orbital_index(l) >= occ_min_index
]

virtual_labels = [
    l for l in virtual_labels
    if orbital_index(l) <= virt_max_index
]


occupied_energies = [
    [d.get(label, None) for d in all_data]
    for label in occupied_labels
]

virtual_energies = [
    [d.get(label, None) for d in all_data]
    for label in virtual_labels
]


# ===============================
# Paramètres matplotlib (TA VERSION)
# ===============================
start_time = time.time()

SMALL_SIZE = 26
BIGGER_SIZE = 32

plt.rcParams.update({
    'font.size': SMALL_SIZE,
    'axes.titlesize': BIGGER_SIZE,
    'axes.edgecolor': 'black',
    'axes.labelsize': SMALL_SIZE,
    'axes.linewidth': 2,
    'xtick.labelsize': SMALL_SIZE,
    'xtick.major.size': 10,
    'xtick.major.width': 2,
    'lines.markersize': 24,
    'patch.linewidth': 3.0,
    'ytick.labelsize': SMALL_SIZE,
    'ytick.major.size': 10,
    'ytick.major.width': 2,
    'ytick.minor.size': 6,
    'ytick.minor.width': 1,
    'axes.xmargin': 0
})


# ===============================
# Plot (IDENTIQUE AU TIEN)
# ===============================
fig, ax = plt.subplots(figsize=(15,10))
x = np.arange(1, len(files)+1)



for label, energies in zip(occupied_labels, occupied_energies):
    ax.scatter(x, energies, label=f"{label}",
               marker="_", lw=4)

for label, energies in zip(virtual_labels, virtual_energies):
    ax.scatter(x, energies, label=f"{label}",
               marker="_", lw=4)


# ===============================
# Limites Y auto
# ===============================
all_occ = [e for sub in occupied_energies for e in sub if e is not None]
all_virt = [e for sub in virtual_energies for e in sub if e is not None]

ymin = math.floor(min(all_occ))
ymax = math.ceil(max(all_virt))

ax.set_ylim(ymin, ymax)


# ===============================
# Gap HOMO-LUMO
# ===============================
# HOMO = dernière orbitale occupée affichée
# LUMO = première orbitale virtuelle affichée

HOMO_values = occupied_energies[-1]
LUMO_values = virtual_energies[0]

for i, (h, l, g) in enumerate(zip(HOMO_values, LUMO_values, all_gaps)):

    if h is None or l is None:
        continue

    ax.text(
        i + 1,
        (h + l) / 2,
        f"{g:.2f} eV",
        ha='center',
        va='center',
        rotation=90,
        fontsize=SMALL_SIZE * 0.9
    )


# ===============================
# Electrons (VERSION PROPRE)
# ===============================
arrow_dx = 0.035
arrow_len = 0.28

for i in range(len(x)):
    for occ_list in occupied_energies:

        e = occ_list[i]
        if e is None:
            continue

        # spin up
        ax.annotate(
            "",
            xy=(i+1-arrow_dx, e-arrow_len/4),
            xytext=(i+1-arrow_dx, e+arrow_len/4),
            arrowprops=dict(
                arrowstyle="->",
                lw=1.2,
                shrinkA=0,
                shrinkB=0,
                mutation_scale=8
            )
        )

        # spin down
        ax.annotate(
            "",
            xy=(i+1+arrow_dx, e+arrow_len/4),
            xytext=(i+1+arrow_dx, e-arrow_len/4),
            arrowprops=dict(
                arrowstyle="->",
                lw=1.2,
                shrinkA=0,
                shrinkB=0,
                mutation_scale=8
            )
        )


# ===============================
# Axes
# ===============================
ax.set_ylabel("Energy (eV)")
ax.set_xticks(x)
ax.set_xticklabels(complexes, rotation=45)
ax.set_xlim(0, len(files)+1)

ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 1.10),
    ncol=len(occupied_labels)+len(virtual_labels),
    frameon=False,
    handletextpad=0.3,   # espace trait ↔ texte
    columnspacing=0.8,   # espace entre colonnes
    handlelength=1.2,    # longueur du trait dans la légende
    borderaxespad=0.2
)


plt.savefig("diagramme.png", dpi=1200)
plt.savefig("diagramme.eps")

print(f"Execution time: {time.time() - start_time:.2f} s")
plt.show()
