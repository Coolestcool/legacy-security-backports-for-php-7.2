# Guía y rollback — PHP 7.2.34

Este repositorio es exclusivamente para **PHP 7.2.34**. Distribuye el
backport de Sury para CVE-2026-109618 y CVE-2026-109619, conservando créditos y
licencias. Coolestcool mantiene la distribución comunitaria, sin atribuirse la
autoría del parche ni representar oficialmente a Sury.

```sh
git clone --branch v0.2.0 https://github.com/Coolestcool/legacy-security-backports-for-php-7.2.git
cd legacy-security-backports-for-php-7.2
sha256sum -c SHA256SUMS

# Comprobar en copias temporales; no modifica las fuentes entregadas.
python3 tools/prepare-source.py /ruta/php-7.2.34
# Aplicar explícitamente a una copia de trabajo respaldada.
python3 tools/prepare-source.py /ruta/php-7.2.34 --apply
```

Se requiere Python 3.8+, patch y espacio temporal escribible. En macOS usar
`shasum -a 256 -c SHA256SUMS`. Los hashes no equivalen a una firma.
Se rechazan otras versiones, hashes alterados, contextos incompatibles y la
aplicación repetida. No usar --force ni ignorar rechazos.

El prerrequisito ZSTR_MAX_LEN está incluido. Se aplica primero cuando faltan
ambas macros; si ambas existen se omite. Una definición parcial se rechaza.

**Modificar las fuentes no modifica PHP en ejecución.** Seguir la
[guía técnica completa](INSTALL.md) para reconstruir los paquetes o imágenes
que correspondan a la revisión instalada, preservando extensiones, bibliotecas,
flags, ABI, arquitectura y configuración.

1. Identificar CLI, CGI, Apache/FPM y contenedores reales; php -v sólo prueba CLI.
2. Respaldar binarios, módulos, extensiones, configuración, permisos e imagen
   anterior; comprobar la restauración en un laboratorio y mantener consola.
3. Probar cada SAPI, sesiones, formularios, subidas y flujos con datos de pruebas.
4. Desplegar con los controles propios del servidor, retirar todos los workers
   antiguos y verificar ejecutables y módulos realmente cargados, HTTP y logs.
5. Si falla un criterio, restaurar paquetes/binarios/configuración e imagen,
   reiniciar los servicios afectados y verificar recuperación. Revertir el
   archivo .patch no revierte binarios ya instalados. No tocar bases de datos.

Es una mitigación para una versión sin soporte, no cobertura de todas las
vulnerabilidades. Cambia la terminación por falta de memoria y desactiva el
seguimiento del progreso de subidas en código. Las subidas normales se prueban
por separado; php.ini puede seguir mostrando upload_progress.enabled=1.
El rollback también restaura la exposición anterior. Las pruebas de falta de
memoria se ejecutan sólo en procesos de laboratorio, nunca contra tráfico real.
CI construye CLI/CGI/FPM y prueba CLI/CGI; no certifica Apache, pools FPM ni todos
los flujos de aplicación. Ver [validación](VALIDATION.md) y [seguridad](../SECURITY.md).
