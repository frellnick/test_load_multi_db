FROM postgres:latest

ARG datadir=datadir

ENV POSTGRES_PASSWORD=dockerpass \
    POSTGRES_USER=docker \
    POSTGRES_DB=testdata

# Install dependencies
RUN apt update
RUN apt upgrade -y


# Copy data
COPY $datadir /data