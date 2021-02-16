# Install Databases in Fresh debian 10 image

# Debian 10 - 100Gb disk

sudo apt update -y
sudo apt upgrade -y

# Install utilities
sudo apt-get -y install wget gnupg

# Install PostgreSQL
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql-12

# Create Database User (docker@dockerpass) and testdata database
sudo -u postgres bash -c "psql -c \"CREATE USER docker WITH PASSWORD 'dockerpass';\""
sudo -u postgres bash -c "psql -c \"CREATE DATABASE testdata;\""
sudo -u postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE testdata to docker;\""

sudo systemctl enable postgres

# Install MySQL
cd /tmp
wget https://dev.mysql.com/get/mysql-apt-config_0.8.13-1_all.deb
sudo dpkg -i mysql-apt-config*
# MANUAL STEP ABOVE.  NOT SURE HOW TO AUTOMATE
sudo apt update -y
sudo apt install -y mysql-server
# MANUAL STEP ABOVE.  NOT SURE HOW TO AUTOMATE
sudo systemctl enable mysql

mysql_secure_installation
# MANUAL STEP ABOVE. NOTE SURE HOW TO AUTOMATE
sudo mysql -p # Becomes manual setup process.  Here again, automation needed.

# Creating database, user, and grant 
CREATE DATABASE testdata;
CREATE USER 'docker' IDENTIFIED BY 'dockerpass';
GRANT ALL ON testdata.* TO 'docker';

# Get loading application
