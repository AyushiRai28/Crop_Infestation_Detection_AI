import ee
import geemap

# Initialize Earth Engine
ee.Initialize(project="crop-infestation-ai")

# Same area used earlier
roi = ee.Geometry.Rectangle([77.07, 23.17, 77.12, 23.22])

# Load Sentinel-2
collection = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(roi)
    .filterDate("2024-01-01", "2024-12-31")
    .sort("CLOUDY_PIXEL_PERCENTAGE")
)

image = collection.first()

print("Exporting least cloudy image...")

cloud = image.get("CLOUDY_PIXEL_PERCENTAGE").getInfo()
print(f"Selected image cloud cover: {cloud}%")
print("Exporting least cloudy image...")

# Export as a single GeoTIFF
geemap.ee_export_image(
    image,                              # first positional argument
    filename="data/raw/field_image.tif",
    scale=10,
    region=roi,
    file_per_band=False
)

print("Export completed!")
print("Saved: data/raw/field_image.tif")