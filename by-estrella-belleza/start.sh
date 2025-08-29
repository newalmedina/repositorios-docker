#!/bin/bash
set -e

# PHP-FPM ya se lanza como proceso propio
# Si quieres correrlo con supervisord, no necesitas esta línea

# Iniciar supervisord (cron, queue workers, etc.) en foreground
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf -n

# Mantener el contenedor vivo
# tail -f /var/log/supervisor/*.log
