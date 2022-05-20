FROM nginx:1.21-alpine

RUN apk update \
    && apk add openssl

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d
COPY ./snippets /etc/nginx/snippets
COPY ./entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
