FROM nginx:1.15.8-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d
COPY ./certs /etc/ssl/certs
COPY ./snippets /etc/nginx/snippets
