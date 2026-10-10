# DataVision AI — Laboratory Intelligence

Plataforma integral de Ciencia de Datos para laboratorios químicos, farmacéuticos y biotecnológicos.

## Primera entrega: dashboard interactivo
- Datos sintéticos reproducibles de control de calidad.
- Limpieza, valores faltantes e indicadores.
- Análisis estadístico, matriz de correlación y K-means.
- Gráfico 3D interactivo con ejes configurables.
- Exportación CSV y esquema SQL PostgreSQL.

## Ejecutar
```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

## Archivos
- `app.py`: dashboard Streamlit/Plotly.
- `src/data.py`: generación y limpieza.
- `sql/schema.sql`: esquema PostgreSQL.
- `docs/PROJECT_SCOPE.md`: alcance.

## Hoja de ruta
ETL y data warehouse dimensional, Supply Chain, predicción y evaluación, Power BI y publicación web.

**Nota:** datos sintéticos; no reemplaza validaciones regulatorias ni de laboratorio.

## Autoría y contacto
Autora: **Mariela Ibañez**  
Teléfono: **+54 11 4058-2174**  
GitHub: https://github.com/ibanezmariela78-lab  
LinkedIn: https://ar.linkedin.com/in/mariela-ibanez-quimioinformatica
