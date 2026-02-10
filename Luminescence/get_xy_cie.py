import numpy as np
import pandas as pd
import glob
import os

# --- Fichier CIE ---
cie_file = "CIE_xyz_1931_2deg.csv"
cie = pd.read_csv(cie_file, header=None, names=['nm', 'x_bar', 'y_bar', 'z_bar'])

# --- Dossier contenant les spectres ---
spectre_folder = "./spectra/"  # à adapter
spectre_files = glob.glob(os.path.join(spectre_folder, "*.csv"))

# --- Liste pour stocker les résultats ---
results = []

for f in spectre_files:
    data = pd.read_csv(f)
    wavelengths = data['nm'].values
    intensities = data['I'].values

    # Interpolation des fonctions CIE
    x_bar = np.interp(wavelengths, cie['nm'], cie['x_bar'])
    y_bar = np.interp(wavelengths, cie['nm'], cie['y_bar'])
    z_bar = np.interp(wavelengths, cie['nm'], cie['z_bar'])

    # Calcul intégrales X,Y,Z
    X = np.trapz(intensities * x_bar, wavelengths)
    Y = np.trapz(intensities * y_bar, wavelengths)
    Z = np.trapz(intensities * z_bar, wavelengths)

    # Coordonnées xy
    total = X + Y + Z
    xy_x = X / total
    xy_y = Y / total

    # Stocke le résultat avec le nom du fichier
    results.append([os.path.basename(f), xy_x, xy_y])

# --- Écriture des résultats dans un fichier TXT ---
output_file = "cie_xy_results.txt"
with open(output_file, 'w') as out:
    out.write("filename\tx\ty\n")
    for r in results:
        out.write(f"{r[0]}\t{r[1]:.4f}\t{r[2]:.4f}\n")

print(f"Résultats enregistrés dans {output_file}")
