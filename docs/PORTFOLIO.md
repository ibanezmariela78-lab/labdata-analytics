# LabData Analytics | Ficha profesional del proyecto

**Autora:** Mariela Ibañez  
**Demostración pública:** https://labdata-analytics-gfzd4w5uuaydlhvwezfxtw.streamlit.app/  
**Código fuente:** https://github.com/ibanezmariela78-lab/labdata-analytics

## Resumen ejecutivo

LabData Analytics es una aplicación web interactiva desarrollada en Python que integra preparación, control de calidad, exploración estadística, visualización tridimensional, indicadores de abastecimiento y evaluación predictiva sobre conjuntos de datos sintéticos de laboratorio. El objetivo es demostrar un flujo reproducible de ciencia de datos y análisis de negocio aplicable, conceptualmente, a los sectores químico, farmacéutico y biotecnológico.

## Problemas que aborda

- **Calidad de datos:** detecta registros duplicados, faltantes, fechas inválidas y valores de pH fuera del rango físico.
- **Visibilidad analítica:** permite explorar resultados de ensayo por producto, desviaciones y métricas de proceso.
- **Exploración multivariable:** representa patrones con gráficos de correlación, dispersión 3D y K-means.
- **Abastecimiento:** presenta cantidades de stock, puntos de reposición, valores de inventario y simulación de depósitos.
- **Evaluación de modelos:** compara una regresión Random Forest con un predictor de referencia y publica MAE, RMSE y R².
- **Trazabilidad del procesamiento:** dispone de un pipeline de preparación/carga a PostgreSQL mediante un proceso ETL independiente.

## Arquitectura técnica

```text
Datos sintéticos reproducibles (src/data.py)
     |
     +--> Auditoría del origen (src/quality.py)
     |         |--> Control de nulos, duplicados, fechas y pH
     |
     +--> Limpieza e imputación
                |
                +--> Streamlit / Plotly / scikit-learn (app.py)
                |      Calidad | Estadística | 3D | Inventarios
                |      Predicción | Auditoría ETL
                |
                +--> ETL opcional (src/postgres_etl.py)
                       |
                       +--> PostgreSQL 17 en Docker Compose, local
                              |
                              +--> Consultas SQL (sql/analytics.sql)
```

**Nota:** la aplicación pública utiliza datos en memoria; no se conecta a PostgreSQL local. La base de datos permite mostrar, de forma independiente, una carga transaccional con UPSERT y consultas SQL. No se conectó a una base de Supabase ni a SAP.

## Verificaciones realizadas el 20/10/2026

- **600 muestras sintéticas** generadas, procesadas y cargadas en una instancia PostgreSQL local.
- **12 pruebas unitarias aprobadas** en una instalación Windows con Python y Docker.
- **20 valores de pH faltantes** detectados correctamente en los datos de origen.
- **0 identificadores duplicados** en la generación inicial.
- Aplicación pública activa; pestañas **Predicción** y **Auditoría ETL** comprobadas mediante navegación.
- En la ejecución de referencia, el modelo Random Forest produjo aproximadamente **MAE 2,343; RMSE 3,239; R² 0,05**, por lo que **no se afirma rendimiento predictivo alto**. Estas métricas pertenecen a datos sintéticos de demostración.

## Tecnologías y competencias representadas

Python, Pandas, NumPy, Streamlit, Plotly, scikit-learn, SQL, PostgreSQL, SQLAlchemy, Docker Compose, Git, GitHub y GitHub Actions. Preparación de datos, indicadores de calidad, imputación, análisis exploratorio, aprendizaje automático, comparación con baseline, modelado relacional, carga transaccional, pruebas y publicación web.

## Límites y uso responsable

- El conjunto es **sintético**; no contiene muestras reales, información de pacientes ni datos privados.
- Los límites fuera de especificación y otras reglas son didácticos, **no** especificaciones de laboratorio aprobadas.
- No se afirma cumplimiento **GxP/GMP**, certificación, validación regulatoria ni integración con sistemas SAP.
- Los resultados de machine learning no deben utilizarse para toma de decisiones de laboratorio.
- La instancia PostgreSQL local no es un servicio publicado en Internet.

## Texto breve para CV

**LabData Analytics | Proyecto de Ciencia de Datos para laboratorios**  
Diseño y publicación de un dashboard interactivo en Python/Streamlit para auditoría de calidad de datos, análisis estadístico, visualización 3D, indicadores de inventario y evaluación de modelos predictivos. Implementación de ETL y consultas SQL en PostgreSQL/Docker, pruebas automatizadas y despliegue web. *Datos sintéticos y fines demostrativos.*

## Texto breve para LinkedIn

Desarrollé **LabData Analytics**, un proyecto de portfolio orientado al análisis de datos de laboratorios químicos, farmacéuticos y biotecnológicos. Integra limpieza y auditoría de datos, estadística interactiva, gráficos 3D, análisis de inventarios y evaluación de un modelo predictivo. También incluye un flujo ETL con PostgreSQL y Docker y pruebas automatizadas. Trabaja con datos sintéticos para demostrar el proceso de punta a punta, sin presentarlo como un sistema regulatorio validado.

**Demo:** https://labdata-analytics-gfzd4w5uuaydlhvwezfxtw.streamlit.app/  
**GitHub:** https://github.com/ibanezmariela78-lab/labdata-analytics

---

**Autora y contacto**  
Mariela Ibañez  
Teléfono: +54 11 4058-2174  
GitHub: https://github.com/ibanezmariela78-lab  
LinkedIn: https://ar.linkedin.com/in/mariela-ibanez-quimioinformatica
