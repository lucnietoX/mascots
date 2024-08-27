import sqlite3
import json
import datetime

current_date=datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

conn = sqlite3.connect('animal_fountains.db')
cursor = conn.cursor()

cursor.execute("SELECT DESC_CLASIFICACION, BARRIO, DISTRITO, LATITUD, LONGITUD, DIRECCION_AUX FROM fountains")
fountains = cursor.fetchall()
conn.close()

fountains_list = [
    {
        "desc_clasificacion": row[0],
        "barrio": row[1],
        "distrito": row[2],
        "latitude": row[3],
        "longitude": row[4],
        "direcction_aux": row[5]
    }
    for row in fountains
]

fountains_json = json.dumps(fountains_list)
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animal Fountains Madrid - Map</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <style>
        body {{
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            color: #333;
            position: relative; /* Ensures proper stacking context for the pseudo-element */
        }}

        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://upload.wikimedia.org/wikipedia/commons/f/f6/Main_square_Madrid.jpg') no-repeat center center fixed;
            background-size: cover;
            opacity: 0.5;
            z-index: -1; /* Ensures the background is behind the content */
        }}

        h1 {{
            font-family: 'Roboto', sans-serif;
            margin: 20px 0;
            font-weight: 700;
            font-size: 2rem;
            color: black;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}

        #map {{
            height: 650px;
            width: 96%;
            max-width: 1200px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}

        .leaflet-popup-content {{
            font-size: 1rem;
            font-family: Roboto
            line-height: 1.5;
        }}

        .leaflet-popup-content b {{
            font-size: 1.1rem;
            font-family: Roboto
        }}
    </style>
</head>
<body>

<h1>Map of Animal Fountains in Madrid, Spain</h1>
<h4>{current_date}</h4>

<div id="map"></div>

<script>
    var map = L.map('map').setView([40.416775, -3.703790], 12);

    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }}).addTo(map);

    var fountains = {fountains_json};

    fountains.forEach(function(fountain) {{
        L.marker([fountain.latitude, fountain.longitude])
            .addTo(map)
            .bindPopup(`<b>${{fountain.desc_clasificacion}}</b>
                        <br>Bairro: ${{fountain.barrio}}
                        <br>Distrito: ${{fountain.distrito}}
                        <br>Direção: ${{fountain.direcction_aux}}`);
    }});
</script>

</body>
</html>
"""

# Save HTML
with open("map.html", "w") as file:
    file.write(html_content)
