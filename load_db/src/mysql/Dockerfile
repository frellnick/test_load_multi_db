FROM mysql:latest

ENV MYSQL_PASSWORD=dockerpass \
    MYSQL_USER=docker \
    MYSQL_DATABASE=testdata \
    MYSQL_ROOT_PASSWORD=dockerpass

# Install dependencies
RUN apt update
RUN apt upgrade -y


# Copy data
COPY $datadir /data

# Copy and Run setup scripts
COPY mysql/scripts /scripts
# RUN /scripts/set_global.sh