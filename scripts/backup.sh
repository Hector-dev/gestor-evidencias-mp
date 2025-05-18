#!/bin/bash

# Variables
BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}.sql"
DB_HOST="localhost"
DB_PORT="5432"

# Asegurar que existe el directorio de backup
mkdir -p ${BACKUP_DIR}

# Crear backup
echo "Creando backup en ${BACKUP_FILE}..."
pg_dump -h ${DB_HOST} -p ${DB_PORT} -U ${POSTGRES_USER} -d ${POSTGRES_DB} -F c -f ${BACKUP_FILE}

# Comprobar resultado
if [ $? -eq 0 ]; then
  echo "Backup completado exitosamente."
  
  # Eliminar backups más antiguos de 30 días
  find ${BACKUP_DIR} -name "backup_*.sql" -type f -mtime +30 -delete
  echo "Backups antiguos eliminados."
else
  echo "Error al crear el backup."
fi 