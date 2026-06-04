"""
Prep map data layers for render_maps.py
===============================================================================
Exports the health-&-safety-filtered 311 points (the same filter used by
../311_heatmap/vacancy_311_synthesis.py) from the full 1.5M-row 311 GeoPackage
to a small EPSG:4326 GeoPackage that render_maps.py turns into a density raster.

Run with the project's default python (needs geopandas):

    python maps/prep_layers.py

Input : data/SacCounty_SalesForce311_calls.gpkg   (layer SalesForce311)
Output: maps/data/hs_311.gpkg                      (layer hs_311, WGS84)

The vacant-parcel layer (hackathon_data/vacant_parcels.geojson) is used directly
by render_maps.py and needs no prep.
"""

from pathlib import Path
import json
import urllib.request

import geopandas as gpd
from shapely.geometry import shape

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CALLS_GPKG = PROJECT_ROOT / "data" / "SacCounty_SalesForce311_calls.gpkg"
OUT_GPKG = SCRIPT_DIR / "data" / "hs_311.gpkg"
COUNTY_GEOJSON = SCRIPT_DIR / "data" / "sacramento_county.geojson"
COUNCIL_SHP = PROJECT_ROOT / "data" / "council_districts" / "Council_Districts.shp"
COUNCIL_GEOJSON = SCRIPT_DIR / "data" / "council_districts.geojson"

# Sacramento County boundary (FIPS 06067) from the stable plotly counties file.
COUNTIES_URL = ("https://raw.githubusercontent.com/plotly/datasets/master/"
                "geojson-counties-fips.json")
SAC_FIPS = "06067"

# Mirrors HS_LEVEL1 / HS_CATEGORYNAME in vacancy_311_synthesis.py.
WHERE = (
    "CategoryLevel1 IN ('Code Enforcement','Homeless Camp','Homeless Camp - Primary') "
    "OR CategoryName IN ("
    "'Solid Waste Illegal Dumping',"
    "'Solid Waste Code Enforcement Illegal Dumping',"
    "'Solid Waste Code Enforcement Receptacles',"
    "'Solid Waste Code Enforcement Receptacles - Residential',"
    "'Solid Waste Code Enforcement Receptacles - Commercial',"
    "'Animal Control Abandoned')"
)
COLS = ["CategoryLevel1", "CategoryName", "DateCreated", "CouncilDistrictNumber"]


def build_county_boundary():
    """Fetch + save the Sacramento County boundary (skips if already present)."""
    if COUNTY_GEOJSON.exists():
        return
    print("Fetching Sacramento County boundary...")
    with urllib.request.urlopen(COUNTIES_URL, timeout=60) as r:
        data = json.load(r)
    feats = [f for f in data["features"] if f.get("id") == SAC_FIPS]
    if not feats:
        print("  WARNING: county boundary not found; maps will omit county lines.")
        return
    gdf = gpd.GeoDataFrame({"name": ["Sacramento County"]},
                           geometry=[shape(feats[0]["geometry"])], crs="EPSG:4326")
    gdf.to_file(COUNTY_GEOJSON, driver="GeoJSON")
    print(f"Wrote county boundary -> {COUNTY_GEOJSON.relative_to(PROJECT_ROOT)}")


def build_council_districts():
    """Reproject the council-district shapefile to WGS84 (skips if present).

    The raw EPSG:2226 shapefile does not reproject reliably onto the 3857
    basemap inside a pyQGIS layout, so the maps consume a WGS84 copy.
    """
    if COUNCIL_GEOJSON.exists() or not COUNCIL_SHP.exists():
        return
    print("Reprojecting council districts to WGS84...")
    cd = gpd.read_file(COUNCIL_SHP).to_crs("EPSG:4326")
    cd = cd[["DISTNUM", "NAME", "geometry"]]
    cd.to_file(COUNCIL_GEOJSON, driver="GeoJSON")
    print(f"Wrote council districts -> {COUNCIL_GEOJSON.relative_to(PROJECT_ROOT)}")


def main():
    build_county_boundary()
    build_council_districts()
    if not CALLS_GPKG.exists():
        raise SystemExit(
            f"MISSING: {CALLS_GPKG}\n"
            "  Download SacCounty_SalesForce311_calls.gpkg into data/ "
            "(see hackathon_data/DATA_DOWNLOAD.md)."
        )
    OUT_GPKG.parent.mkdir(parents=True, exist_ok=True)
    print("Reading health & safety-filtered 311 points (pushed down to the source)...")
    calls = gpd.read_file(CALLS_GPKG, layer="SalesForce311", where=WHERE,
                          columns=COLS)
    if calls.crs is None:
        calls = calls.set_crs("EPSG:4326")
    calls = calls[~calls.geometry.is_empty & calls.geometry.notna()].to_crs("EPSG:4326")
    calls.to_file(OUT_GPKG, layer="hs_311", driver="GPKG")
    print(f"Wrote {len(calls):,} points -> {OUT_GPKG.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
