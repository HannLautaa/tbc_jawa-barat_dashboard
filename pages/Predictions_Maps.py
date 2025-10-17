import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_excel('data/Data_prediksi.xlsx', index_col=0)
    df.index = df.index.str.replace(' ', '', regex=False)
    
    gdf = gpd.read_file('data/gadm41_IDN_2.json')
    gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
    
    merged = gdf.merge(df, left_on='NAME_2', right_index=True)
    return merged

st.title("Peta Prediksi dan Residual Kasus TBC")

merged = load_data()

provinsi = st.multiselect(
    "Pilih Kabupaten / Kota",
    options=merged.NAME_2.tolist(),
)

col, col2 = st.columns([1, 1])
cola, colb = st.columns([1, 1])

with col:
    with st.container(border=True):
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        
        merged.plot(ax=ax1, color='lightgray', edgecolor='black')
        
        if provinsi:
            merged_selected = merged[merged['NAME_2'].isin(provinsi)]
            merged_selected.plot(
                ax=ax1,
                column='Y',
                cmap='YlOrRd',
                legend=True,
                edgecolor='black',
                vmin=-5000,
                vmax=30000
            )
        else:
            merged.plot(
                ax=ax1,
                column='Y',
                cmap='YlOrRd',
                legend=True,
                edgecolor='black',
                vmin=-5000,
                vmax=30000
            )

        ax1.set_title('Peta Kasus TBC Aktual di Jawa Barat', fontsize=14)
        ax1.axis('off')
        st.pyplot(fig1)

with col2:
    with st.container(border=True):
        d = merged.copy()
        d = d[['NAME_2', 'Y', 'Y_prediksi', 'Residual']]
        if provinsi:
            d = d[d['NAME_2'].isin(provinsi)]
        d.rename(columns={'NAME_2': 'Kabupaten/Kota'}, inplace=True)
        d.set_index('Kabupaten/Kota', inplace=True)
        d = d.sort_index()
        st.dataframe(d)

with cola:
    with st.container(border=True):
        fig2, ax2 = plt.subplots(figsize=(10, 4))

        merged.plot(ax=ax2, color='lightgray', edgecolor='black')

        if provinsi:
            merged_selected = merged[merged['NAME_2'].isin(provinsi)]
            merged_selected.plot(
                ax=ax2,
                column='Y_prediksi',
                cmap='YlOrRd',
                legend=True,
                edgecolor='black',
                vmin=-5000,
                vmax=30000
            )
        else:
            merged.plot(
                ax=ax2,
                column='Y_prediksi',
                cmap='YlOrRd',
                legend=True,
                edgecolor='black',
                vmin=-5000,
                vmax=30000
            )
        
        ax2.set_title('Peta Prediksi Kasus TBC di Jawa Barat', fontsize=14)
        ax2.axis('off')
        st.pyplot(fig2)

    
with colb:
    with st.container(border=True):
        fig3, ax3 = plt.subplots(figsize=(10, 4))

        merged.plot(ax=ax3, color='lightgray', edgecolor='black')

        if provinsi:
            merged_selected = merged[merged['NAME_2'].isin(provinsi)]
            merged_selected.plot(
                ax=ax3,
                column='Residual',
                cmap='YlOrRd',
                legend=True,
                edgecolor='black',
                vmin=-5000,
                vmax=30000
            )
        else:
            merged.plot(
                ax=ax3,
                column='Residual',
                cmap='YlOrRd',
                legend=True,
                edgecolor='black',
                vmin=-5000,
                vmax=30000
            )
        
        ax3.set_title('Peta Residual Kasus TBC di Jawa Barat', fontsize=14)
        ax3.axis('off')
        st.pyplot(fig3)

# with st.container(border=True):
#     lisa_map()
#     st.write("""<div style="text-align: justify;">Local Moran’s I atau LISA berfungsi untuk mendeteksi lokasi-lokasi spesifik yang memiliki pola spasial yang signifikan. 
#                 Melihat peta yang dihasilkan, dapat dilihat bahwa wilayah barat yang ada di Jawa Barat (Bekasi, Depok, Bogor) dapat dikategorikan sebagai High-High cluster atau hotspot yang mana terdapat kasus TBC yang tinggi. 
#                 Wilayah selatan dan timur Jawa Barat (Garut dan Tasikmalaya) cenderung membentuk Low-Low Cluster atau coldspot</div>""", unsafe_allow_html=True)