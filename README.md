# Geoanalysis and Visualization of Ukraine's Border

This project implements a geoanalysis program that processes the border of Ukraine, divides it into squares, and visualizes the data on an interactive web map using the **Leaflet** library. The project also supports storing and processing data in a relational database PostgreSQL

---

## Requirements
1. **frameworks**:
   - flask
   - flask-cors
   - geopandas
   - sqlalchemy
   - shapely
   - tqdm
   - leaflet
2. **database**:
   - empty PostgreSQL database
  
  
---

## How It Works

1. **Database setyp**:
   - The user must first create an empty database in PostgreSQL and named it.
  
2. **Database Connection**:
   - The program prompts the user for database connection parameters (username, password, host, port, and database name).

3. **Program Processing**:
   - Loads Ukraine's border coordinates.
   - Divides the territory into a grid of squares.
   - Generates sectors from each vertex of the grid.
   - Calculates intersections: The program computes which vertices of the grid are intersected by each sector.

4. **Storing and Processing Data**:
   - Saves the border, grid vertices, and sector intersection results in the database.

5. **Visualization**:
   - Displays the border, grid, and sectors on an interactive map using **Leaflet**.

---
