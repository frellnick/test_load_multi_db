# Install Databases in Fresh debian 10 image

# Debian 10 - 100Gb disk
# Network firewall rules may be necessary for IP connection:
# Allow TCP/UDP 5432, 3306

BUCKET_NAME=test-assets-1


sudo apt update -y
sudo apt upgrade -y

# Install utilities
sudo apt-get -y install wget gnupg git

# Install PostgreSQL
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql-12

# Create Database User (docker@dockerpass) and testdata database
sudo -u postgres bash -c "psql -c \"CREATE USER docker WITH PASSWORD 'dockerpass';\""
sudo -u postgres bash -c "psql -c \"CREATE DATABASE testdata;\""
sudo -u postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE testdata TO docker;\""
sudo -u postgres bash -c "psql -c \"GRANT pg_read_server_files TO docker;\""
sudo systemctl enable postgresql

# Install MySQL
cd /tmp
wget https://dev.mysql.com/get/mysql-apt-config_0.8.13-1_all.deb
sudo dpkg -i mysql-apt-config*
# MANUAL STEP ABOVE.  NOT SURE HOW TO AUTOMATE
sudo apt update -y
sudo apt install -y mysql-server

# Set root password: dockerpass
# open mysql shell

# Set mysql local infile to true
mysql>SET GLOBAL local_infile = 1;

# MANUAL STEP ABOVE.  NOT SURE HOW TO AUTOMATE
sudo systemctl enable mysql

mysql_secure_installation
# MANUAL STEP ABOVE. NOTE SURE HOW TO AUTOMATE
sudo mysql -p # Becomes manual setup process.  Here again, automation needed.

# Creating database, user, and grant 
CREATE DATABASE testdata;
CREATE USER 'docker' IDENTIFIED BY 'dockerpass';
GRANT ALL ON testdata.* TO 'docker';

# Get loading application & data
cd ~
git clone https://github.com/newnativeabq/docker_tests
sudo mkdir /app
sudo cp -R docker_tests/load_db/src/app/* /app/
sudo mkdir /data
sudo gsutil -m cp -r gs://$BUCKET_NAME/data/* /data/

# Install Python & app dependencies
sudo apt install python3 python3-pip pipenv sudo -y
pip3 install -r /app/requirements.txt

# Setup scripts for automatic updates
sudo mv docker_tests/load_db/build/startup_pull_update.sh /usr/local/bin/startup_pull_update.sh
sudo chmod +x /usr/local/bin/startup_pull_update.sh

# Load Data via app (note: future versions, app can control data update, table deletion, everything)
# Run from root dir
cd /
python3 app/app.py