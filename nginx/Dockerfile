FROM nginx:latest
RUN rm /etc/nginx/conf.d/default.conf
RUN rm /etc/nginx/nginx.conf
COPY etc/nginx.conf.tmp /etc/nginx/
COPY etc/run.sh /bin/
COPY www/* /var/www/
WORKDIR /
