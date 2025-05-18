#!/bin/bash

# Verificar si se proporcionó un archivo de backup
if [ $# -eq 0 ]; then
  echo "Error: No se proporcionó archivo de backup para restaurar."
  echo "Uso: restore.sh /backups/backup_file.sql"
  exit 1
fi

BACKUP_FILE=$1
DB_HOST="db"
DB_PORT="5432"

# Verificar si el archivo existe
if [ ! -f "$BACKUP_FILE" ]; then
  echo "Error: El archivo de backup $BACKUP_FILE no existe."
  exit 1
fi

echo "Restaurando backup desde $BACKUP_FILE..."

# Restaurar backup
pg_restore -h ${DB_HOST} -p ${DB_PORT} -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c ${BACKUP_FILE}

# Comprobar resultado
if [ $? -eq 0 ]; then
  echo "Restauración completada exitosamente."
else
  echo "Error al restaurar el backup."
  exit 1
fi 