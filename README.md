# Geoanalysis and Visualization of Ukraine's Border

This project implements a geoanalysis program that processes the border of Ukraine, divides it into squares, and visualizes the data on an interactive web map using the **Leaflet** library. The project also supports storing and processing data in a relational database PostgreSQL

---

## Features

1. **Loading and Storing Ukraine's Border**:
   - The program loads Ukraine's border coordinates from a GeoJSON file.
   - The data is stored in a relational database PostgreSQL for further processing.

2. **Visualization of Ukraine's Border**:
   - The border is displayed on an interactive web map using **Leaflet**.

3. **Dividing the Map into Squares**:
   - The program divides the map of Ukraine into a grid of equal squares.
   - Each square has a side length(entered by the user during program execution).
   - The vertices of the squares are generated and stored in the database.

4. **Visualization of the Grid**:
   - The grid of squares is displayed on the web map.

5. **Sector Generation**:
   - From each vertex of the grid, the program generates three sectors:
     - Azimuths: 0°, 120°, and 240°.
     - Each sector spans 60° with a configurable radius(entered by the user during program execution)
   - An algorithm calculates which vertices of the grid are intersected by each sector.
   - The results of these intersections are stored in the database.

6. **Visualization of Sectors**:
   - The generated sectors are overlaid on the grid on the web map.

---

## Requirements
-frameworks:
  --flask
  --flask-cors
  --geopandas
  --sqlalchemy
  --shapely
  --tqdm
  --leaflet
-database:
  --empty PostgreSQL database
  
  
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
