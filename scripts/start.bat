@echo off
REM Script para iniciar el sistema de gestión de evidencias en Windows

REM Verificar si Docker está instalado
WHERE docker >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Docker no está instalado. Por favor, instálalo primero.
    pause
    exit /b 1
)

REM Verificar si Docker Compose está instalado
WHERE docker-compose >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Docker Compose no está instalado. Por favor, instálalo primero.
    pause
    exit /b 1
)

REM Comprobar si Docker Desktop está en ejecución
docker info >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Docker Desktop no está en ejecución. Por favor, inicia Docker Desktop primero.
    echo 1. Busca Docker Desktop en el menú inicio
    echo 2. Inicia la aplicación y espera a que se inicialice completamente
    echo 3. Cuando veas el icono de Docker en la barra de tareas, intenta ejecutar este script nuevamente.
    pause
    exit /b 1
)

REM Directorio del proyecto
pushd %~dp0..

REM Verificar si el archivo .env existe, si no, crear a partir de env.example
IF NOT EXIST .env (
    echo Creando archivo .env a partir de env.example...
    copy env.example .env
    echo Por favor, edita el archivo .env con la configuración correcta.
    pause
    exit /b 1
)

REM Iniciar los contenedores en modo detached
echo Iniciando los contenedores Docker...
docker-compose up -d
IF %ERRORLEVEL% NEQ 0 (
    echo Error al iniciar los contenedores Docker. Comprueba los mensajes anteriores.
    pause
    exit /b 1
)

echo Sistema iniciado correctamente. Accede a través de: http://localhost:8000
pause 