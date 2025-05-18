#!/bin/bash

# Script para iniciar el sistema de gestión de evidencias en modo desarrollo local

# Directorio del proyecto
PROJECT_DIR=$(dirname "$(dirname "$(readlink -f "$0")")")
cd "$PROJECT_DIR"

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python -m venv venv
fi

# Activar el entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias si es necesario
if ! pip freeze | grep Django > /dev/null; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
fi

# Verificar si el archivo .env existe, si no, crear a partir de env.example
if [ ! -f .env ]; then
    echo "Creando archivo .env a partir de env.example..."
    cp env.example .env
    echo "Por favor, edita el archivo .env con la configuración correcta."
    exit 1
fi

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate

# Iniciar el servidor de desarrollo
echo "Iniciando servidor de desarrollo..."
python manage.py runserver

# Nota: Para salir presiona CTRL+C 