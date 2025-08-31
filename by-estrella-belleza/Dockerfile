# Usar PHP-FPM 8.2
FROM php:8.2-fpm

MAINTAINER Newal Medina

# Instalar Apache + extensiones PHP necesarias
RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-proxy-fcgi \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    libzip-dev \
    unzip \
    git \
    curl \
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
    libxml2-dev \
    libldap2-dev \
    ruby-dev \
    rubygems \
    sudo \
    cron \
    nodejs \
    && docker-php-ext-install \
        pdo_mysql \
        mysqli \
        zip \
        bz2 \
        bcmath \
        tidy \
        intl \
        soap \
        pcntl \
        ldap \
        gd \
        opcache \
    && docker-php-ext-configure gd --with-freetype --with-jpeg

# Habilitar mod_proxy_fcgi en Apache
RUN a2enmod proxy_fcgi setenvif \
    && a2enconf php8.2-fpm

# Configurar zona horaria
RUN ln -sf /usr/share/zoneinfo/Europe/Madrid /etc/localtime \
    && echo "Europe/Madrid" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

# Crear directorios y permisos
RUN mkdir -p /var/www/html && chown -R www-data:www-data /var/www

WORKDIR /var/www/html

# Copiar configuraciones personalizadas
COPY docker-php-opcache.ini /usr/local/etc/php/conf.d/
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY crontab /etc/cron.d/laravel-cron
COPY start.sh /usr/local/bin/start.sh

RUN chmod +x /usr/local/bin/start.sh \
    && chmod 0644 /etc/cron.d/laravel-cron \
    && touch /var/log/cron.log

# Instalar Composer
RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" \
    && php composer-setup.php --install-dir=/usr/local/bin --filename=composer \
    && rm composer-setup.php

# Exponer puerto y CMD
EXPOSE 80
CMD ["/usr/local/bin/start.sh"]

# Healthcheck
HEALTHCHECK --interval=1m --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
