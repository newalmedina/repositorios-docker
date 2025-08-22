FROM php:8.2-apache

LABEL maintainer="Newal Medina"

# ----------------------------
# Apache mod_rewrite
# ----------------------------
RUN a2enmod rewrite

# ----------------------------
# PHP Configuration
# ----------------------------
RUN echo "memory_limit=-1" > $PHP_INI_DIR/conf.d/memory-limit.ini \
    && echo "date.timezone=Europe/Madrid" > $PHP_INI_DIR/conf.d/date_timezone.ini

# ----------------------------
# System dependencies
# ----------------------------
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    default-mysql-client \
    libjpeg62-turbo-dev \
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
    libkrb5-dev \
    libxml2-dev \
    libldap2-dev \
    ruby-dev \
    rubygems \
    sudo \
    cron \
    supervisor \
    build-essential \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Compile c-client for IMAP
# ----------------------------
RUN curl -L -o c-client.tar.gz https://www.washington.edu/imap/ftp/c-client.tar.gz \
    && tar -xzf c-client.tar.gz \
    && cd c-client-* \
    && make os=linux \
    && cp c-client.a /usr/lib/ \
    && cp c-client.h /usr/include/ \
    && cd .. && rm -rf c-client* 

# ----------------------------
# PHP Extensions
# ----------------------------
RUN docker-php-ext-install pdo_mysql mysqli zip bz2 bcmath tidy intl soap pcntl \
    && docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ \
    && docker-php-ext-install gd \
    && docker-php-ext-enable tidy \
    && docker-php-ext-configure imap --with-kerberos --with-imap-ssl --with-imap-include=/usr/include/ \
    && docker-php-ext-install imap \
    && docker-php-ext-configure ldap --with-libdir=lib/x86_64-linux-gnu/ \
    && docker-php-ext-install ldap

# ----------------------------
# Node.js 20
# ----------------------------
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Supervisor setup
# ----------------------------
RUN mkdir -p /var/log/supervisor
COPY --chown=root:root supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# ----------------------------
# Composer
# ----------------------------
RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" \
    && php composer-setup.php --install-dir=/usr/local/bin --filename=composer \
    && rm composer-setup.php

# ----------------------------
# Cron setup
# ----------------------------
ADD crontab /etc/cron.d/laravel-cron
RUN chmod 0644 /etc/cron.d/laravel-cron \
    && touch /var/log/cron.log

# ----------------------------
# Startup script
# ----------------------------
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh
CMD ["/usr/local/bin/start.sh"]

# ----------------------------
# Healthcheck
# ----------------------------
HEALTHCHECK --interval=1m --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# ----------------------------
# Set ownership
# ----------------------------
RUN chown -R www-data:www-data /var/www
