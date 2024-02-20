#!/bin/bash

# Iniciar el servicio cron al iniciar el contenedor
cron -f &

# Iniciar supervisord
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf

RUN chmod -R 777 /root/proyectos-web/www
