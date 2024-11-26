FROM influxdb:2.7-alpine

# add openssh and clean
RUN apk update \
    && apk add --update openssh \
    && rm -rf /tmp/* /var/cache/apk/*

ENV INFLUX_PORT=8086
ENV LOCAL_IP=127.0.0.1
ENV REMOTE_HOSTNAME=pxl_devbox