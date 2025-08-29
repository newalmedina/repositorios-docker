#!/bin/bash
set -e

# Iniciar supervisord (cron, queue workers, etc.) en foreground
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf -n
