# PostgreSQL: carga ETL opcional

La aplicación pública de Streamlit **no necesita PostgreSQL**: sigue usando datos sintéticos en memoria. Este módulo permite demostrar un flujo de carga persistente en una base PostgreSQL propia, sin tocar otros proyectos.

## Preparación local

1. Tener PostgreSQL instalado y crear una base de datos vacía, por ejemplo `labdata`.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Definir la variable de entorno `LABDATA_DATABASE_URL` con una URL PostgreSQL válida. No subir contraseñas ni archivos `.env` a GitHub.
4. Ejecutar `python -m src.postgres_etl`.
5. Ejecutar consultas de `sql/analytics.sql` en PostgreSQL.

Ejemplo de formato de URL (reemplazar los valores localmente):
```text
postgresql+psycopg://USUARIO:CLAVE@localhost:5432/labdata
```

El proceso valida el origen, limpia muestras y ejecuta un UPSERT por `sample_id` dentro de una transacción. Repetir la carga actualiza las mismas muestras sin duplicarlas. El informe de calidad se muestra por consola.

**Limitaciones:** se trata de datos sintéticos y reglas demostrativas, no de un proceso GxP validado. El modelo dimensional en `sql/warehouse.sql` es un diseño inicial independiente; esta primera carga escribe en la tabla operacional `laboratory_samples`.
