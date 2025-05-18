#!/bin/bash

# Esperar a que la base de datos esté disponible
echo "Esperando a la base de datos..."
sleep 5

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Ejecutar comando
exec "$@" 