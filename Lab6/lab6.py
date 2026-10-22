


#1.
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
points = [
    Point(100, 100),
    Point(200, 300),
    Point(400, 400),
    Point(600, 200)
]

points_gdf = gpd.GeoDataFrame(
    geometry=points,
    crs="EPSG:32643"
)
buffer_100m = points_gdf.copy()
buffer_100m["geometry"] = points_gdf.geometry.buffer(100)
buffer_500m = points_gdf.copy()
buffer_500m["geometry"] = points_gdf.geometry.buffer(500)
buffer_1km = points_gdf.copy()
buffer_1km["geometry"] = points_gdf.geometry.buffer(1000)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
buffer_100m.plot(ax=axes[0], color="lightblue", edgecolor="blue")
points_gdf.plot(ax=axes[0], color="black", markersize=15)
axes[0].set_title("100 m Buffer")
buffer_500m.plot(ax=axes[1], color="lightgreen", edgecolor="green")
points_gdf.plot(ax=axes[1], color="black", markersize=15)
axes[1].set_title("500 m Buffer")
buffer_1km.plot(ax=axes[2], color="lightcoral", edgecolor="red")
points_gdf.plot(ax=axes[2], color="black", markersize=15)
axes[2].set_title("1 km Buffer")
plt.tight_layout()
plt.show()

#2.
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, box
circle = Point(200, 200).buffer(150)
rectangle = box(250, 150, 450, 350)
circle_gdf = gpd.GeoDataFrame(
    {"type": ["Circle"]},
    geometry=[circle],
    crs="EPSG:32643"
)
rectangle_gdf = gpd.GeoDataFrame(
    {"type": ["Rectangle"]},
    geometry=[rectangle],
    crs="EPSG:32643"
)
intersection = gpd.overlay(
    circle_gdf,
    rectangle_gdf,
    how="intersection"
)
fig, ax = plt.subplots(figsize=(8, 8))
circle_gdf.plot(ax=ax, color="skyblue", alpha=0.5, edgecolor="blue")
rectangle_gdf.plot(ax=ax, color="lightgreen", alpha=0.5, edgecolor="green")
if not intersection.empty:
    intersection.plot(ax=ax, color="red", alpha=0.8, edgecolor="black")
ax.set_title("Intersection of Circular and Rectangular Polygons")
plt.show()
print("Number of intersection features:", len(intersection))
print("Intersection area (m^2):", intersection.geometry.area.sum())



import geopandas as gpd
import matplotlib.pyplot as plt
bp = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\buildings\nedumangad_buildings.shp"
roads = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\roads\nedumangad_road.shp"
water = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\waterways\nedumangad_waterways.shp"
pois = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\pois\nedumangad_pois.shp"
lulc = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\landuse\nedumangad_landuse.shp"
bw=r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\waterways\buildings_within_100m_stream\buildings_within_100m_stream.shp"
b = gpd.read_file(bp)
r = gpd.read_file(roads)
w = gpd.read_file(water)
p = gpd.read_file(pois)
l = gpd.read_file(lulc)
x=gpd.read_file(bw)
print("Buildings CRS:", b.crs)
print("Roads CRS:", r.crs)
print("Waterways CRS:", w.crs)
print("POIs CRS:", p.crs)
print("LULC CRS:", l.crs)
print("buildings_with_water CRS:", x.crs)

#3.
# Display LULC columns

# Question 3(a): Identify forest areas in the LULC layer

print("LULC columns:", l.columns.tolist())

print("Available LULC classes:")
print(l["fclass"].dropna().unique())

forest = l[
    l["fclass"].astype(str).str.contains(
        "forest", case=False, na=False
    )
].copy()

print("Number of forest polygons:", len(forest))

print("Forest classes:")
print(forest["fclass"].value_counts())

if not forest.empty:
    forest.plot(
        figsize=(8, 6),
        color="forestgreen",
        edgecolor="black"
    )
    plt.title("Forest Areas in Nedumangad")
    plt.xlabel("Easting (m)")
    plt.ylabel("Northing (m)")
    plt.show()

# Question 3(b): Identify primary roads

print("Road columns:", r.columns.tolist())
print("Available road classes:", r["fclass"].dropna().unique())

primary_roads = r[
    r["fclass"].astype(str).str.lower() == "primary"
].copy()

print("Number of primary road features:", len(primary_roads))

# Display road names, if a name field exists
name_field = next(
    (c for c in ["name_2", "name", "name_1"]
     if c in primary_roads.columns),
    None
)

if name_field:
    print("Primary road names:")
    print(primary_roads[name_field].dropna().unique())
else:
    print("No recognised road-name column found.")

if not primary_roads.empty:
    primary_roads.plot(
        figsize=(8, 6),
        color="red",
        linewidth=1
    )
    plt.title("Primary Roads in Nedumangad")
    plt.xlabel("Easting (m)")
    plt.ylabel("Northing (m)")
    plt.show()

# Question 3(c): Calculate total mapped LULC area

