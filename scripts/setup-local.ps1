# Preparacion local de LabData Analytics (Windows PowerShell)
# No modifica proyectos ni bases Supabase existentes.
$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "No se encontro Docker. Abrir Docker Desktop e instalar/activar Docker Compose."
}
docker info *> $null
if ($LASTEXITCODE -ne 0) {
    throw "Docker Desktop no esta funcionando. Abrilo y espera a que el motor este listo."
}
docker compose version
if ($LASTEXITCODE -ne 0) {
    throw "Tu instalacion de Docker no incluye Docker Compose."
}

if (-not (Test-Path ".env")) {
    $bytes = New-Object byte[] 24
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try {
        $rng.GetBytes($bytes)
    } finally {
        $rng.Dispose()
    }
    $password = [BitConverter]::ToString($bytes).Replace("-", "").ToLowerInvariant()
    Set-Content -Path ".env" -Encoding ascii -Value "LABDATA_POSTGRES_PASSWORD=$password"
    Write-Host "Se creo .env con una clave segura local (no subir a GitHub)."
} else {
    $line = Get-Content ".env" | Where-Object { $_ -match '^LABDATA_POSTGRES_PASSWORD=' } | Select-Object -First 1
    if (-not $line) {
        throw "Existe .env, pero falta LABDATA_POSTGRES_PASSWORD. Agregala al archivo local."
    }
    $password = ($line -split "=", 2)[1].Trim()
    if (-not $password) {
        throw "LABDATA_POSTGRES_PASSWORD esta vacia en .env."
    }
    Write-Host "Usando clave local definida en el archivo .env."
}

Write-Host "Iniciando PostgreSQL independiente en 127.0.0.1:55432..."
docker compose up -d --wait
if ($LASTEXITCODE -ne 0) {
    throw "No se pudo iniciar PostgreSQL. Revisa docker compose ps y docker compose logs postgres."
}

$python = Join-Path (Get-Location).Path ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 -m venv .venv
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        & python -m venv .venv
    } else {
        throw "No se encontro Python 3. Instala Python y volve a ejecutar este script."
    }
    if ($LASTEXITCODE -ne 0) { throw "No se pudo crear el entorno virtual Python." }
}

Write-Host "Instalando dependencias..."
& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Fallo la instalacion de dependencias." }

Write-Host "Ejecutando pruebas..."
& $python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "Las pruebas fallaron; no se realizara la carga de datos." }

$encodedPassword = [System.Uri]::EscapeDataString($password)
$env:LABDATA_DATABASE_URL = "postgresql+psycopg://labdata:$encodedPassword@127.0.0.1:55432/labdata"
Write-Host "Cargando las muestras sinteticas a PostgreSQL..."
& $python -m src.postgres_etl
if ($LASTEXITCODE -ne 0) { throw "Fallo la carga ETL a PostgreSQL." }

Write-Host "Verificando registros en la base..."
docker compose exec -T postgres psql -U labdata -d labdata -c "SELECT COUNT(*) AS muestras FROM laboratory_samples;"
if ($LASTEXITCODE -ne 0) { throw "No se pudo consultar la base." }

Write-Host ""
Write-Host "Preparacion completada. Para abrir el dashboard local:"
Write-Host ".\.venv\Scripts\python.exe -m streamlit run app.py"
Write-Host "La publicacion de Streamlit funciona por separado, sin conectar esta base local."
