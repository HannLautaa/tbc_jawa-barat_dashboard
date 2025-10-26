import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from utils.LISA import lisa_map, lisa_map_cluster
from utils.Map import create_indo_map

t1, t2 = st.columns(2)
t1.title("Peta Kasus TBC di Jawa Barat")
t2.title('Peta LISA')
@st.cache_data
def load_data():
    df =pd.read_excel('data/Data_prediksi.xlsx', index_col=0)
    df.index = df.index.str.replace(' ', '', regex=False)

    gdf = gpd.read_file('data/gadm41_IDN_2.json')
    gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
    merged = gdf.merge(df, left_on='NAME_2', right_index=True)
    return merged

merged = load_data()

fig, ax = plt.subplots(figsize=(20, 4))

cola, colb = st.columns([1, 1])
with cola:
    with st.container(border=True):
        provinsi = st.multiselect(
            "",
            label_visibility='collapsed',
            options=merged.NAME_2.tolist(),
            placeholder='Pilih Kabupaten / Kota'
        )
        if provinsi:
            merged.plot(ax=ax, color='lightgray', edgecolor='black')
            merged_selected = merged[merged['NAME_2'].isin(provinsi)]
            merged_selected.plot(
                    ax=ax,
                    cmap='YlOrRd',
                    legend=True,
                    column='Y',
                    edgecolor='black',
                    vmin=0,
                    vmax=30000
                )
        else:
                merged.plot(
                    ax=ax,
                    cmap='YlOrRd',
                    legend=True,
                    column='Y',
                    edgecolor='black',
                    vmin=0,
                    vmax=30000
                )
        # ax.set_title('Peta Kasus TBC di Jawa Barat', fontsize=14)
        ax.axis('off')
        # plt.tight_layout()
        st.pyplot(fig)
with colb:
        with st.container(border=True):
            lisa_map()
            st.write("""<div style="text-align: justify;">Local Moran’s I atau LISA berfungsi untuk mendeteksi lokasi-lokasi spesifik yang memiliki pola spasial yang signifikan. 
                Melihat peta yang dihasilkan, dapat dilihat bahwa wilayah barat yang ada di Jawa Barat (Bekasi, Depok, Bogor) dapat dikategorikan sebagai High-High cluster atau hotspot yang mana terdapat kasus TBC yang tinggi. 
                Wilayah selatan dan timur Jawa Barat (Garut dan Tasikmalaya) cenderung membentuk Low-Low Cluster atau coldspot</div>""", unsafe_allow_html=True)

colaa, colbb = st.columns(2)
with colbb:
    with st.expander('Show Cluster'):
        lisa_map_cluster()