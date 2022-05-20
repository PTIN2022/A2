FROM nginx:1.21-alpine

RUN apk update \
    && apk add openssl

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d
COPY ./certs /etc/ssl/certs
COPY ./snippets /etc/nginx/snippets

WORKDIR /etc/ssl/certs
CMD ./generate.sh
CMD ["nginx", "-g", "daemon off;"]
