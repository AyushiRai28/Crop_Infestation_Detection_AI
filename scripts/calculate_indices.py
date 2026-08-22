import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Create output folder
os.makedirs("data/processed", exist_ok=True)

with rasterio.open("data/raw/field_image.tif") as src:
    red = src.read(4).astype(np.float32)      # B4
    nir = src.read(8).astype(np.float32)      # B8
    rededge = src.read(5).astype(np.float32)  # B5

# NDVI
ndvi = (nir - red) / (nir + red + 1e-10)

# NDRE
ndre = (nir - rededge) / (nir + rededge + 1e-10)

# Save NDVI
plt.figure(figsize=(8,8))
plt.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
plt.colorbar(label="NDVI")
plt.axis("off")
plt.savefig("data/processed/ndvi.png", dpi=300, bbox_inches="tight")

# Save NDRE
plt.figure(figsize=(8,8))
plt.imshow(ndre, cmap="RdYlGn", vmin=-1, vmax=1)
plt.colorbar(label="NDRE")
plt.axis("off")
plt.savefig("data/processed/ndre.png", dpi=300, bbox_inches="tight")

print("NDVI and NDRE images saved.")