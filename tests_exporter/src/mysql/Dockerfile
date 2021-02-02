FROM mysql:latest

ENV MYSQL_PASSWORD=dockerpass \
    MYSQL_USER=docker \
    MYSQL_DATABASE=testdata \
    MYSQL_ROOT_PASSWORD=dockerpass

# Copy folder into container - Data must be mounted prior to container creation
COPY scripts/* /docker-entrypoint-initdb.d/

WORKDIR /scripts/