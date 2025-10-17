
import geopandas as gpd
import numpy as np
from libpysal.weights import Queen
from spreg import ML_Lag, ML_Error
import streamlit as st
import pandas as pd
import statsmodels.formula.api as smf
from spreg import OLS


@st.cache_data
def load_data():
    gdf = gpd.read_file("data/gadm41_IDN_2.json")
    gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
    df = pd.read_csv('data/data_jumlah_tbc.csv', sep=';', index_col=0)
    df.index = df.index.str.replace(' ', '', regex=False)

    merged = gdf.merge(df, left_on='NAME_2', right_index=True)
    return merged

data_spatial = load_data()
cols = ["Y", "X1", "X2", "X3", "X4"]
for col in cols:
    data_spatial[col] = (
        data_spatial[col].astype(str)
        .str.replace(",", ".")
        .str.replace("%", "")
    )
    data_spatial[col] = pd.to_numeric(data_spatial[col], errors="coerce")

y = data_spatial["Y"].values.reshape((-1, 1))
X = data_spatial[["X1", "X2", "X3", "X4"]].values

w = Queen.from_dataframe(data_spatial)
w.transform = "r"

# SAR Model
sar_model = ML_Lag(y, X, w=w, method="full")

# OLS Model
formula = 'Y ~ X1 + X2 + X3 + X4'
ols_model = smf.ols(formula, data=data_spatial).fit()

# SEM Model
sem_model = ML_Error(y, X, w=w, name_y='Y', name_x=['X1', 'X2', 'X3', 'X4'])

# with st.container(border=True):
st.subheader('Model dengan AIC terbaik adalah SAR')
c1, c2 = st.columns([1, 1])
c3, c4 = st.columns([1, 1])
with c1:
    with st.container(border=True):
        st.header("Spatial Auto Regression (SAR)")

        st.markdown("##### Model Fit and Diagnostics")
        col1, col2, col3 = st.columns(3)
        # col1.metric("Pseudo R-squared", f"{sar_model.pr2:.4f}")
        col1.metric("AIC", f"{sar_model.aic:.2f}")
        col2.metric("Log-Likelihood", f"{sar_model.logll:.2f}")
        col3.metric("Observations", sar_model.n)

        st.markdown("##### Model Coefficients (β)")

        coeffs = {
            'Variable': sar_model.name_x[:-1],
            'Coefficient': sar_model.betas.flatten()[:-1], # Exclude rho from betas
            'Std. Error': sar_model.std_err.flatten()[:-1],
            'Z_Statistic' : [z[1] for z in sar_model.z_stat[:-1]],
            'Probability': np.array([p for z, p in sar_model.z_stat][:-1]),
        }
        coeffs_df = pd.DataFrame(coeffs).round(4)
        st.dataframe(coeffs_df, use_container_width=True, hide_index=True)

with c3:
    with st.container(border=True):
        st.header('Ordinary Least Square (OLS)')

        st.markdown("##### Model Fit and Diagnostics")
        col1, col2, col3 = st.columns(3)
        col1.metric("AIC", f"{ols_model.aic:.2f}")
        col2.metric("Log-Likelihood", f"{ols_model.llf:.2f}")
        col3.metric("Observations", ols_model.nobs)

        st.markdown("##### Model Coefficients (β)")
        coeffs = {
            'Variabel': ols_model.params.index.tolist(),
            'Coefficient': ols_model.params.values,
            'Std. Error': ols_model.bse.values,
            'Z_Statistic': ols_model.tvalues.values,
            'Probability': ols_model.pvalues.values
        }
        coeffs_df = pd.DataFrame(coeffs).round(4)
        st.dataframe(coeffs_df, use_container_width=True, hide_index=True)

with c2:
    with st.container(border=True):
        st.header("Spatial Error Model (SEM)")

        st.markdown("##### Model Fit and Diagnostics")
        col1, col2, col3 = st.columns(3)
        col1.metric("AIC", f"{sem_model.aic:.2f}")
        col2.metric("Log-Likelihood", f"{sem_model.logll:.2f}")
        col3.metric("Observations", sem_model.n)

        st.markdown("##### Model Coefficients (β)")
        coeffs = {
            'Variable': sar_model.name_x[:-1],
            'Coefficient': sem_model.betas.flatten()[:-1], # Exclude rho from betas
            'Std. Error': sem_model.std_err.flatten()[:-1],
            'Z_Statistic' : [z[1] for z in sem_model.z_stat[:-1]],
            'Probability': np.array([p for z, p in sem_model.z_stat][:-1]),
        }
        coeffs_df = pd.DataFrame(coeffs).round(4)
        st.dataframe(coeffs_df, use_container_width=True, hide_index=True)