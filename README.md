# Geoanalysis and Visualization of Ukraine's Border

This project implements a geoanalysis program that processes the border of Ukraine, divides it into squares, and visualizes the data on an interactive web map using the **Leaflet** library. The project also supports storing and processing data in a relational database PostgreSQL

---

## Requirementss
1. **Frameworks and Libraries**:
   
   In requirements.txt
     
3. **Database**:
   
   PostgreSQL (version:17)
   
   Download it from the [official website](https://www.postgresql.org/download/).
   
   empty PostgreSQL database
  
---

## How To Run It

1. **Database setyp**:
   - The user must first create an empty database in PostgreSQL and named it.
  
2. **Run main.py**
   what this file do:
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

3. **How to run interactive map**
   1) run map.py
      - The program prompts the user for database(DB) connection parameters:
         - DB Username.
         - DB password.
         - DB Host(default: localhost).
         - DB Port(default: 5432 for PostgreSQL).
         - DB Name.
   2) open terminal in project folder and run command "python -m http.server" or "py -m http.server" and go by link: http://localhost:8000/index.html


## Dataset Source
- The dataset containing the border coordinates of Ukraine was sourced from [geoBoundaries](https://www.geoboundaries.org/), an open database for political administrative boundaries.

**Dataset Details**:
- File format: GeoJSON
- Boundary level: ADM0 (country-level boundary)
  
**Notes**:
- Ensure the dataset file (geoBoundaries-UKR-ADM0.geojson) is placed in the root directory of the project before running the program.

## Program Result
Program Result in border 
![image](https://github.com/user-attachments/assets/e34a6a9e-174d-4ebc-864e-e502cddc4ec0)

Program Result  over the capital and neighboring regions

![output1](https://github.com/user-attachments/assets/6296d3da-0a36-46f8-b377-5c3c2cc7de9d)

Program result over the country

![image](https://github.com/user-attachments/assets/320f2907-e209-47a1-9c13-025560985020)

