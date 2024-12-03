import geopandas as gpd
from shapely.geometry import Point
from tqdm import tqdm


class SectorVertexIntersection:
    def __init__(self, engine):
        """
        Initializes the SectorVertexIntersection object.
        :param engine: SQLAlchemy engine for database connection.
        """
        self.engine = engine

    def extract_vertices(self, grid):
        """
        Extract unique vertices from the grid polygons.
        :param grid: GeoDataFrame containing the grid geometry.
        :return: GeoDataFrame with unique vertices as points.
        """
        vertices = gpd.GeoDataFrame(
            geometry=[
                Point(coord) for polygon in grid.geometry if polygon.geom_type == "Polygon"
                for coord in polygon.exterior.coords[:]
            ],
            crs=grid.crs
        )
        print(f"Unique vertices extracted: {len(vertices)}")
        return vertices

    def calculate_intersections(self, grid, sectors):
        """
        Calculates which vertices of the grid are intersected by each sector.
        :param grid: GeoDataFrame containing the grid.
        :param sectors: GeoDataFrame containing the sectors.
        :return: GeoDataFrame containing sectors with intersected vertices.
        """
        vertices = self.extract_vertices(grid)

        vertices_sindex = vertices.sindex

        sector_vertex_map = []

        for sector_id, sector_row in tqdm(sectors.iterrows(), total=len(sectors), desc="Processing sectors"):
            sector_geom = sector_row.geometry
            sector_bounds = sector_geom.bounds  # Precompute bounds
            possible_matches_index = list(vertices_sindex.intersection(sector_bounds))
            possible_vertices = vertices.iloc[possible_matches_index]
            intersecting_mask = possible_vertices.geometry.intersects(sector_geom)
            intersecting_vertices = possible_vertices[intersecting_mask]
            sector_vertex_map.append({
                "geometry": sector_geom,
                "azimuth": sector_row.get("azimuth", None),
                "vertex_ids": intersecting_vertices.index.tolist()
            })

        results_gdf = gpd.GeoDataFrame(sector_vertex_map, crs=sectors.crs)
        print(f"Intersections calculated for {len(sectors)} sectors.")
        return results_gdf
