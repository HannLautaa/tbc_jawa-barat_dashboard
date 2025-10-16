# # import streamlit as st
# # import geopandas as gpd
# # import folium
# # from streamlit_folium import st_folium


# # gdf = gpd.read_file("gadm41_IDN_1.json")

# # # map = folium.Map(location=[-6, 118], zoom_start=4, scrollWheelZoom=False, tiles="cartodbpositron")
# # # folium.GeoJson(gdf, 
# # #                style_function=lambda feature: {
# # #                'fillColor': '#2563eb',
# # #                'color': 'blue',
# # #                'weight': 2,
# # #                'fillOpacity': 0.6,}).add_to(map)
# # # # folium.GeoJson(gdf).add_to(map)
# # # st_map = st_folium(map, width=725, height=500)

# import streamlit as st
# import geopandas as gpd
# import matplotlib.pyplot as plt
# import pandas as pd

# st.title("Peta Indonesia (Static Image)")

# df = pd.read_excel('data.xlsx', index_col=0)
# df.index = df.index.str.replace(' ', '', regex=False)
# mapping = {
#     'KepulauanBangkaBelitung': 'BangkaBelitung',
#     'DKIJakarta': 'JakartaRaya',
#     'DIYogyakarta': 'Yogyakarta'
# }
# df.index = df.index.to_series().replace(mapping)

# gdf = gpd.read_file('gadm41_IDN_1.json')

# provinsi = st.multiselect(
#     "Pilih Provinsi",
#     options=df.index.tolist(), 
#     default=['Aceh']  
# )

# merged = gdf.merge(df, left_on='NAME_1', right_index=True)

# fig, ax = plt.subplots(figsize=(18, 5))

# merged.plot(ax=ax, cmap='YlOrRd', legend=True, column='Angka Penemuan dan Pengobatan TBC 2024 (%)', edgecolor='black')

# ax.set_axis_off()
# plt.tight_layout()

# st.pyplot(fig)

# fig, ax = plt.subplots(1, 1, figsize=(18, 8))

# gdf.plot(ax=ax, edgecolor='k', color='lightgray')
# ax.set_axis_off()
# plt.tight_layout()
# st.pyplot(fig)


def create_indo_map():
    import streamlit as st
    import pandas as pd
    import geopandas as gpd
    import matplotlib.pyplot as plt

    st.title("Peta Kasus TBC di Indonesia")

    df = pd.read_excel('data/data.xlsx', index_col=0)
    df.index = df.index.str.replace(' ', '', regex=False)
    mapping = {
        'KepulauanBangkaBelitung': 'BangkaBelitung',
        'DKIJakarta': 'JakartaRaya',
        'DIYogyakarta': 'Yogyakarta'
    }
    df.index = df.index.to_series().replace(mapping)

    gdf = gpd.read_file('data/gadm41_IDN_1.json')

    provinsi = st.multiselect(
        "Pilih Provinsi",
        options=df.index.tolist(),
        # default=['Aceh']
    )

    merged = gdf.merge(df, left_on='NAME_1', right_index=True)

    fig, ax = plt.subplots(figsize=(18, 5))

    cols = st.columns(1)
    for col in cols:
        with col:
            with st.container(border=True):

                if provinsi:    
                    merged.plot(ax=ax, color='lightgray', edgecolor='black')

                    merged_selected = merged[merged['NAME_1'].isin(provinsi)]
                    merged_selected.plot(
                        ax=ax,
                        cmap='YlOrRd',
                        legend=True,
                        column='Angka Penemuan dan Pengobatan TBC 2024 (%)',
                        edgecolor='black'
                    )
                else:
                    merged.plot(
                        ax=ax,
                        cmap='YlOrRd',
                        legend=True,
                        column='Angka Penemuan dan Pengobatan TBC 2024 (%)',
                        edgecolor='black'
                    )

                ax.set_axis_off()
                plt.tight_layout()

                st.pyplot(fig)

if __name__ == '__main__':
    create_indo_map()