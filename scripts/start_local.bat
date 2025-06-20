@echo off
REM Script para iniciar el sistema de gestión de evidencias en modo desarrollo local para Windows

REM Directorio del proyecto
pushd %~dp0..

REM Verificar si el entorno virtual existe
IF NOT EXIST venv (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar el entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate

REM Verificar e instalar setuptools (necesario para pkg_resources)
pip show setuptools >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Instalando setuptools...
    pip install setuptools
)

REM Instalar dependencias si es necesario
pip freeze | findstr Django >nul
IF %ERRORLEVEL% NEQ 0 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

REM Verificar si el archivo .env existe, si no, crear con valores por defecto
IF NOT EXIST .env (
    echo Creando archivo .env con configuración para desarrollo local...
    echo DEBUG=True > .env
    echo SECRET_KEY=django-insecure-key-for-development-only >> .env
    echo ALLOWED_HOSTS=localhost,127.0.0.1 >> .env
    echo DB_ENGINE=postgresql >> .env
    echo DB_NAME=gestor_evidencias >> .env
    echo DB_USER=postgres >> .env
    echo DB_PASSWORD=password >> .env
    echo DB_HOST=localhost >> .env
    echo DB_PORT=5432 >> .env
)

REM Verificar PostgreSQL
echo Verificando conexión a PostgreSQL...
python -c "import psycopg2; conn = psycopg2.connect(dbname='postgres', user='postgres', password='password', host='localhost', port='5432'); conn.close()" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ADVERTENCIA: No se pudo conectar a PostgreSQL.
    echo.
    echo Por favor, asegúrate de que PostgreSQL esté instalado y funcionando:
    echo.
    echo 1. Descarga PostgreSQL desde https://www.postgresql.org/download/windows/
    echo 2. Durante la instalación:
    echo    - Usa el usuario 'postgres'
    echo    - Establece la contraseña como 'password' (o actualiza el archivo .env)
    echo    - Mantén el puerto predeterminado 5432
    echo.
    echo 3. Después de la instalación, crea la base de datos:
    echo    - Abre pgAdmin (viene con PostgreSQL)
    echo    - Conéctate al servidor local
    echo    - Crea una nueva base de datos llamada 'gestor_evidencias'
    echo.
    echo Presiona cualquier tecla para continuar cuando hayas instalado PostgreSQL...
    pause
)

REM Crear la base de datos si no existe
echo Creando base de datos si no existe...
python -c "import psycopg2; try: conn = psycopg2.connect(dbname='postgres', user='postgres', password='password', host='localhost', port='5432'); conn.autocommit = True; cur = conn.cursor(); cur.execute(\"SELECT 1 FROM pg_database WHERE datname='gestor_evidencias'\"); exists = cur.fetchone(); conn.close(); conn = psycopg2.connect(dbname='postgres', user='postgres', password='password', host='localhost', port='5432') if not exists else None; if conn: conn.autocommit = True; cur = conn.cursor(); cur.execute('CREATE DATABASE gestor_evidencias'); cur.close(); conn.close(); print('Base de datos creada.') except Exception as e: print(f'Error: {e}')" 2>nul

REM Aplicar migraciones
echo Aplicando migraciones...
python manage.py migrate

REM Iniciar el servidor de desarrollo
echo Iniciando servidor de desarrollo...
python manage.py runserver

REM Nota: Para salir presiona CTRL+C 