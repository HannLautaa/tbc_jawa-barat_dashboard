import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Welcome",
    page_icon="📊",
    layout='wide'
)

st.write("# Dashboard Kasus TBC di Jawa Barat Tahun 2024")
st.sidebar.success("Silahkan pilih section.")
st.markdown("Dashboard ini dibuat dengan tujuan memberikan wawasan terkait TBC dan faktor-faktor pengaruhnya.")
st.markdown('Dengan faktor-faktor sebagai berikut: ')
st.markdown('Y = Jumlah Kasus  \n X1 = Jumlah Puskesmas  \n X2 = Persentase Rumah Tangga yang Memiliki Sumber Air Minum Layak  \n'
'X3 = Persentase Rumah Tangga yang Memiliki Sanitasi Layak  \n X4 = Indeks Kualitas Udara')
@st.cache_data
def get_data():
    return pd.read_csv('data/data_jumlah_tbc.csv', index_col=0, sep=';')
df = get_data()
df = df.sort_index()
cols = ["Y", "X1", "X2", "X3", "X4"]
for col in cols:
    df[col] = (
        df[col].astype(str)
        .str.replace(",", ".")   # fix comma decimals
        .str.replace("%", "")    # remove percent signs
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")
fig = px.histogram(df, x='Y', nbins=20)

# with st.container(border=True):
a, b = st.columns([1, 1])
c1, c2 = st.columns([1, 1])
with a:
    with st.container(border=True):
        st.subheader('Bar Chart')
        st.bar_chart(df['Y'])
with b:
    with st.container(border=True):
        st.subheader('Histogram Jumlah Kasus')
        fig.update_layout(height=360)
        st.plotly_chart(fig, height=500)
with c1:
    with st.container(border=True):
        st.subheader('DataFrame')
        st.dataframe(df)
with c2:
    with st.container(border=True):
        st.subheader('Statistik Deskriptif')
        st.write(df.describe())