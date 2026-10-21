# 🧪 LabData Analytics

**Plataforma demostrativa de Ciencia de Datos y Business Intelligence para laboratorios químicos, farmacéuticos y biotecnológicos.**

**Demo pública:** https://labdata-analytics-gfzd4w5uuaydlhvwezfxtw.streamlit.app/

Los conjuntos de datos son **100 % sintéticos** y reproducibles. Esta aplicación es un proyecto de portfolio, **no** un LIMS real, un sistema SAP, ni una solución validada para uso regulatorio.

## Funcionalidades

| Sección | Contenido |
| --- | --- |
| 🧪 Calidad | Indicadores de muestras, desviaciones, resultados fuera de especificación, gráficos y CSV |
| 📊 Estadística | Descriptivos y matriz de correlación interactiva |
| 🔬 Exploración 3D | Visualización interactiva y agrupamiento K-means |
| 📦 Inventarios | Stock, reposición, valor de materiales y simulación de abastecimiento |
| 📈 Predicción | Random Forest, comparación con línea base, MAE, RMSE y R² |
| 🛡️ Auditoría ETL | Controles de duplicados, nulos, fechas, pH y reporte CSV |

## Tecnologías

Python, Streamlit, Pandas, NumPy, Plotly, scikit-learn, SQLAlchemy, PostgreSQL y Docker Compose. GitHub Actions ejecuta la suite de pruebas definida en `.github/workflows/tests.yml`.

## Instalación en Windows con Docker Desktop

**Requisitos:** Git, Python 3 y Docker Desktop abierto.

En **PowerShell**:

```powershell
cd $HOME\Desktop
git clone https://github.com/ibanezmariela78-lab/labdata-analytics.git
cd labdata-analytics
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup-local.ps1
.\.venv\Scripts\python.exe -m streamlit run app.py
```

El script crea un archivo `.env` local ignorado por Git, genera una contraseña, inicia **una base aislada** PostgreSQL 17 en `127.0.0.1:55432`, prepara el entorno de Python, ejecuta las pruebas, carga datos sintéticos y verifica los registros. **No conecta ni modifica** las bases de Supabase existentes. Si la carpeta ya está clonada, ingresar a ella y ejecutar `git pull` antes del script.

Para detener PostgreSQL conservando datos: `docker compose down`. Para volver a iniciarlo: `docker compose up -d`. No usar `down -v` si se desean conservar los datos.

## Ejecutar sin Docker

Para explorar el dashboard sin base de datos:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Publicación

La demo de Streamlit Community Cloud se despliega desde este repositorio, rama `main`, archivo de entrada `app.py`. Los cambios enviados a `main` actualizan la demo después de la compilación del servicio. Si fuera necesario configurar el despliegue, usar https://share.streamlit.io/ y seleccionar este repositorio, rama y archivo.

**Importante:** PostgreSQL local **no** se conecta al dashboard público; la demo sigue funcionando con datos sintéticos en memoria. Para publicar una base persistente se necesita un PostgreSQL remoto y configurar credenciales privadas en el proveedor de despliegue.

## Presentación para el portfolio

[Leer la ficha técnica y la descripción profesional para CV y LinkedIn](docs/PORTFOLIO.md).

## Estructura y documentación

- `app.py`: aplicación interactiva.
- `src/data.py`, `src/quality.py`: generación, limpieza y auditoría.
- `src/inventory.py`: inventarios.
- `src/predictive.py`: evaluación predictiva.
- `src/postgres_etl.py`: carga transaccional a PostgreSQL local o remoto autorizado.
- `compose.yaml`: PostgreSQL independiente con Docker.
- `sql/schema.sql`, `sql/analytics.sql`, `sql/warehouse.sql`: SQL operacional y analítico.
- `tests/`: pruebas.
- `docs/POSTGRESQL.md`: instrucciones detalladas.

## Alcance y limitaciones

Las reglas de control son demostrativas y no equivalen a especificaciones GMP/GxP. La evaluación predictiva se realiza sobre datos simulados y sus métricas no acreditan capacidad de predicción en laboratorios reales. El esquema dimensional es inicial; la carga ETL implementada escribe en la tabla operacional.

## Autoría y contacto

**Autora: Mariela Ibañez**

GitHub: https://github.com/ibanezmariela78-lab

LinkedIn: https://ar.linkedin.com/in/mariela-ibanez-quimioinformatica
