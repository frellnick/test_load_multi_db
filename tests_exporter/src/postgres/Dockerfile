FROM postgres:latest

ENV POSTGRES_PASSWORD=dockerpass POSTGRES_USER=docker POSTGRES_DB=testdata

# Copy folder into container - Data must be mounted prior to container creation
COPY scripts/* /docker-entrypoint-initdb.d/
