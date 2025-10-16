def lisa_map():
    import streamlit as st
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import pandas as pd
    from libpysal.weights import Queen
    from esda import Moran_Local

    gdf = gpd.read_file("data/gadm41_IDN_2.json")
    gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
    df = pd.read_csv('data/data_jumlah_tbc.csv', sep=';', index_col=0)
    df.index = df.index.str.replace(' ', '', regex=False)

    merged = gdf.merge(df, left_on='NAME_2', right_index=True)

    y = merged["Y"].values

    w = Queen.from_dataframe(merged)
    w.transform = 'r'
    moran_loc = Moran_Local(y, w)

    merged["LISA"] = moran_loc.Is

    fig, ax = plt.subplots(1, 1, figsize=(20, 4))
    merged.plot(
        column="LISA",
        cmap="RdYlBu",
        legend=True,
        vmin=-1, 
        vmax=1,
        ax=ax
        )
    merged.boundary.plot(ax=ax, color="black", linewidth=0.5)
    
    ax.set_title("Peta LISA Kasus TBC di Jawa Barat", fontsize=14)
    ax.axis("off")
    st.pyplot(fig)


    # c, _ = st.columns([1, 1])
    # with c:
        # with st.container(border=True):
        #     merged.plot(
        #         column="LISA",
        #         cmap="RdYlBu",
        #         legend=True,
        #         vmin=-1, 
        #         vmax=1,
        #         ax=ax
        #     )
        #     merged.boundary.plot(ax=ax, color="black", linewidth=0.5)

        #     ax.set_title("Peta LISA Kasus TBC di Jawa Barat", fontsize=14)
        #     ax.axis("off")
        #     st.pyplot(fig)

if __name__ == '__main__':
    lisa_map()