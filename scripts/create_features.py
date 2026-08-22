import os
import rasterio
import numpy as np
import pandas as pd

# Make sure output folder exists
os.makedirs("data/processed", exist_ok=True)

# Read Sentinel-2 bands
with rasterio.open("data/raw/field_image.tif") as src:
    red = src.read(4).astype(np.float32)      # B4
    nir = src.read(8).astype(np.float32)      # B8
    rededge = src.read(5).astype(np.float32)  # B5

# Calculate indices
ndvi = (nir - red) / (nir + red + 1e-10)
ndre = (nir - rededge) / (nir + rededge + 1e-10)

# Convert every pixel into one row
df = pd.DataFrame({
    "NDVI": ndvi.flatten(),
    "NDRE": ndre.flatten()
})

# Remove invalid values
df = df.replace([np.inf, -np.inf], np.nan).dropna()

# Prototype labels
# 0 = Healthy
# 1 = Potentially Infested
df["Label"] = (df["NDVI"] < 0.4).astype(int)

# Save CSV
output = "data/processed/features.csv"
df.to_csv(output, index=False)

print(f"Features saved to: {output}")
print(f"Total samples: {len(df)}")
print(df.head())