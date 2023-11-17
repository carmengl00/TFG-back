#!/bin/bash
envsubst '$$SERVER_NAME ' < /etc/nginx/nginx.conf.tmp > /etc/nginx/nginx.conf &&
nginx -g "daemon off;"
