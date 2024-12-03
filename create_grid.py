import geopandas as gpd
from shapely.geometry import box
import numpy as np


class GridGenerator:
    def __init__(self, engine):
        """
        Initializes the GridGenerator object.
        :param engine: SQLAlchemy engine for connecting to the database.
        """
        self.engine = engine

    def create_grid(self, ukraine_border, square_size_km):
        """
        Creates a grid of squares based on the Ukraine border and saves it to the database.
        :param ukraine_border: GeoDataFrame containing the geometry of Ukraine's border.
        :param square_size_km: Size of the square's side in meters.
        :return: GeoDataFrame containing the grid.
        """
        # Convert to metric projection (EPSG:3857)
        ukraine_border = ukraine_border.to_crs("EPSG:3857")

        # Determine bounds
        xmin, ymin, xmax, ymax = ukraine_border.total_bounds

        # Grid step (square size)
        step = square_size_km

        # Vectorized grid creation
        x_coords = np.arange(xmin, xmax, step)
        y_coords = np.arange(ymin, ymax, step)
        grid_polygons = [
            box(x, y, x + step, y + step) for x in x_coords for y in y_coords
        ]

        # Creating GeoDataFrame for grid
        grid = gpd.GeoDataFrame(geometry=grid_polygons, crs="EPSG:3857")
        print("Grid created.")

        # Intersection with Ukraine border
        grid_within_ukraine = gpd.overlay(grid, ukraine_border, how='intersection')
        print("Intersection with Ukraine border completed.")

        # Convert back to EPSG:4326
        grid_within_ukraine = grid_within_ukraine.to_crs("EPSG:4326")

        return grid_within_ukraine
