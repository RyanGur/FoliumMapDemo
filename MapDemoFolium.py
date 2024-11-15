# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 19:35:47 2024

@author: ryang
"""

# Import necessary libraries
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

# Load the CSV data into a DataFrame (replace 'your_data.csv' with your actual file name)
data = pd.read_csv('your_data.csv')

# Check the data (ensure there are columns 'name', 'type', 'latitude', and 'longitude')
print(data.head())

# Define the center of the map (Minneapolis)
map_center = [44.9778, -93.2650]  # Minneapolis coordinates
m = folium.Map(location=map_center, zoom_start=12)

# Function to create a 4 km radius around each point and find nearby locations
def add_points_with_radius(data, map_object, radius_km=4):
    # Create marker clusters for better visualization
    marker_cluster = MarkerCluster().add_to(map_object)
    
    for index, row in data.iterrows():
        point = [row['latitude'], row['longitude']]
        folium.Marker(location=point, popup=row['name'], tooltip=row['type']).add_to(marker_cluster)
        
        # Draw a 4 km circle around each point
        folium.Circle(
            location=point,
            radius=radius_km * 1000,  # converting km to meters
            color="blue",
            fill=True,
            fill_opacity=0.1
        ).add_to(map_object)
        
        # Find and mark nearby locations
        nearby_points = data[(data['latitude'] != row['latitude']) & (data['longitude'] != row['longitude'])]
        for _, nearby_row in nearby_points.iterrows():
            if geodesic(point, [nearby_row['latitude'], nearby_row['longitude']]).km <= radius_km:
                folium.Marker(
                    location=[nearby_row['latitude'], nearby_row['longitude']],
                    popup=nearby_row['name'],
                    icon=folium.Icon(color="green" if nearby_row['type'] == 'farm' else "red")
                ).add_to(map_object)

# Add points with radius circles to the map
add_points_with_radius(data, m)

# Display the map
m
