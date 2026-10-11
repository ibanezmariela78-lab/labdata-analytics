import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from src.data import generate_laboratory_data, clean_laboratory_data
from src.inventory import generate_inventory_data, inventory_kpis
from src.predictive import evaluate_assay_model

st.set_page_config(page_title="LabData Analytics", page_icon="🧪", layout="wide")
st.title("🧪 LabData Analytics")
st.caption("Ciencia de Datos y Business Intelligence para laboratorios | Demostración con datos sintéticos.")

@st.cache_data
def load_data():
    raw = generate_laboratory_data()
    return raw, clean_laboratory_data(raw)

@st.cache_data
def load_inventory():
    return inventory_kpis(generate_inventory_data())

raw, df = load_data()
with st.sidebar:
    st.header("Filtros")
    selected = st.multiselect("Productos", sorted(df["product"].unique()), default=sorted(df["product"].unique()))
    st.caption("Datos sintéticos. No son mediciones reales ni resultados validados.")

filtered = df[df["product"].isin(selected)].copy()
if filtered.empty:
    st.warning("Seleccioná al menos un producto para continuar.")
    st.stop()

quality, stats, clusters, inventory, predictive = st.tabs(["🧪 Calidad", "📊 Estadística", "🔬 Exploración 3D", "📦 Inventarios", "📈 Predicción"])

with quality:
    st.subheader("Control de calidad")
    a, b = st.columns(2)
    a.metric("Muestras", len(filtered))
    b.metric("Fuera de especificación", int(filtered["out_of_spec"].sum()))
    c, d = st.columns(2)
    c.metric("Desviación media", f'{filtered["deviation"].mean():.2f}')
    d.metric("pH faltantes en origen", int(raw["ph"].isna().sum()))
    fig = px.box(filtered, x="product", y="assay_pct", color="product", points="outliers",
                 labels={"product": "Producto", "assay_pct": "Ensayo (%)"})
    fig.update_layout(showlegend=False, margin=dict(l=5, r=5, t=15, b=5))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.download_button("Descargar muestras CSV", filtered.to_csv(index=False).encode("utf-8"),
                       "laboratory_clean.csv", "text/csv")

with stats:
    st.subheader("Estadística descriptiva")
    names = {"temperature_c": "Temperatura (°C)", "ph": "pH",
             "assay_pct": "Ensayo (%)", "deviation": "Desviación"}
    numeric = filtered[list(names)].rename(columns=names)
    st.dataframe(numeric.describe().round(2), use_container_width=True)
    fig = px.imshow(numeric.corr(), text_auto=".2f", zmin=-1, zmax=1,
                    color_continuous_scale="RdBu_r", aspect="auto")
    fig.update_layout(margin=dict(l=5, r=5, t=20, b=5))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Correlación no implica causalidad.")

with clusters:
    st.subheader("Exploración tridimensional")
    features = ["temperature_c", "ph", "assay_pct", "deviation"]
    labels = {"temperature_c": "Temperatura (°C)", "ph": "pH",
              "assay_pct": "Ensayo (%)", "deviation": "Desviación"}
    x = st.selectbox("Eje X", features, index=0, format_func=lambda v: labels[v])
    y = st.selectbox("Eje Y", features, index=1, format_func=lambda v: labels[v])
    z = st.selectbox("Eje Z", features, index=2, format_func=lambda v: labels[v])
    k = st.slider("Cantidad de grupos", 2, 6, 3)
    scaled = StandardScaler().fit_transform(filtered[features])
    filtered["cluster"] = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(scaled).astype(str)
    fig = px.scatter_3d(filtered, x=x, y=y, z=z, color="cluster",
                        labels={**labels, "cluster": "Grupo"},
                        hover_data=["sample_id", "product", "batch"], opacity=0.7)
    fig.update_layout(height=520, margin=dict(l=0, r=0, t=5, b=0),
                      legend_title_text="Grupo")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Agrupamientos exploratorios K-means; no equivalen a categorías regulatorias.")

with inventory:
    st.subheader("Inventarios y abastecimiento")
    st.caption("Simulación conceptual de materiales y producción; sin integración con SAP.")
    stock = load_inventory()
    warehouse = st.selectbox("Depósito", ["Todos"] + sorted(stock["warehouse"].unique().tolist()))
    view = stock if warehouse == "Todos" else stock[stock["warehouse"] == warehouse]
    a, b = st.columns(2)
    a.metric("Registros", len(view))
    b.metric("Bajo punto de reposición", int(view["below_reorder"].sum()))
    st.metric("Valor del stock (ARS)", f'{view["stock_value_ars"].sum():,.0f}')
    grouped = view.groupby("material", as_index=False)["stock_value_ars"].sum()
    fig = px.bar(grouped, x="material", y="stock_value_ars",
                 labels={"material": "Material", "stock_value_ars": "Valor del stock (ARS)"})
    fig.update_layout(margin=dict(l=5, r=5, t=10, b=5))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.download_button("Descargar inventario CSV", view.to_csv(index=False).encode("utf-8"),
                       "inventory_synthetic.csv", "text/csv")


with predictive:
    st.subheader("Modelo predictivo de resultados analíticos")
    st.caption("Regresión Random Forest con división entrenamiento/prueba 75/25. Datos sintéticos, sin validez clínica ni regulatoria.")
    st.info("Las variables usadas son producto, temperatura, pH y objetivo. No se utiliza la desviación ni el indicador fuera de especificación para evitar fuga de información.")
    if len(filtered) < 30:
        st.warning("Se requieren al menos 30 muestras para evaluar el modelo.")
    else:
        @st.cache_data
        def run_model(data):
            return evaluate_assay_model(data)
        metrics, predictions = run_model(filtered)
        st.markdown("**Evaluación en muestras reservadas para prueba**")
        st.dataframe(metrics.round(3), hide_index=True, use_container_width=True)
        fig = px.scatter(predictions, x="Real (%)", y="Predicción (%)",
                         hover_data=["Muestra", "Error absoluto"],
                         title="Valores observados frente a predichos")
        lower = min(predictions["Real (%)"].min(), predictions["Predicción (%)"].min())
        upper = max(predictions["Real (%)"].max(), predictions["Predicción (%)"].max())
        fig.add_shape(type="line", x0=lower, y0=lower, x1=upper, y1=upper,
                      line=dict(color="gray", dash="dash"))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(predictions.round(3), hide_index=True, use_container_width=True)
        st.download_button("Descargar predicciones CSV",
                           predictions.to_csv(index=False).encode("utf-8"),
                           "predicciones_sinteticas.csv", "text/csv")
        st.caption("Comparar siempre contra el modelo de referencia. Un R² bajo o negativo indica rendimiento limitado. Los datos fueron generados artificialmente y pueden no contener patrones predictivos reales.")

st.divider()
st.caption("Autora: Mariela Ibañez | +54 11 4058-2174 | GitHub: ibanezmariela78-lab | LinkedIn: mariela-ibanez-quimioinformatica")
