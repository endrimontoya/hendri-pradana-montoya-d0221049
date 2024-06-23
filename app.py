import streamlit as st
import folium
import json
from streamlit.components.v1 import html
import pandas as pd

colors_red = [
    "#8B0000",  # Merah paling gelap
    "#B22222",
    "#DC143C",
    "#FF0000",
    "#FF6347",
    "#FF7F50",
    "#FA8072",
    "#F08080",
    "#E9967A",
    "#FFA07A"   # Merah paling pudar
]

# Membaca data GeoJSON
with open('map.geojson') as f:
    geojson_data = json.load(f)

# Mengambil JUMLAH_PEN penduduk
densities = [feature['properties']['JUMLAH_PEN'] for feature in geojson_data['features']]
min_density = min(densities)
max_density = max(densities)

# Fungsi untuk membuat popup untuk setiap fitur
def popup_function(feature):
    density = feature['properties']['JUMLAH_PEN']
    return folium.Popup(f"DESA: {feature['properties']['DESA']} JUMLAH_PEN: {density}", parse_html=True)

# Urutkan fitur berdasarkan JUMLAH_PEN dari tinggi ke rendah
sorted_features = sorted(geojson_data['features'], key=lambda x: x['properties']['JUMLAH_PEN'], reverse=True)

# Buat daftar warna sesuai urutan fitur yang diurutkan
feature_colors = {feature['properties']['DESA']: colors_red[i] for i, feature in enumerate(sorted_features)}

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
        'fillOpacity': 1,
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
html(map_html, height=400)

# Menampilkan judul untuk peta
st.write("Peta dengan skala warna merah berdasarkan JUMLAH_PEN penduduk, dari paling gelap ke paling pudar")

# Membuat DataFrame untuk tabel desa dan JUMLAH_PEN
data = {
    "Nama Desa": [feature['properties']['DESA'] for feature in sorted_features],
    "JUMLAH_PEN": [feature['properties']['JUMLAH_PEN'] for feature in sorted_features],
    "Warna": [feature_colors[feature['properties']['DESA']] for feature in sorted_features]
}

df = pd.DataFrame(data)

# Fungsi untuk mewarnai sel warna
def color_row(row):
    return [f"background-color: {row['Warna']};"] * len(row)

# Menerapkan fungsi pewarnaan ke DataFrame Styler
styled_df = df.style.apply(color_row, axis=1)

# Menampilkan tabel desa dan JUMLAH_PEN di Streamlit
st.write("Tabel Desa dan JUMLAH_PEN Penduduk serta Warna di Peta")
st.dataframe(styled_df)
