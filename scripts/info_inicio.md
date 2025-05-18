# Instrucciones de Inicio - Sistema de Gestión de Evidencias

## Inicio con Docker (Recomendado)

### Inicio Manual

1. Asegúrese de tener Docker y Docker Compose instalados en su sistema.
2. Abra una terminal (PowerShell/CMD en Windows o Terminal en Linux/Mac).
3. Navegue hasta el directorio del proyecto: `cd ruta/al/proyecto/gestion_dasti`
4. Ejecute el comando: `docker-compose up -d`
5. Acceda al sistema a través de su navegador web en: http://localhost:8000

### Inicio Automatizado

#### En Windows:
1. Vaya a la carpeta `scripts` dentro del directorio del proyecto.
2. Haga doble clic en `start.bat` para iniciar el sistema.
3. Para configurar el inicio automático con el arranque del sistema:
   - Haga clic derecho en `setup_autostart.bat` y seleccione "Ejecutar como administrador".
   - Siga las instrucciones en pantalla.

#### En Linux/Mac:
1. Abra una terminal.
2. Navegue hasta la carpeta scripts: `cd ruta/al/proyecto/gestion_dasti/scripts`
3. Ejecute el script de inicio: `./start.sh`
4. Para hacer que el script sea ejecutable: `chmod +x start.sh`

## Inicio en Modo Desarrollo Local

### En Windows:
1. Vaya a la carpeta `scripts` dentro del directorio del proyecto.
2. Haga doble clic en `start_local.bat`.

### En Linux/Mac:
1. Abra una terminal.
2. Navegue hasta la carpeta scripts: `cd ruta/al/proyecto/gestion_dasti/scripts`
3. Ejecute el script de inicio local: `./start_local.sh`
4. Para hacer que el script sea ejecutable: `chmod +x start_local.sh`

## Solución de Problemas

### El sistema no inicia correctamente:
1. Verifique que Docker esté instalado y en ejecución.
2. Asegúrese de tener un archivo `.env` configurado correctamente en la raíz del proyecto.
3. Revise los logs con: `docker-compose logs`

### Problemas con el archivo .env:
1. Si no existe el archivo `.env`, copie el archivo `env.example` y renómbrelo a `.env`.
2. Edite el archivo `.env` y configure las variables de entorno según su entorno.

### Problemas con los puertos:
- Si el puerto 8000 está en uso, puede cambiarlo en el archivo `docker-compose.yml`.
- Si el puerto 5432 (PostgreSQL) está en uso, puede cambiarlo en el archivo `docker-compose.yml`. 