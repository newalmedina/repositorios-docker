#!/bin/bash
set -e

# Iniciar PHP-FPM
service php8.2-fpm start

# Iniciar Nginx
service nginx start

# Iniciar supervisord en foreground (maneja cron, queue workers, etc.)
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf -n
