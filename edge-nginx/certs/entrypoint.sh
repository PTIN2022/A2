# Gen keys

if ! [ -f ./nginx-selfsigned.key ];
then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./nginx-selfsigned.key -out ./nginx-selfsigned.crt -subj '/CN=craaxkvm.epsevg.es/O=Gesys./C=ES'
fi

if ! [ -f ./dhparam.pem ];
then
    openssl dhparam -out ./dhparam.pem 2048
fi

nginx -g daemon off
