FROM redis:latest

ARG REDIS_PORT
ENV REDIS_PORT=${REDIS_PORT}

COPY redis.conf /usr/local/etc/redis/redis.conf

EXPOSE ${REDIS_PORT}

CMD ["sh","-c","redis-server /usr/local/etc/redis/redis.conf --port ${REDIS_PORT}"]