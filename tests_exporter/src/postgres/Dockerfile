FROM postgres:latest

ENV POSTGRES_PASSWORD=dockerpass POSTGRES_USER=docker POSTGRES_DB=testdata \
    PGDATA=./data/

# Copy folder into container - Data must be mounted prior to container creation
COPY scripts/* /socker-entrypoint-initdb.d/

ADD data/ ./data/

