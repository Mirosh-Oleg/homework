import time
import geopandas as gpd
import create_grid as cg
import intersecting as itng
import sectors_analysis as sa
from sqlalchemy import create_engine


def connect_to_database():
    """
    Prompts the user for database connection parameters and establishes a connection.

    :return: SQLAlchemy engine object for connecting to the database.
    """

    user = input("Enter database username: ")

    password = input("Enter database password: ")

    host = input("Enter database host (default: localhost): ")

    port = input("Enter database port (default: 5432): ")

    database = input("Enter database name: ")

    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(connection_string)


def fill_database_ukraine_border(file_path, engine):
    """
    Reads a GeoJSON file containing Ukraine's border and uploads it to the database.

    :param file_path: Path to the GeoJSON file containing border data.
    :param engine: SQLAlchemy engine object for database connection.
    """
    geo_data = gpd.read_file(file_path)
    geo_data.to_postgis("ukraine_border", con=engine, if_exists="replace", index=False)
    print("Border data successfully upload!")


def get_square_size():
    """
    Prompts the user to input the size of grid squares in meters.

    :return: Integer value representing the side length of the squares (minimum 5000).
    """
    print("WARNING: If the square size is too small, the computation time may significantly increase!")
    while True:
        try:
            square_size_m = int(input("Enter the size of the grid squares in meters (minimum 5000): "))
            if square_size_m < 5000:
                print("The square size must be at least 5000 meters. Please try again.")
            else:
                return square_size_m
        except ValueError:
            print("Invalid input. Please enter an integer value in meters.")


def get_radius():
    """
    Prompts the user to input the radius for sectors in meters.

    :return: Integer value representing the radius of the sectors.
    """
    while True:
        try:
            radius = int(input("Enter the radius (in meters): "))
            return radius
        except ValueError:
            print("Invalid input. Please enter an integer value in meters.")


def get_azimuths():
    """
    Prompts the user to input up to 3 azimuth values, each serving as the start angle for sectors.

    :return: List of tuples (azimuth, start_angle).
    """
    print("Enter up to 3 azimuths one by one. Each azimuth will also serve as its start angle.")
    azimuths = []
    for i in range(3):
        while True:
            try:
                azimuth = int(input(f"Enter azimuth {i + 1}: "))
                azimuths.append((azimuth, azimuth))  # Create a tuple (azimuth, start_angle)
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")
    return azimuths


def database_upload(data, table_name, engine):
    """
    Uploads a GeoDataFrame to the specified database table.

    :param data: GeoDataFrame to be uploaded.
    :param table_name: Name of the database table.
    :param engine: SQLAlchemy engine object for database connection.
    """
    data.to_postgis(table_name, con=engine, if_exists="replace", index=False)
    print(f"Data successfully imported into the table '{table_name}'.")


def database_save_file(data, file_name):
    """
    Saves a GeoDataFrame to a file in GeoJSON format.

    :param data: GeoDataFrame to be saved.
    :param file_name: Name of the GeoJSON file.
    """
    data.to_file(file_name, driver="GeoJSON")
    print(f"Data saved to {file_name}")


def read_data(tabla, engine):
    """
    Reads data from the specified database table into a GeoDataFrame.

    :param tabla: Name of the database table.
    :param engine: SQLAlchemy engine object for database connection.
    :return: GeoDataFrame containing the data.
    """
    return gpd.read_postgis(f"SELECT * FROM {tabla}", con=engine, geom_col="geometry")


def generate_grid(ukraine_border, square_size_m, engine):
    """
    Generates a grid of squares based on Ukraine's border.

    :param ukraine_border: GeoDataFrame containing Ukraine's border geometry.
    :param square_size_m: Side length of the grid squares in meters.
    :param engine: SQLAlchemy engine object for database connection.
    :return: GeoDataFrame containing the grid.
    """
    grid_generator = cg.GridGenerator(engine)
    grid = grid_generator.create_grid(ukraine_border, square_size_m)
    return grid


def generate_sectors(ukraine_border, grid, engine, radius, arimuths):
    """
    Generates sectors based on the grid vertices and Ukraine's border.

    :param ukraine_border: GeoDataFrame containing Ukraine's border geometry.
    :param grid: GeoDataFrame containing the grid geometry.
    :param engine: SQLAlchemy engine object for database connection.
    :param radius: Radius of the sectors in meters.
    :param arimuths: List of azimuths (angle pairs) for the sectors.
    :return: GeoDataFrame containing the sectors.
    """
    sector_generator = sa.SectorGenerator(engine)
    sectors = sector_generator.create_sectors(ukraine_border, grid, radius, arimuths)
    return sectors


def calculate_intersections(grid, sectors, engine):
    """
    Calculates intersections between grid vertices and sectors.

    :param grid: GeoDataFrame containing the grid.
    :param sectors: GeoDataFrame containing the sectors.
    :param engine: SQLAlchemy engine object for database connection.
    :return: GeoDataFrame containing the intersection results.
    """
    intersection_calculator = itng.SectorVertexIntersection(engine)
    results = intersection_calculator.calculate_intersections(grid, sectors)
    return results


def main():
    """
    Main function to execute the workflow.
    """
    start_time = time.time()

    # Path to the Ukraine border GeoJSON file
    file_path = r"geoBoundaries-UKR-ADM0.geojson"

    # Connect to the database
    engine = connect_to_database()

    # Step 1: Load Ukraine border data into the database
    fill_database_ukraine_border(file_path, engine)

    # Step 2: Read Ukraine border from database
    ukraine_border = read_data("ukraine_border", engine)

    # Step 3: Generate grid
    square_size_m = get_square_size()  # Size of the squares in meters
    grid = generate_grid(ukraine_border, square_size_m, engine)
    database_upload(grid, "ukraine_grid", engine)
    database_save_file(grid, "ukraine_grid.geojson")

    grid = read_data("ukraine_grid", engine)

    # Step 4: Generate sectors
    radius = get_radius()  # Sector radius in meters
    arimuths = get_azimuths()
    sectors = generate_sectors(ukraine_border, grid, engine, radius, arimuths)
    database_upload(sectors, "sectors", engine)
    database_save_file(sectors, "sectors.geojson")

    sectors = read_data("sectors", engine)

    # Step 5: Calculate intersections
    intersections = calculate_intersections(grid, sectors, engine)
    database_upload(intersections, "intersections", engine)
    database_save_file(intersections, "intersections.geojson")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
