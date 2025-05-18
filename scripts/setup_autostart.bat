@echo off
REM Script para configurar el inicio automático del sistema de gestión de evidencias en Windows

echo Configurando el inicio automático del Sistema de Gestión de Evidencias...

REM Obtener la ruta completa del script de inicio
SET "SCRIPT_PATH=%~dp0start.bat"
SET "SCRIPT_PATH=%SCRIPT_PATH:\=\\%"

REM Crear un archivo XML para la tarea programada
echo ^<?xml version="1.0" encoding="UTF-16"?^> > "%TEMP%\gestor_evidencias_task.xml"
echo ^<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"^> >> "%TEMP%\gestor_evidencias_task.xml"
echo   ^<RegistrationInfo^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<Description^>Inicia automáticamente el Sistema de Gestión de Evidencias al iniciar sesión^</Description^> >> "%TEMP%\gestor_evidencias_task.xml"
echo   ^</RegistrationInfo^> >> "%TEMP%\gestor_evidencias_task.xml"
echo   ^<Triggers^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<LogonTrigger^> >> "%TEMP%\gestor_evidencias_task.xml"
echo       ^<Enabled^>true^</Enabled^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^</LogonTrigger^> >> "%TEMP%\gestor_evidencias_task.xml"
echo   ^</Triggers^> >> "%TEMP%\gestor_evidencias_task.xml"
echo   ^<Principals^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<Principal id="Author"^> >> "%TEMP%\gestor_evidencias_task.xml"
echo       ^<LogonType^>InteractiveToken^</LogonType^> >> "%TEMP%\gestor_evidencias_task.xml"
echo       ^<RunLevel^>HighestAvailable^</RunLevel^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^</Principal^> >> "%TEMP%\gestor_evidencias_task.xml"
echo   ^</Principals^> >> "%TEMP%\gestor_evidencias_task.xml"
echo   ^<Settings^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<MultipleInstancesPolicy^>IgnoreNew^</MultipleInstancesPolicy^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<DisallowStartIfOnBatteries^>false^</DisallowStartIfOnBatteries^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<StopIfGoingOnBatteries^>false^</StopIfGoingOnBatteries^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<AllowHardTerminate^>true^</AllowHardTerminate^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<StartWhenAvailable^>true^</StartWhenAvailable^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<RunOnlyIfNetworkAvailable^>false^</RunOnlyIfNetworkAvailable^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<IdleSettings^> >> "%TEMP%\gestor_evidencias_task.xml"
echo       ^<StopOnIdleEnd^>true^</StopOnIdleEnd^> >> "%TEMP%\gestor_evidencias_task.xml"
echo       ^<RestartOnIdle^>false^</RestartOnIdle^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^</IdleSettings^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<AllowStartOnDemand^>true^</AllowStartOnDemand^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<Enabled^>true^</Enabled^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<Hidden^>false^</Hidden^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<RunOnlyIfIdle^>false^</RunOnlyIfIdle^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<WakeToRun^>false^</WakeToRun^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<ExecutionTimeLimit^>PT0S^</ExecutionTimeLimit^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<Priority^>7^</Priority^> >> "%TEMP%\gestor_evidencias_task.xml"
echo   ^</Settings^> >> "%TEMP%\gestor_evidencias_task.xml"
echo   ^<Actions Context="Author"^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^<Exec^> >> "%TEMP%\gestor_evidencias_task.xml"
echo       ^<Command^>%SCRIPT_PATH%^</Command^> >> "%TEMP%\gestor_evidencias_task.xml"
echo     ^</Exec^> >> "%TEMP%\gestor_evidencias_task.xml"
echo   ^</Actions^> >> "%TEMP%\gestor_evidencias_task.xml"
echo ^</Task^> >> "%TEMP%\gestor_evidencias_task.xml"

REM Registrar la tarea programada
schtasks /create /tn "Sistema Gestor de Evidencias" /xml "%TEMP%\gestor_evidencias_task.xml" /f

IF %ERRORLEVEL% EQU 0 (
    echo Configuración completada. El sistema se iniciará automáticamente al iniciar sesión.
) ELSE (
    echo Error al configurar el inicio automático. Por favor, ejecute este script como administrador.
)

del "%TEMP%\gestor_evidencias_task.xml"
pause 