import rasterio
import os
folder=os.path.dirname(os.path.abspath(__file__))
band_files=[
    "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B2.tif",
    "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B3.tif",
    "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B4.tif",
    "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B5.tif"
]
print("Total bands available:",len(band_files))
for file in band_files:
    file_path=os.path.join(folder,file)
    with rasterio.open(file_path) as src:
        print("File:",file)
        print("Dimensions:")
        print("Height:",src.height)
        print("Width:",src.width)
        print("Number of bands in this file:",src.count)
        print("Coordinate system of this file:",src.crs)
        print("resolution of this file:",src.res)
        print("Datatype:",src.dtypes[0])

# 2.
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os
folder = os.path.dirname(os.path.abspath(__file__))
band_files = {
    "Band 2 - Blue": "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B2.tif",
    "Band 3 - Green": "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B3.tif",
    "Band 4 - Red": "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B4.tif",
    "Band 5 - NIR": "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B5.tif"
}
band_data = {}
for band_name, file_name in band_files.items():

    file_path = os.path.join(folder, file_name)

    with rasterio.open(file_path) as src:

        
        data = src.read(1)

        
        data = data.astype(float)

        
        if src.nodata is not None:
            data[data == src.nodata] = np.nan

        
        minimum = np.nanmin(data)
        maximum = np.nanmax(data)
        mean = np.nanmean(data)

        print("\n", band_name)
        print("Minimum :", minimum)
        print("Maximum :", maximum)
        print("Mean    :", mean)

        
        band_data[band_name] = data



plt.figure(figsize=(8, 5))

data = band_data["Band 2 - Blue"]

plt.hist(data[~np.isnan(data)].flatten(), bins=50)

plt.title("Histogram of Landsat 9 Band 2 - Blue")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.grid(True)

plt.show()


plt.figure(figsize=(8, 5))

data = band_data["Band 3 - Green"]

plt.hist(data[~np.isnan(data)].flatten(), bins=50)

plt.title("Histogram of Landsat 9 Band 3 - Green")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.grid(True)

plt.show()
plt.figure(figsize=(8, 5))

data = band_data["Band 4 - Red"]

plt.hist(data[~np.isnan(data)].flatten(), bins=50)

plt.title("Histogram of Landsat 9 Band 4 - Red")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.grid(True)

plt.show()

#3.
import rasterio
import os

folder = os.path.dirname(os.path.abspath(__file__))
band_files = [
    "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B2.tif",
    "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B3.tif",
    "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B4.tif",
    "LC09_L2SP_148047_20230208_20230310_02_T1_SR_B5.tif"
]


output_file = os.path.join(folder, "Landsat9_Band_Stack.tif")
with rasterio.open(os.path.join(folder, band_files[0])) as src:

   
    profile = src.profile


profile.update(count=len(band_files))
with rasterio.open(output_file, "w", **profile) as dst:

    
    for i, file_name in enumerate(band_files, start=1):

        file_path = os.path.join(folder, file_name)

        with rasterio.open(file_path) as src:

            
            data = src.read(1)

        
            dst.write(data, i)

print("Band stacking completed successfully!")
print("Output file:", output_file)
print("Total bands stacked:", len(band_files))

#4.
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os
folder = os.path.dirname(os.path.abspath(__file__))
stacked_file = os.path.join(folder, "Landsat9_Band_Stack.tif")
with rasterio.open(stacked_file) as src:
    blue = src.read(1)    
    green = src.read(2)   
    red = src.read(3)     
    nir = src.read(4)     


def stretch(image):
    lower = np.percentile(image, 2)
    upper = np.percentile(image, 98)

    image = (image - lower) / (upper - lower)

    image = np.clip(image, 0, 1)

    return image


blue_stretched = stretch(blue)
green_stretched = stretch(green)
red_stretched = stretch(red)
nir_stretched = stretch(nir)

true_color = np.dstack((
    red_stretched,
    green_stretched,
    blue_stretched
))


plt.figure(figsize=(10, 8))

plt.imshow(true_color)

plt.title("Landsat 9 True Color Composite (RGB = 4, 3, 2)")

plt.axis("off")

plt.show()


false_color = np.dstack((
    nir_stretched,
    red_stretched,
    green_stretched
))


plt.figure(figsize=(10, 8))

plt.imshow(false_color)

plt.title("Landsat 9 False Color Composite (RGB = 5, 4, 3)")

plt.axis("off")

plt.show()

#5.
import rasterio
from rasterio.windows import Window
import os
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder, "Landsat9_Band_Stack.tif")
output_file = os.path.join(folder, "Landsat9_AOI.tif")
with rasterio.open(input_file) as src:

    print("Original image dimensions:")
    print("Width :", src.width)
    print("Height:", src.height)

    window = Window(
        col_off=500,
        row_off=500,
        width=1000,
        height=1000
    )
    clipped_data = src.read(window=window)
    clipped_transform = src.window_transform(window)
    profile = src.profile
    profile.update(
        width=window.width,
        height=window.height,
        transform=clipped_transform
    )
    with rasterio.open(output_file, "w", **profile) as dst:

        dst.write(clipped_data)


print("\nClipping completed successfully!")
print("Output file:", output_file)
print("Clipped image size: 1000 x 1000 pixels")

#6.
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os
folder = os.path.dirname(os.path.abspath(__file__))

