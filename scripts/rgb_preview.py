import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

# Open GeoTIFF
with rasterio.open("data/raw/field_image.tif") as src:
    red = src.read(4).astype(np.float32)    # Band 4
    green = src.read(3).astype(np.float32)  # Band 3
    blue = src.read(2).astype(np.float32)   # Band 2

# Stack into RGB
rgb = np.dstack((red, green, blue))

# Stretch contrast for better visualization
rgb = rgb / np.percentile(rgb, 98)
rgb = np.clip(rgb, 0, 1)

# Save preview
plt.figure(figsize=(8,8))
plt.imshow(rgb)
plt.axis("off")
plt.tight_layout()

output_path = "data/raw/rgb_preview.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0)
plt.show()

print(f"RGB preview saved at: {output_path}")