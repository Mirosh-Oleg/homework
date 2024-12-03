# Geoanalysis and Visualization of Ukraine's Border

This project implements a geoanalysis program that processes the border of Ukraine, divides it into squares, and visualizes the data on an interactive web map using the **Leaflet** library. The project also supports storing and processing data in a relational database PostgreSQL

---

## Requirements
1. **Frameworks and Libraries**:
   - flask
   - flask-cors
   - geopandas
   - sqlalchemy
   - shapely
   - tqdm
   - leaflet
2. **Database**:
   - empty PostgreSQL database
  
---

## How To Run It

1. **Database setyp**:
   - The user must first create an empty database in PostgreSQL and named it.
  
2. **Run main.py**
   what this fild do:
      1) Connection to database
         - The program prompts the user for database(DB) connection parameters:
            - DB Username.
            - DB password.
            - DB Host(default: localhost).
            - DB Port(default: 5432 for PostgreSQL).
            - DB Name.
         - Automatic Data Loading: The program automatically creates the necessary tables and loads data into the database. No manual table creation is required.
      2) The program prompts the user for size of the grid squares in meters.
      3) The program prompts the user for radius for sectors in meters.
      4) The program prompts the user for valuse for azimuths.
