#!/bin/sh
# Gen keys

if ! [ -f /etc/ssl/certs/nginx-selfsigned.key ];
then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/certs/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj '/CN=craaxkvm.epsevg.es/O=Gesys./C=ES'
fi

if ! [ -f /etc/ssl/certs/dhparam.pem ];
then
    openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
fi

nginx -g "daemon off;"
