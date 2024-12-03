import geopandas as gpd
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
import numpy as np
from tqdm import tqdm


class SectorGenerator:
    def __init__(self, engine):
        """
        Initializes the SectorGenerator object.
        :param engine: SQLAlchemy engine for connecting to the database.
        """
        self.engine = engine

    def generate_sector(self, center, radius, start_angle, end_angle, num_points=10):
        """
        Generates a single sector as a polygon.

        :param center: Shapely Point object representing the center of the sector.
        :param radius: Radius of the sector in meters.
        :param start_angle: Start angle of the sector in degrees.
        :param end_angle: End angle of the sector in degrees.
        :param num_points: Number of points to approximate the curved edge of the sector.
        :return: Shapely Polygon object representing the sector.
        """

        # Generate angles and convert them to radians
        angles = np.linspace(start_angle, end_angle, num_points + 1)
        angles_rad = np.radians(angles)

        # Calculate the coordinates for the points of the sector
        x_coords = center.x + radius * np.cos(angles_rad)
        y_coords = center.y + radius * np.sin(angles_rad)

        # Create the polygon points (from center to arc and back to center)
        sector_points = [(center.x, center.y)] + list(zip(x_coords, y_coords)) + [(center.x, center.y)]
        return Polygon(sector_points)

    def create_sectors(self, ukraine_border, grid, radius, azimuths):
        """
        Generates sectors for each vertex of the grid that fall within Ukraine's border.

        :param ukraine_border: GeoDataFrame containing Ukraine's border geometry.
        :param grid: GeoDataFrame containing the grid geometry.
        :param radius: Radius of the sectors in meters.
        :param azimuths: List of tuples (azimuth, start_angle) defining sector angles.
        :return: GeoDataFrame containing the generated sectors.
        """
        # Reproject border and grid to a metric projection (EPSG:3857)
        ukraine_border = ukraine_border.to_crs("EPSG:3857")
        grid = grid.to_crs("EPSG:3857")

        # Buffer the border to exclude vertices near the border edge
        ukraine_border_buffered = unary_union(ukraine_border.geometry.buffer(-1))

        # Extract unique vertices from the grid
        vertices = gpd.GeoDataFrame(
            geometry=list(
                {Point(coord) for row in grid.geometry if row.geom_type == "Polygon"
                 for coord in row.exterior.coords[:]}
            ),
            crs="EPSG:3857",
        )
        print(f"Unique vertices found: {len(vertices)}")

        # Filter vertices that fall within Ukraine's buffered border
        ukraine_border_gdf = gpd.GeoDataFrame(geometry=[ukraine_border_buffered], crs="EPSG:3857")
        vertices_filtered = vertices.sjoin(ukraine_border_gdf, predicate="within").drop(columns=["index_right"])
        print(f"Vertices after filtering: {len(vertices_filtered)}")

        # Generate sectors
        sectors = []
        for idx, center in tqdm(enumerate(vertices_filtered.geometry), total=len(vertices_filtered),
                                desc="Generating sectors"):
            for azimuth, start_angle in azimuths:
                sectors.append({
                    "geometry": self.generate_sector(center, radius, start_angle, start_angle + 60),
                    "azimuth": azimuth,
                    "vertex_id": idx
                })

        # Convert sectors to GeoDataFrame
        sectors = gpd.GeoDataFrame(sectors, crs="EPSG:3857")
        sectors = sectors.to_crs("EPSG:4326")
        print(f"Sectors created: {len(sectors)}")
        return sectors
