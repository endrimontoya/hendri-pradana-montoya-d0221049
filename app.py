import streamlit as st
import folium
import json
from streamlit.components.v1 import html

# Skema warna merah dari paling gelap ke paling pudar
colors_blue = [
    "#00008B",  # Biru paling gelap
    "#0000CD",
    "#1E90FF",
    "#4169E1",
    "#6495ED",
    "#87CEEB",
    "#ADD8E6",
    "#B0E0E6",
    "#BFEFFF",
    "#CFE2F3"  # Biru paling pudar
]

# Membaca data GeoJSON
with open('map.geojson') as f:
    geojson_data = json.load(f)

# Mengambil kepadatan penduduk
densities = [feature['properties']['KEPADATAN'] for feature in geojson_data['features']]
min_density = min(densities)
max_density = max(densities)

# Fungsi untuk membuat popup untuk setiap fitur
def popup_function(feature):
    density = feature['properties']['KEPADATAN']
    return folium.Popup(f"Nama Desa: {feature['properties']['DESA']} KEPADATAN: {density}", parse_html=True)

# Urutkan fitur berdasarkan kepadatan dari tinggi ke rendah
sorted_features = sorted(geojson_data['features'], key=lambda x: x['properties']['KEPADATAN'], reverse=True)

# Buat daftar warna sesuai urutan fitur yang diurutkan
feature_colors = {feature['properties']['DESA']: colors_blue[i] for i, feature in enumerate(sorted_features)}

# Membuat peta Folium
m = folium.Map()

# Menambahkan data GeoJSON ke peta dengan warna abu-abu dan popup
for feature in sorted_features:
    desa_name = feature['properties']['DESA']
    color = feature_colors[desa_name]
    
    style_function = lambda x, color=color: {
        'fillColor': color,
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7,
    }
    
    geojson_layer = folium.GeoJson(
        feature,
        style_function=style_function,
        popup=popup_function(feature)
    )
    geojson_layer.add_to(m)

# Menyesuaikan peta ke batas data GeoJSON
m.fit_bounds(m.get_bounds())

# Menyimpan peta ke file HTML sementara
m.save('index.html')

# Membaca konten HTML dari file
with open('index.html', 'r', encoding='utf-8') as f:
    map_html = f.read()

# Menampilkan peta di Streamlit menggunakan komponen HTML
html(map_html, height=600)

# Menampilkan judul untuk peta
st.write("Peta dengan skala warna biru berdasarkan kepadatan penduduk, dari paling gelap ke paling pudar")
