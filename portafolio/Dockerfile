# Dockerfile Apache+PHP
FROM php:8.2-apache


MAINTAINER Newal Medina

# |--------------------------------------------------------------------------
# | Apache mod_rewrite
# |--------------------------------------------------------------------------
# |
# | Enables Apache mod_rewrite.
# |
RUN a2enmod rewrite

# Memory Limit
#RUN echo "memory_limit=800M" > $PHP_INI_DIR/conf.d/memory-limit.ini
RUN echo "memory_limit=-1" > $PHP_INI_DIR/conf.d/memory-limit.ini

# Time Zone
RUN echo "date.timezone=Europe/Madrid" > $PHP_INI_DIR/conf.d/date_timezone.ini

RUN apt-get update \
    && apt-get install -y \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libmcrypt-dev \
    libbz2-dev \
    libzip-dev \
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
    openssl \
    libssl-dev \
    wget \
    zsh \
    libicu-dev \
    libc-client-dev \
    libkrb5-dev \
    libxml2-dev \
    libldap2-dev \
    ruby-dev \
    rubygems \
    nodejs \
    sudo \
    && docker-php-ext-install \
    pdo_mysql \
    mysqli \
    zip \
    bz2 \
    bcmath \
    tidy \
    intl \
    && docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ \
    && docker-php-ext-install gd \
    && docker-php-ext-enable tidy \
    && docker-php-ext-configure imap --with-kerberos --with-imap-ssl \
    && docker-php-ext-install imap \
    && docker-php-ext-install soap \
    && docker-php-ext-install pcntl \
    && docker-php-ext-configure ldap --with-libdir=lib/x86_64-linux-gnu/ \
    && docker-php-ext-install ldap


# Install supervisord
RUN apt-get update && apt-get upgrade -y && apt-get install -y supervisor
# Make supervisor log directory
RUN mkdir -p /var/log/supervisor
COPY --chown=root:root supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN chown -R www-data:www-data /var/www


# Installation of Composer
RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
    php composer-setup.php --install-dir=/usr/local/bin --filename=composer && \
    rm composer-setup.php


# Instalación de cron
RUN apt-get update && apt-get install -y cron

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/laravel-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/laravel-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# # Iniciar el servicio cron al iniciar el contenedor
# CMD ["cron", "-f"]

# # Start supervisord
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]

COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh
CMD ["/usr/local/bin/start.sh"]
