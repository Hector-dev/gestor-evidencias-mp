# Sistema de Gestión de Evidencias - Ministerio Público

<!-- Héctor M. Rodríguez A. -->

Sistema para la gestión, seguimiento y control de evidencias para el Ministerio Público. Permite registrar, clasificar y mantener trazabilidad de la cadena de custodia de evidencias físicas y digitales en procesos judiciales.

## Características

- Autenticación y gestión de usuarios con diferentes niveles de acceso
- Registro detallado de evidencias con información completa
- Seguimiento completo de cadena de custodia con historial de movimientos
- Generación de reportes personalizados y estadísticas
- Respaldos automáticos programados de la base de datos
- Interfaz web intuitiva y responsiva
- Soporte para evidencias físicas y digitales

## Requisitos del Sistema

### Para Despliegue con Docker (Recomendado)
- Docker Engine 19.03.0 o superior
- Docker Compose 1.27.0 o superior
- 2GB RAM mínimo (4GB recomendado)
- 500MB de espacio en disco para la aplicación + espacio para datos

### Para Desarrollo Local
- Python 3.8 o superior
- PostgreSQL 13 o superior
- Pip y virtualenv
- Git
- 2GB RAM mínimo

## Instalación y Configuración

### Usando Docker (Recomendado)

1. Clone el repositorio:
   ```
   git clone https://github.com/ministerio-publico/gestor_evidencias_mp.git
   cd gestor_evidencias_mp
   ```

2. Cree el archivo de variables de entorno:
   ```
   cp env.example .env
   ```

3. Edite el archivo `.env` con su configuración:
   ```
   DEBUG=False
   SECRET_KEY=su_clave_secreta_segura
   ALLOWED_HOSTS=localhost,127.0.0.1,su_dominio.com

   DB_ENGINE=postgresql
   DB_NAME=gestor_evidencias
   DB_USER=usuario_postgres
   DB_PASSWORD=contraseña_segura
   DB_HOST=db
   DB_PORT=5432
   ```

4. Inicie los servicios con Docker Compose:
   ```
   docker-compose up -d
   ```

5. Acceda a la aplicación en: http://localhost:8000

### Instalación Local para Desarrollo

1. Clone el repositorio:
   ```
   git clone https://github.com/ministerio-publico/gestor_evidencias_mp.git
   cd gestor_evidencias_mp
   ```

2. Cree un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instale las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Cree y configure el archivo `.env`:
   ```
   cp env.example .env
   ```
   Luego edite `.env` con su configuración local.

5. Configure la base de datos PostgreSQL:
   - Instale PostgreSQL si no lo tiene
   - Cree una base de datos: `createdb gestor_evidencias`
   - Ajuste los parámetros de conexión en `.env`

6. Ejecute las migraciones:
   ```
   python manage.py migrate
   ```

7. Cree un superusuario:
   ```
   python manage.py createsuperuser
   ```

8. Inicie el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

## Inicio del Sistema

### Métodos de Inicio

Hay varios métodos para iniciar el sistema:

#### 1. Inicio Manual con Docker Compose

```
cd ruta/al/proyecto/gestion_dasti
docker-compose up -d
```

Este método levanta el servidor web y la base de datos PostgreSQL. No es necesario iniciar pgAdmin ni otros servicios adicionales, ya que la base de datos se gestiona automáticamente.

#### 2. Usando Scripts de Inicio (Recomendado)

Para facilitar el inicio del sistema, se incluyen scripts en la carpeta `scripts/`:

##### Para Windows:
- Abra el explorador de archivos y navegue a la carpeta del proyecto
- Vaya a la carpeta `scripts`
- Haga doble clic en `start.bat` para iniciar el sistema con Docker
- Alternativamente, use `start_local.bat` para modo desarrollo

##### Para Linux/Mac:
- Abra una terminal
- Navegue hasta la carpeta scripts: `cd ruta/al/proyecto/gestion_dasti/scripts`
- Ejecute: `./start.sh` (modo Docker) o `./start_local.sh` (modo desarrollo)
- Si es necesario, haga los scripts ejecutables: `chmod +x *.sh`

### Automatización del Inicio

#### En Windows:
Para configurar el inicio automático al arrancar Windows:

1. Navegue a la carpeta `scripts` del proyecto
2. Haga clic derecho en `setup_autostart.bat`
3. Seleccione "Ejecutar como administrador"
4. Se creará una tarea programada que iniciará automáticamente el sistema

#### En Linux:
Para configurar el inicio automático en Linux:

