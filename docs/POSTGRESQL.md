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

## Opción recomendada: PostgreSQL local con Docker

El archivo `compose.yaml` levanta una instancia independiente de PostgreSQL 17, en el puerto local **55432** (solo accesible desde la computadora). No usa Supabase ni modifica otros proyectos.

1. Clonar el repositorio y abrir una terminal en su carpeta.
2. Crear un archivo `.env` local con una contraseña propia (no subirlo a GitHub):

```dotenv
LABDATA_POSTGRES_PASSWORD=REEMPLAZAR_CON_CLAVE_LOCAL_SEGURA
```

3. Iniciar la base:

```bash
docker compose up -d
docker compose ps
```

4. Instalar dependencias de Python y definir `LABDATA_DATABASE_URL` **solo en la terminal**, reemplazando la contraseña por la elegida. En PowerShell:

```powershell
python -m pip install -r requirements.txt
$env:LABDATA_DATABASE_URL = "postgresql+psycopg://labdata:TU_CLAVE@127.0.0.1:55432/labdata"
python -m src.postgres_etl
docker compose exec postgres psql -U labdata -d labdata -c "SELECT COUNT(*) FROM laboratory_samples;"
```

La URL de conexión solo debe guardarse localmente y **nunca** en un commit ni una captura compartida. Si la contraseña tiene caracteres especiales, debe codificarse correctamente para una URL.

Para detener la base sin borrar datos: `docker compose down`. **No ejecutar** `docker compose down -v` si se quieren conservar los registros, porque elimina el volumen de datos.

Esta opción requiere Docker Desktop en funcionamiento. La aplicación de Streamlit seguirá siendo pública y no necesita que tu computadora permanezca encendida.
