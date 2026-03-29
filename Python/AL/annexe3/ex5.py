import numpy as np
from skimage import data
from matplotlib import pyplot as plt
camera = data.camera()

# Création d'une matrice carrée de 512*512
M = np.eye(512)

# Transformation en matrice représentant la moyenne glissante
for i in range (512):
    for j in range (512):
        if abs(i - j) <= 1:
            M[i, j] = 1/3
        if i == 0 and j == 0:
            M[i][j] = 2/3
        if i == 511 and j == 511:
            M[i][j] = 2/3

# Application du flou horizontal (10 fois pour un résultat plus visuel)
camera_modified_horizontal = camera@M      
for i in range (10):
    camera_modified_horizontal = camera_modified_horizontal@M

# Application du flou vertical (10 fois pour un résultat plus visuel)
camera_modified_vertical = M@camera
for i in range (10):
    camera_modified_vertical = M@camera_modified_vertical

# Application du flou horizontal + vertical (10 fois pour un résultat plus visuel)
camera_modified = M@camera@M

Minverted = np.linalg.inv(M)

camera_modified_defloutage = Minverted@camera_modified@Minverted

# Affichage
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, figsize=(18, 6))
ax1.imshow(camera, cmap='gray')
ax1.set_title("Originale")
ax2.imshow(camera_modified, cmap='gray')
ax2.set_title("Modifiée (Flou horizontal + vertical)")
ax3.imshow(camera_modified_horizontal, cmap='gray')
ax3.set_title("Modifiée (Flou horizontal)")
ax4.imshow(camera_modified_vertical, cmap='gray')
ax4.set_title("Modifiée (Flou vertical)")
ax5.imshow(camera_modified_defloutage, cmap='gray')
ax5.set_title("Modifiée (défloutage)")

plt.show()