# Geometry area is in square metres because the layer
# should be in a projected CRS measured in metres.
l["area_km2"] = l.geometry.area / 1_000_000

total_area = l["area_km2"].sum()

print("Total mapped LULC area (km^2):", round(total_area, 4))
print("Number of LULC polygons:", len(l))

# Area of each land-use class
print("\nArea by LULC class (km^2):")

area_by_class = (
    l.groupby("fclass")["area_km2"]
    .sum()
    .sort_values(ascending=False)
)

print(area_by_class.round(4))


# Question 4: Buildings within 200 m of rivers/streams

print("Waterway classes:", w["fclass"].dropna().unique())

river_streams = w[
    w["fclass"].astype(str).str.contains(
        r"river|stream", case=False, na=False
    )
].copy()

print("River/stream features:", len(river_streams))

if not river_streams.empty:
    # Create a 200 m buffer around rivers/streams
    water_buffer = river_streams.geometry.buffer(200).union_all()

    # Select buildings that intersect the buffer
    buildings_200m = b[
        b.geometry.intersects(water_buffer)
    ].copy()

    print("Buildings within 200 m:", len(buildings_200m))

    print("Building columns:", buildings_200m.columns.tolist())

    ax = river_streams.plot(
        figsize=(8, 6),
        color="blue",
        linewidth=1
    )

    buildings_200m.plot(
        ax=ax,
        color="orange",
        markersize=4
    )

    plt.title("Buildings Within 200 m of Rivers/Streams")
    plt.xlabel("Easting (m)")
    plt.ylabel("Northing (m)")
    plt.show()
else:
    print("No river/stream classes matched. Check the waterway labels.")



import geopandas as gpd
import matplotlib.pyplot as plt

# File paths
bp = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\buildings\nedumangad_buildings.shp"
roads = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\roads\nedumangad_road.shp"
water = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\waterways\nedumangad_waterways.shp"
pois = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\pois\nedumangad_pois.shp"
lulc = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\landuse\nedumangad_landuse.shp"
bw = r"C:\Users\jothi\Mtech\sem1\PYTHON\Lab6\nedumangad\waterways\buildings_within_100m_stream\buildings_within_100m_stream.shp"

# Load layers
b = gpd.read_file(bp)
r = gpd.read_file(roads)
w = gpd.read_file(water)
p = gpd.read_file(pois)
l = gpd.read_file(lulc)
x = gpd.read_file(bw)

# Roads CRS is EPSG:32644
print("Original POI CRS:", p.crs)
print("Road CRS:", r.crs)

# Assign EPSG:32644 ONLY if POI coordinates are already in UTM Zone 44N
if p.crs is None:
    p = p.set_crs(epsg=32644)

# Reproject POIs to match roads
p = p.to_crs(r.crs)

# Check projected CRS
print("POI CRS after processing:", p.crs)

if r.crs.is_geographic:
    raise ValueError("Road CRS must be projected in metres.")

# Check fields
print("POI columns:", p.columns.tolist())
print("Road columns:", r.columns.tolist())

if "fclass" not in p.columns or "fclass" not in r.columns:
    raise ValueError("Check whether both layers contain an 'fclass' field.")

print("\nPOI categories:")
print(p["fclass"].value_counts(dropna=False))

# Select hospital-category POIs
hospitals = p[
    p["fclass"].astype(str).str.lower().str.strip() == "hospital"
].copy()

# Select primary and trunk roads
major_roads = r[
    r["fclass"].astype(str).str.lower().str.strip().isin(
        ["primary", "trunk"]
    )
].copy()

print("\nHospitals:", len(hospitals))
print("Primary/trunk road features:", len(major_roads))

if hospitals.empty or major_roads.empty:
    print("No matching features. Check the printed categories.")
else:
    # Buffer roads by 750 metres
    road_buffer = major_roads.geometry.buffer(750).union_all()

    # Select hospitals within the buffer
    hospitals_near_roads = hospitals[
        hospitals.geometry.intersects(road_buffer)
    ].copy()

    print(
        "\nHospitals within 750 m of primary/trunk roads:",
        len(hospitals_near_roads)
    )
    print(
        "Hospitals outside 750 m:",
        len(hospitals) - len(hospitals_near_roads)
    )

    # Print hospital names
    name_field = next(
        (field for field in ["name", "name_1", "name_2", "Name"]
         if field in hospitals_near_roads.columns),
        None
    )

    if name_field:
        print("\nHospital names:")
        print(
            hospitals_near_roads[name_field]
            .dropna()
            .drop_duplicates()
            .to_list()
        )
    else:
        print("No recognised name field found.")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    major_roads.plot(ax=ax, color="grey", linewidth=0.7)
    hospitals_near_roads.plot(ax=ax, color="red", markersize=20)

    ax.set_title("Hospitals Within 750 m of Primary/Trunk Roads")
    ax.set_xlabel("Easting (m)")
    ax.set_ylabel("Northing (m)")
    plt.tight_layout()
    plt.show()