1. Edite el archivo crontab: `crontab -e`
2. Agregue la siguiente línea: `@reboot /ruta/completa/al/proyecto/scripts/start.sh`
3. Guarde y cierre el archivo

## Migración a Otra PC

El sistema está diseñado para ser portable y puede migrarse fácilmente a otro equipo:

1. Requisitos en la nueva PC:
   - Docker y Docker Compose instalados
   - Puertos 8000 y 5432 disponibles (o modificar en docker-compose.yml)

2. Pasos para migrar:
   - Copie toda la carpeta del proyecto a la nueva PC
   - Si desea conservar los datos existentes, realice un respaldo (ver sección Respaldos)
   - En la nueva PC, navegue hasta la carpeta del proyecto
   - Ejecute el script de inicio apropiado para su sistema operativo
   - Si tiene un respaldo, restaure la base de datos

3. Verificación:
   - Acceda a http://localhost:8000 para comprobar que el sistema funciona correctamente
   - Inicie sesión con sus credenciales existentes
   - Verifique que los datos se hayan migrado correctamente si restauró un respaldo

## Respaldo y Restauración

### Crear un Respaldo

Usando el contenedor Docker:

```
docker-compose exec db bash -c 'cd /backups && ./backup.sh'
```

O ejecute el script directamente:

```
cd scripts
./backup.sh
```

Los respaldos se almacenan en el directorio `backups/` con el formato `backup_YYYYMMDD_HHMMSS.sql`.

### Restaurar un Respaldo

```
docker-compose exec db bash -c 'cd /backups && ./restore.sh /backups/nombre_del_archivo_backup.sql'
```

O ejecute el script directamente:

```
cd scripts
./restore.sh ../backups/nombre_del_archivo_backup.sql
```

## Solución de Problemas Comunes

### El sistema no inicia correctamente
1. Verifique que Docker esté instalado y en ejecución
   ```
   docker --version
   docker-compose --version
   ```

2. Asegúrese de tener un archivo `.env` configurado correctamente
   ```
   cat .env  # En Linux/Mac
   type .env  # En Windows
   ```

3. Revise los logs para identificar errores
   ```
   docker-compose logs
   docker-compose logs web  # Solo logs de la aplicación
   docker-compose logs db   # Solo logs de la base de datos
   ```

### Problemas de conexión a la base de datos
1. Verifique que el contenedor de la base de datos esté en ejecución
   ```
   docker-compose ps
   ```

2. Compruebe que las credenciales en `.env` coincidan con las del contenedor de la base de datos

3. Intente reiniciar los servicios
   ```
   docker-compose down
   docker-compose up -d
   ```

### Problemas con los puertos
Si hay conflictos de puertos, edite el archivo `docker-compose.yml` y cambie los puertos mapeados:
```
ports:
  - "nuevo_puerto:8000"  # Para la aplicación web
  - "nuevo_puerto:5432"  # Para PostgreSQL
```

### Para más información
Consulte la documentación detallada en `scripts/info_inicio.md`

## Desarrollo

- Ejecutar tests: `pytest`
- Verificar estilo de código: `flake8`
- Verificar tipos: `mypy .`
- Generar documentación: `cd docs && make html`

# Despliegue en red local con Docker

## 1. Configuración del entorno

Copia el archivo de ejemplo de variables de entorno y edítalo:

```bash
cp env.example .env
```

Edita el archivo `.env` para que contenga:

```
DEBUG=True
SECRET_KEY=tu_clave_secreta_para_desarrollo
ALLOWED_HOSTS=*
DB_ENGINE=postgresql
DB_NAME=gestor_evidencias
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

> **Advertencia:** Usar `ALLOWED_HOSTS=*` solo es seguro en redes locales cerradas. **No uses esto si vas a exponer el sistema a internet.**

## 2. Levantar los servicios

Ejecuta:

```bash
docker compose up --build
```

## 3. Acceso desde otros equipos

Desde cualquier equipo conectado a la misma red local, abre un navegador y accede a:

```
http://<IP_DE_TU_PC>:8000
```

Donde `<IP_DE_TU_PC>` es la dirección IP local del equipo donde se ejecuta Docker (puedes obtenerla con `ipconfig` en Windows).

## 4. Permitir el puerto en el firewall (Windows)

Ejecuta PowerShell como administrador y permite el puerto 8000:

```powershell
New-NetFirewallRule -DisplayName "Django 8000" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

---
<!-- Honrando el trabajo de Héctor M. Rodríguez A. --> 