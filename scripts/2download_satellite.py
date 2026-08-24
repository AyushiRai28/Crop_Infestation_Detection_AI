import ee

# -----------------------------
# CONNECT TO EARTH ENGINE
# -----------------------------
PROJECT_ID = "crop-infestation-ai"   # Replace if different
ee.Initialize(project=PROJECT_ID)

# -----------------------------
# REGION OF INTEREST (ROI)
# -----------------------------
# Small agricultural area near Bhopal
roi = ee.Geometry.Rectangle([77.05, 23.15, 77.15, 23.25])

# -----------------------------
# LOAD SENTINEL-2 DATA
# -----------------------------
collection = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(roi)
    .filterDate("2025-01-01", "2025-03-31")
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
)

# -----------------------------
# CHECK AVAILABLE IMAGES
# -----------------------------
count = collection.size().getInfo()
print(f"Images found: {count}")

if count == 0:
    print("No suitable satellite image found.")
    exit()

# -----------------------------
# SELECT BEST IMAGE
# -----------------------------
image = collection.sort("CLOUDY_PIXEL_PERCENTAGE").first()

print("\nSatellite image selected successfully!")

print("\nImage ID:")
print(image.get("PRODUCT_ID").getInfo())

print("\nCloud Percentage:")
print(image.get("CLOUDY_PIXEL_PERCENTAGE").getInfo())

# -----------------------------
# SELECT RGB BANDS
# -----------------------------
rgb_image = image.select(["B4", "B3", "B2"])

# -----------------------------
# EXPORT TO GOOGLE DRIVE
# -----------------------------
task = ee.batch.Export.image.toDrive(
    image=rgb_image,
    description="Bhopal_Field_Image",
    folder="Crop_Infestation_AI",
    fileNamePrefix="field_image",
    region=roi,
    scale=10,
    maxPixels=1e13,
    fileFormat="GeoTIFF"
)

task.start()

print("\nExport started successfully!")
print("Check Google Drive → Crop_Infestation_AI folder.")