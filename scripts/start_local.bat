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

REM Instalar dependencias si es necesario
pip freeze | findstr Django >nul
IF %ERRORLEVEL% NEQ 0 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

REM Verificar si el archivo .env existe, si no, crear a partir de env.example
IF NOT EXIST .env (
    echo Creando archivo .env a partir de env.example...
    copy env.example .env
    echo Por favor, edita el archivo .env con la configuración correcta.
    pause
    exit /b 1
)

REM Aplicar migraciones
echo Aplicando migraciones...
python manage.py migrate

REM Iniciar el servidor de desarrollo
echo Iniciando servidor de desarrollo...
python manage.py runserver

REM Nota: Para salir presiona CTRL+C 