# Question 6: Find bridges that intersect rivers



import geopandas as gpd
import matplotlib.pyplot as plt

# QUESTION 6: Bridges intersecting rivers
# Requires existing variables r (roads) and w (waterways).

print("Road CRS:", r.crs)
print("Waterway CRS:", w.crs)
print("Road columns:", r.columns.tolist())
print("Waterway columns:", w.columns.tolist())

if r.crs is None or w.crs is None:
    raise ValueError("Roads and waterways must have defined CRSs.")

# Match the waterway CRS to the roads CRS
if w.crs != r.crs:
    w = w.to_crs(r.crs)

if "bridge" not in r.columns:
    raise ValueError("No 'bridge' field found in the roads layer.")

if "fclass" not in w.columns:
    raise ValueError("No 'fclass' field found in the waterways layer.")

print("\nBridge attribute values:")
print(r["bridge"].value_counts(dropna=False))

print("\nWaterway classes:")
print(w["fclass"].value_counts(dropna=False))

# Select bridge features
bridge_values = r["bridge"].astype(str).str.upper().str.strip()

bridges = r[
    bridge_values.isin(["T", "TRUE", "YES", "1"])
].copy()

# Select rivers
rivers = w[
    w["fclass"].astype(str).str.lower().str.strip() == "river"
].copy()

# Remove missing/empty geometries
bridges = bridges[
    bridges.geometry.notna() & ~bridges.geometry.is_empty
].copy()

rivers = rivers[
    rivers.geometry.notna() & ~rivers.geometry.is_empty
].copy()

print("\nBridge features:", len(bridges))
print("River features:", len(rivers))

if bridges.empty or rivers.empty:
    print("No matching bridge or river features were found.")
else:
    # Find bridge features intersecting river geometries
    bridges_on_rivers = gpd.sjoin(
        bridges,
        rivers[["geometry"]],
        how="inner",
        predicate="intersects"
    )

    # Count each original bridge/road feature once
    bridges_on_rivers = bridges_on_rivers[
        ~bridges_on_rivers.index.duplicated(keep="first")
    ].copy()

    print(
        "\nTotal bridge features intersecting rivers:",
        len(bridges_on_rivers)
    )

    # Print associated road/bridge names, if available
    name_field = next(
        (field for field in ["name_2", "name", "name_1", "Name"]
         if field in bridges_on_rivers.columns),
        None
    )

    if name_field:
        names = (
            bridges_on_rivers[name_field]
            .dropna()
            .astype(str)
            .str.strip()
        )
        names = sorted(names[names != ""].unique())

        print("\nBridge/associated road names:")
        if names:
            for name in names:
                print(name)
        else:
            print("No names recorded for the matching features.")
    else:
        print("No recognised name field found.")
        print("Available columns:", bridges_on_rivers.columns.tolist())

    # Plot rivers in blue and intersecting bridge features in red
    fig, ax = plt.subplots(figsize=(10, 8))

    rivers.plot(ax=ax, color="blue", linewidth=1)
    bridges_on_rivers.plot(ax=ax, color="red", linewidth=2)

    ax.set_title("Bridge Features Intersecting Rivers")
    ax.set_xlabel("Easting / projected coordinate")
    ax.set_ylabel("Northing / projected coordinate")
    plt.tight_layout()
    plt.show()

# =====================================================
# END OF QUESTION 6
# =====================================================



# Question 7: Primary and tertiary roads intersecting forest

print("LULC classes:", l["fclass"].dropna().unique())
print("Road classes:", r["fclass"].dropna().unique())

forest = l[
    l["fclass"].astype(str).str.contains(
        "forest", case=False, na=False
    )
].copy()

selected_roads = r[
    r["fclass"].astype(str).str.lower().isin(
        ["primary", "tertiary"]
    )
].copy()

print("Forest polygons:", len(forest))
print("Primary/tertiary road features:", len(selected_roads))

if not forest.empty and not selected_roads.empty:
    roads_in_forest = gpd.sjoin(
        selected_roads,
        forest[["fclass", "geometry"]],
        how="inner",
        predicate="intersects"
    )

    # Count each original road feature only once
    roads_in_forest = roads_in_forest[
        ~roads_in_forest.index.duplicated(keep="first")
    ]

    print(
        "Primary/tertiary road features intersecting forest:",
        len(roads_in_forest)
    )

    name_field = next(
        (c for c in ["name_2", "name", "name_1"]
         if c in roads_in_forest.columns),
        None
    )

    if name_field:
        print("Road names:")
        print(roads_in_forest[name_field].dropna().unique())

    roads_in_forest.plot(
        figsize=(8, 6),
        color="darkgreen",
        linewidth=1
    )

    plt.title("Primary and Tertiary Roads Intersecting Forest")
    plt.xlabel("Easting (m)")
    plt.ylabel("Northing (m)")
    plt.show()
else:
    print("No forest or matching roads found. Check the class labels.")
