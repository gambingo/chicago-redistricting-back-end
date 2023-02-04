import pandas as pd

from src import CommunityArea


class Redistricting:
    def __init__(self, gdf_filepath, building_block_type="community_area"):
        """
        TKTK
        """
        self.gdf_filepath = gdf_filepath
        self.building_block_type = building_block_type

        self.blocks = self.form_building_blocks()


    def form_building_blocks(self):
        """
        These are not census blocks but the geographic boundary objects we will
        build the wards out of. To start, they will be community areas. Next, 
        census tracts. Likely never actual census blocks for this project 
        because they are too small and numerous.
        """
        gdf = pd.read_pickle(self.gdf_filepath)

        if self.building_block_type == "community_area":
            community_areas = []
            arg_columns = ["id", "name", "population", "geometry"]
            gdf_dict = gdf.reset_index()[arg_columns].to_dict(orient="index")

            for kwargs in gdf_dict.values():
                community_areas.append(CommunityArea(**kwargs))

            return community_areas

        else:
            # TODO: Census Tracts
            raise NotImplementedError
            
