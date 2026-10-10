import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from src.data import generate_laboratory_data, clean_laboratory_data

st.set_page_config(page_title="DataVision AI | Laboratory Intelligence", page_icon="🧪", layout="wide")
st.title("🧪 DataVision AI — Laboratory Intelligence")
st.caption("Demostración con datos sintéticos; no son mediciones reales ni resultados validados de laboratorio.")

@st.cache_data
def load_data():
    raw = generate_laboratory_data()
    return raw, clean_laboratory_data(raw)

raw, df = load_data()
selected = st.sidebar.multiselect("Productos", sorted(df["product"].unique()), default=sorted(df["product"].unique()))
filtered = df[df["product"].isin(selected)].copy()
if filtered.empty:
    st.warning("Seleccioná al menos un producto.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Muestras", f"{len(filtered):,}")
c2.metric("Fuera de especificación", int(filtered["out_of_spec"].sum()))
c3.metric("Desviación media", f'{filtered["deviation"].mean():.2f}')
c4.metric("pH faltantes en origen", int(raw["ph"].isna().sum()))

left, right = st.columns(2)
with left:
    st.subheader("Control analítico por producto")
    st.plotly_chart(px.box(filtered, x="product", y="assay_pct", color="product", points="outliers"), use_container_width=True)
with right:
    st.subheader("Correlación entre variables")
    numeric = filtered[["temperature_c", "ph", "assay_pct", "deviation"]]
    st.plotly_chart(px.imshow(numeric.corr(), text_auto=".2f", zmin=-1, zmax=1, color_continuous_scale="RdBu_r"), use_container_width=True)

st.subheader("Visualización 3D y agrupamientos")
features = ["temperature_c", "ph", "assay_pct", "deviation"]
a, b, c = st.columns(3)
x = a.selectbox("Eje X", features, index=0)
y = b.selectbox("Eje Y", features, index=1)
z = c.selectbox("Eje Z", features, index=2)
k = st.slider("Clústeres", 2, 6, 3)
scaled = StandardScaler().fit_transform(filtered[features])
filtered["cluster"] = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(scaled).astype(str)
st.plotly_chart(px.scatter_3d(filtered, x=x, y=y, z=z, color="cluster", hover_data=["sample_id", "product", "batch"], opacity=0.75), use_container_width=True)
st.caption("K-means exploratorio: los grupos no equivalen a categorías regulatorias.")

st.subheader("Datos procesados")
st.dataframe(filtered, use_container_width=True)
st.download_button("Descargar CSV procesado", filtered.to_csv(index=False).encode("utf-8"), file_name="laboratory_clean.csv", mime="text/csv")
st.divider()
st.caption("Autora: Mariela Ibañez | Tel: +54 11 4058-2174 | GitHub: ibanezmariela78-lab | LinkedIn: mariela-ibanez-quimioinformatica")