stacked_file = os.path.join(
    folder,
    "Landsat9_Band_Stack.tif"
)
with rasterio.open(stacked_file) as src:

    blue = src.read(1).astype(float)    # B2
    green = src.read(2).astype(float)   # B3
    red = src.read(3).astype(float)     # B4
    nir = src.read(4).astype(float)     # B5


blue = blue * 0.0000275 - 0.2
green = green * 0.0000275 - 0.2
red = red * 0.0000275 - 0.2
nir = nir * 0.0000275 - 0.2
pixels = {

    "Vegetation": (1659, 6080),

    "Water": (2646, 5137),

}
spectral_signatures = {}

for landuse, (row, col) in pixels.items():

    signature = [
        blue[row, col],
        green[row, col],
        red[row, col],
        nir[row, col]
    ]

    spectral_signatures[landuse] = signature


for landuse, values in spectral_signatures.items():

    print("\n", landuse)

    print("Blue  (0.482 µm):", values[0])
    print("Green (0.561 µm):", values[1])
    print("Red   (0.655 µm):", values[2])
    print("NIR   (0.865 µm):", values[3])

wavelengths = [0.482, 0.561, 0.655, 0.865]
plt.figure(figsize=(10, 6))

for landuse, values in spectral_signatures.items():

    plt.plot(
        wavelengths,
        values,
        marker='o',
        linewidth=2,
        label=landuse
    )


plt.xlabel("Wavelength (µm)")
plt.ylabel("Reflectance")

plt.title(
    "Landsat 9 Spectral Signatures of Different Land Use Categories"
)

plt.xticks(wavelengths)

plt.grid(True, linestyle="--", alpha=0.5)

plt.legend()

plt.tight_layout()

plt.show()

#7.
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os
folder = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.join(
    folder,
    "Landsat9_Band_Stack.tif"
)

ndvi_file = os.path.join(
    folder,
    "Landsat9_NDVI.tif"
)

vegetation_file = os.path.join(
    folder,
    "Landsat9_Vegetation_Map.tif"
)
with rasterio.open(input_file) as src:
    red = src.read(3).astype(float)
    nir = src.read(4).astype(float)

    profile = src.profile

    transform = src.transform

    pixel_width = src.res[0]
    pixel_height = src.res[1]
red = red * 0.0000275 - 0.2
nir = nir * 0.0000275 - 0.2
denominator = nir + red
ndvi = np.where(
    denominator != 0,
    (nir - red) / denominator,
    np.nan
)
ndvi_profile = profile.copy()

ndvi_profile.update(
    dtype="float32",
    count=1,
    nodata=-9999
)

ndvi_output = np.where(
    np.isnan(ndvi),
    -9999,
    ndvi
).astype("float32")

with rasterio.open(
    ndvi_file,
    "w",
    **ndvi_profile
) as dst:

    dst.write(ndvi_output, 1)

print("NDVI calculation completed.")
print("NDVI file:", ndvi_file)
threshold = 0.3
vegetation = np.where(
    ndvi >= threshold,
    1,
    0
).astype("uint8")
vegetation_profile = profile.copy()

vegetation_profile.update(
    dtype="uint8",
    count=1,
    nodata=0
)

with rasterio.open(
    vegetation_file,
    "w",
    **vegetation_profile
) as dst:

    dst.write(vegetation, 1)

print("Vegetation classification completed.")
print("Vegetation map:", vegetation_file)
vegetation_pixels = np.sum(vegetation == 1)
pixel_area = pixel_width * pixel_height
vegetated_area_m2 = vegetation_pixels * pixel_area
vegetated_area_hectares = vegetated_area_m2 / 10000
vegetated_area_km2 = vegetated_area_m2 / 1000000
print("NDVI threshold:", threshold)
print("Vegetation pixels:", vegetation_pixels)
print("Pixel size:", pixel_width, "x", pixel_height, "m")
print("Area of one pixel:", pixel_area, "m²")
print("Vegetated area:", vegetated_area_m2, "m²")
print("Vegetated area:", vegetated_area_hectares, "hectares")
print("Vegetated area:", vegetated_area_km2, "km²")
total_pixels = vegetation.size
total_area_m2 = total_pixels * pixel_area
total_area_km2 = total_area_m2 / 1000000
vegetation_percentage = (
    vegetation_pixels / total_pixels
) * 100

print("\nTotal image area:", total_area_km2, "km²")

print(
    "Vegetated percentage:",
    vegetation_percentage,
    "%"
)
plt.figure(figsize=(10, 8))

plt.imshow(
    ndvi,
    cmap="RdYlGn",
    vmin=-1,
    vmax=1
)

plt.colorbar(
    label="NDVI"
)

plt.title("Landsat 9 NDVI Map")

plt.xlabel("Column")
plt.ylabel("Row")

plt.tight_layout()

plt.show()
plt.figure(figsize=(10, 8))

plt.imshow(
    vegetation,
    cmap="gray",
    vmin=0,
    vmax=1
)

plt.title(
    "Vegetated Landcover Map\n"
    "0 = No Vegetation, 1 = Vegetation"
)

plt.xlabel("Column")
plt.ylabel("Row")

plt.colorbar(
    ticks=[0, 1],
    label="Landcover Class"
)

plt.tight_layout()

plt.show()