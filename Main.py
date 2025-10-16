import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
    layout='wide'
)

st.write("# Dashboard Kasus TBC di Jawa Barat Tahun 2024")
st.sidebar.success("Silahkan pilih section.")
st.markdown("Dashboard ini dibuat dengan tujuan memenuhi nilai mata kuliah Epidem dan Spasial")
@st.cache_data
def get_data():
    return pd.read_csv('data/data_jumlah_tbc.csv', index_col=0, sep=';')
df = get_data()
df = df.sort_index()

cols = ["Y", "X1", "X2", "X3", "X4"]
# data_spatial[cols] = data_spatial[cols].apply(pd.to_numeric, errors="coerce")
for col in cols:
    df[col] = (
        df[col].astype(str)
        .str.replace(",", ".")   # fix comma decimals
        .str.replace("%", "")    # remove percent signs
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

st.bar_chart(df['Y'])
st.subheader('DataFrame')
st.dataframe(df)
st.subheader('Statistik Deskriptif')
st.write(df.describe())