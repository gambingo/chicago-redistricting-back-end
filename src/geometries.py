"""
Data Preprocessing: Assigning each census tract to a community area so that we 
can tally up the popluation of each community area
"""
import os
from pathlib import Path

import pandas as pd
import geopandas as gpd

from directories import DATA_DIR

# This is to suppress the CRS warning that generates during the buffer 
# operation. It's not a problem in this case, but I sure wish I had a more 
# specific suppression.
import warnings
warnings.filterwarnings("ignore")


def load_data():
    # Chicago Community Areas
    filename = "Boundaries - Community Areas (current).geojson"
    community_areas = gpd.read_file(DATA_DIR / filename)
    index_col = "area_num_1"
    community_areas[index_col] = community_areas[index_col].astype(int)
    community_areas.set_index(index_col, inplace=True)
    
    # Illinois Census Tracts
    filename = "2020-census/tl_2020_17_tract/tl_2020_17_tract.shp"
    illinois_tracts = gpd.read_file(DATA_DIR / filename)
    index_col = "NAME"
    illinois_tracts[index_col] = illinois_tracts[index_col].astype(float)
    illinois_tracts.set_index(index_col, inplace=True)

    # City of Chicago Boundaries
    filename = "Boundaries - City.geojson"
    city_limits = gpd.read_file(DATA_DIR / filename)
    
    return community_areas, illinois_tracts, city_limits


def identify_tracts_within_chicagoland(city_limits, illinois_tracts, load_existing=False):
    """
    Use a buffer to draw a "bubble" around the city limits and filter to all 
    tracts within that bubble. This approach will capture any census tracts 
    that straddle the city limits.
    """
    filename = "chicagoland_tracts.pkl"
    if load_existing and os.path.exists(DATA_DIR / filename):
        chicagoland_tracts = pd.read_pickle(DATA_DIR / filename)

    else:
        buffer_dist = 0.04
        chicago_bubble = city_limits.geometry.buffer(buffer_dist).geometry
        chicago_bubble_series = gpd.GeoSeries(
            [chicago_bubble.iloc[0]]*illinois_tracts.shape[0],
            index=illinois_tracts.index)
        # The GeoSeries.within() method only compares row to row for series 
        # that have the same index.
        chicagoland_tracts = illinois_tracts[illinois_tracts.within(chicago_bubble_series)]
        chicagoland_tracts.to_pickle(DATA_DIR / filename)        

    return chicagoland_tracts


def assign_tracts_to_community_areas(chicagoland_tracts, community_areas):
    """
    Assign tracts to community areas based on percent overlap of geometries.
    `chicagoland_tracts` includes tracts outside the city limits.

    We will assign each tract to the community area it is most within. 
    Visual inspection shows that the 2020 census tracts and community area
    boundaries play nicely. The only tract that truly spans two community areas
    is the tract for Midway airport (which has population of 18!). However, 
    since these datasets were draw by two separate organizations, their borders
    do not align precisely enough to use convenient shapely opeations like 
    'touches' or 'within'. Also, the census tracts along the Chicago shoreline 
    extend into the lake, but this method properly assigns them to a community 
    area on land.
    """
    # Area of Intersection / Total Tract Area = Percent Tract Overlap
    pairwise_overlap = chicagoland_tracts.geometry.apply(
        lambda gmtry: community_areas.geometry.intersection(gmtry).area/gmtry.area)

    # Drop Tracts that don't overlap any Community Areas (outside city limits)
    pairwise_overlap = pairwise_overlap[pairwise_overlap.any(axis=1)]

    # Filter by minimum overlap
    threshold = 0.20
    pairwise_overlap = pairwise_overlap[pairwise_overlap.max(axis=1) >= threshold]

    # CAs are Column Labels; Tracts are Row Labels
    CA_tract_assignments = pd.DataFrame(
        pairwise_overlap.T.idxmax(), 
        columns=["Community Area"])
    CA_tract_assignments.index.name = "Census Tract"

    return CA_tract_assignments


def identify_tracts_within_chicago(chicagoland_tracts, CA_tract_assignments):
    """
    From the community area assignments, we now have tracts that are only
    within Chicago and not "Chicagoland". Save these tracts.
    """
    mask = chicagoland_tracts.index.isin(CA_tract_assignments.index)
    chicago_tracts = chicagoland_tracts[mask]
    chicago_tracts.to_pickle(DATA_DIR / "chicago_census_tracts.pkl")
    return chicago_tracts



if __name__ == "__main__":
    community_areas, illinois_tracts, city_limits = load_data()
    chicagoland_tracts = identify_tracts_within_chicagoland(city_limits, illinois_tracts)
    CA_tract_assignments = assign_tracts_to_community_areas(chicagoland_tracts, community_areas)
    chicago_tracts = identify_tracts_within_chicago(chicagoland_tracts, CA_tract_assignments)
    print(chicago_tracts)