


class BuildingBlock:
    def __init__(self, id=None, population=None, geometry=None):
        self.id = id
        self.population = population
        self.geometry = geometry


    def plot(self):
        return self.geometry


class CommunityArea(BuildingBlock):
    def __init__(self, id=None, name=None, population=None, geometry=None):
        super().__init__(id, population, geometry)
        self.name = name