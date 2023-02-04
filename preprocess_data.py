import src.population as population
import src.geometries as geometries


"""
The code below saves a geodataframe to data/community_areas.pkl
"""


if __name__ == "__main__":
    _ = population.load_clean_and_save_raw_data()
    _ = geometries.identify_community_area_tracts_and_populations()