# Usa la imagen base oficial de Nginx Proxy Manager
FROM jc21/nginx-proxy-manager:latest

# Crea los directorios necesarios dentro del contenedor
RUN mkdir -p /data /etc/letsencrypt

# Establece el directorio de trabajo
WORKDIR /app

# Establece el usuario adecuado (si es necesario)
USER root

# Expone los puertos (en caso de que quieras hacer la exposición explícita en el Dockerfile)
EXPOSE 81 443

# Comando por defecto
CMD ["npm", "start"]
