import geopandas as gpd
import glob
import os
megh_f=r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab5\data (1)\meghalaya"
ne_f=r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab5\data (1)\NE_states"
meg_shp= glob.glob(os.path.join(megh_f,"*.shp"))[0]
ne_shp= glob.glob(os.path.join(ne_f,"*.shp"))[0]
print("File:",meg_shp)
meg=gpd.read_file(meg_shp)
ne=gpd.read_file(ne_shp)
print("CRS OF MEGHALAYA SHAPEFILE:",meg.crs)
print("CRS OF NORTHEAST SHAPEFILE:",ne.crs)

meg_miss=meg.isnull().sum()
ne_miss=ne.isnull().sum()
if meg_miss.sum()==0:
    print("No missing valuse in meghalaya shapefile")
else:
    print("The missing values in meghalaya shapefile are:",meg_miss)
if ne_miss.sum()==0:
    print("There are no missing values in Northeast shapefile")
else:
    print("The missing values in Northeast shapefile are:",ne_miss)

#3. 
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import glob
meg_f=r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab5\data (1)\meghalaya"
ne_f=r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab5\data (1)\NE_states"
lab5=r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab5"
meg_shp=glob.glob(os.path.join(meg_f,"*.shp"))[0]
ne_shp=glob.glob(os.path.join(ne_f,"*.shp"))[0]
meg=gpd.read_file(meg_shp)
ne=gpd.read_file(ne_shp)
meg_new=meg.to_crs(epsg=4326)
ne_new=ne.to_crs(epsg=4326)
meg_op=os.path.join(lab5,"meg_new.shp")
ne_op=os.path.join(lab5,"ne_new.shp")
meg_new.to_file(meg_op)
ne_new.to_file(ne_op)
print("The new crs of meghalaya and northeastern states are",meg_new.crs,ne_new.crs)
fig,ax=plt.subplots(figsize=(10,8))
ne_new.plot(
    ax=ax,facecolor="pink",edgecolor="red",linewidth=1
)
meg_new.plot(
    ax=ax,facecolor="blue",edgecolor="green",linewidth=1.5
)

ax.set_title("Northeastern states with meghalaya highlighted",fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.show()

#4 
import geopandas as gpd
import glob
import os
import matplotlib.pyplot as plt

folder = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab5\data (1)\NE_states"

shp = glob.glob(os.path.join(folder, "*.shp"))[0]

gdf = gpd.read_file(shp)

print(gdf.columns)

projected = gdf.to_crs(gdf.estimate_utm_crs())

projected["Area_km2"] = projected.geometry.area / 1000000

state_field = gdf.columns[0]

result = projected[[state_field, "Area_km2"]].sort_values(
    by="Area_km2",
    ascending=False
)

print("\nNorth Eastern States - Area")
print(result.to_string(index=False))

plt.figure(figsize=(10, 6))

plt.bar(
    result[state_field].astype(str),
    result["Area_km2"]
)

plt.xlabel("North-Eastern States")
plt.ylabel("Area (km²)")
plt.title("Area of North-Eastern States")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#5
import geopandas as gpd
import matplotlib.pyplot as plt
import glob
import os

folder = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab5\tn"

shp = glob.glob(os.path.join(folder, "*.shp"))[0]

gdf = gpd.read_file(shp)

print("Projection:")
print(gdf.crs)

print("\nColumns:")
print(gdf.columns)

print("\nNumber of features:")
print(len(gdf))

gdf.plot(
    figsize=(10, 8),
    edgecolor="black",
    linewidth=0.8
)

plt.title("State Boundary")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()

#6. 
import geopandas as gpd
import glob
import os
import matplotlib.pyplot as plt

folder = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab5\india"

shp = glob.glob(os.path.join(folder, "*.shp"))[0]

india = gpd.read_file(shp)

kerala = india[india["STATE"] == "KERALA"]

kerala_4326 = kerala.to_crs(epsg=4326)

print("Kerala CRS:")
print(kerala_4326.crs)

output = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab5\Kerala_EPSG4326.shp"

kerala_4326.to_file(output)

print("\nKerala shapefile saved at:")
print(output)

kerala_4326.plot(
    figsize=(8, 8),
    edgecolor="black",
    linewidth=1
)

plt.title("Kerala State - EPSG:4326")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()

#7. 
import geopandas as gpd
import glob
import os
import matplotlib.pyplot as plt

folder = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab5\kerala"

shp = glob.glob(os.path.join(folder, "*.shp"))[0]

kerala = gpd.read_file(shp)

print("Columns:")
print(kerala.columns)

print("\nCRS:")
print(kerala.crs)

kerala["Area_km2"] = kerala.geometry.area / 1000000

result = kerala[["District_n", "Area_km2"]].sort_values(
    by="Area_km2",
    ascending=False
)

print("\nKerala District Areas:")
print(result.to_string(index=False))

plt.figure(figsize=(12, 7))

plt.bar(
    result["District_n"].astype(str),
    result["Area_km2"]
)

plt.xlabel("Districts")
plt.ylabel("Area (km²)")
plt.title("Area of Districts in Kerala")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()