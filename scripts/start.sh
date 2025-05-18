#!/bin/bash

# Script para iniciar el sistema de gestión de evidencias

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker no está instalado. Por favor, instálalo primero."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose no está instalado. Por favor, instálalo primero."
    exit 1
fi

# Directorio del proyecto
PROJECT_DIR=$(dirname "$(dirname "$(readlink -f "$0")")")
cd "$PROJECT_DIR"

# Verificar si el archivo .env existe, si no, crear a partir de env.example
if [ ! -f .env ]; then
    echo "Creando archivo .env a partir de env.example..."
    cp env.example .env
    echo "Por favor, edita el archivo .env con la configuración correcta."
    exit 1
fi

# Iniciar los contenedores en modo detached
echo "Iniciando los contenedores Docker..."
docker-compose up -d

echo "Sistema iniciado correctamente. Accede a través de: http://localhost:8000" 