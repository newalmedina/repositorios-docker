# Dockerfile PHP-FPM + Nginx para Laravel Livewire

FROM php:8.2-fpm

MAINTAINER Newal Medina

# Configuración básica de PHP
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    libzip-dev \
    libbz2-dev \
    libxrender1 \
    libfontconfig \
    curl \
    git \
    unzip \
    nano \
    vim \
    bash-completion \
    htop \
    net-tools \
    iproute2 \
    apt-utils \
    gnupg2 \
    libtidy-dev \
    libicu-dev \
    libkrb5-dev \
    libxml2-dev \
    libldap2-dev \
    ruby-dev \
    rubygems \
    sudo \
    supervisor \
    cron \
    nodejs \
    npm \
    && docker-php-ext-install pdo_mysql mysqli zip bz2 bcmath tidy intl soap pcntl \
    && docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ \
    && docker-php-ext-install gd \
    && docker-php-ext-configure ldap --with-libdir=lib/x86_64-linux-gnu/ \
    && docker-php-ext-install ldap

# Configurar zona horaria
RUN ln -sf /usr/share/zoneinfo/Europe/Madrid /etc/localtime \
    && echo "Europe/Madrid" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

# Configuración PHP
RUN echo "memory_limit=-1" >> /usr/local/etc/php/conf.d/custom.ini \
    && echo "post_max_size=8G" >> /usr/local/etc/php/conf.d/custom.ini \
    && echo "upload_max_filesize=8G" >> /usr/local/etc/php/conf.d/custom.ini \
    && echo "date.timezone=Europe/Madrid" >> /usr/local/etc/php/conf.d/custom.ini

# Instalar y configurar OPcache
RUN docker-php-ext-install opcache
RUN echo "opcache.enable=1" >> /usr/local/etc/php/conf.d/opcache.ini \
    && echo "opcache.enable_cli=1" >> /usr/local/etc/php/conf.d/opcache.ini \
    && echo "opcache.memory_consumption=256" >> /usr/local/etc/php/conf.d/opcache.ini \
    && echo "opcache.interned_strings_buffer=16" >> /usr/local/etc/php/conf.d/opcache.ini \
    && echo "opcache.max_accelerated_files=10000" >> /usr/local/etc/php/conf.d/opcache.ini \
    && echo "opcache.revalidate_freq=0" >> /usr/local/etc/php/conf.d/opcache.ini \
    && echo "opcache.validate_timestamps=0" >> /usr/local/etc/php/conf.d/opcache.ini

# Instalación de Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Crear directorio de logs para supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Crear directorio de trabajo y dar permisos
WORKDIR /var/www/html
RUN chown -R www-data:www-data /var/www/html

# Copiar crontab
ADD crontab /etc/cron.d/laravel-cron
RUN chmod 0644 /etc/cron.d/laravel-cron \
    && touch /var/log/cron.log

# Copiar script de inicio
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Nginx
RUN apt-get install -y nginx
COPY default.conf /etc/nginx/conf.d/default.conf

# Exponer puerto HTTP
EXPOSE 80

# Comando de inicio
CMD ["/usr/local/bin/start.sh"]

# Healthcheck
HEALTHCHECK --interval=1m --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
