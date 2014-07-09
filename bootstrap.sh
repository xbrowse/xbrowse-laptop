#!/usr/bin/env bash

apt-get update 
apt-get upgrade -y

# basic system libs
apt-get install -y git vim build-essential

# python
apt-get install -y python-dev python-setuptools
easy_install pip

# postgres 
apt-get install -y libpq-dev postgresql postgresql-contrib 
sudo -u postgres createdb xbrowsedb
sudo -u postgres createuser xbrowseuser --superuser
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE xbrowsedb TO xbrowseuser;"
sudo -u postgres psql -c "ALTER USER xbrowseuser WITH PASSWORD 'password';"
pip install psycopg2

# mongodb
apt-get install -y mongodb
mkdir -p /data/db

# VEP
apt-get install -y libdbi-perl
cp /vagrant/xbrowse-laptop-downloads/variant_effect_predictor.tar.gz .
tar -xzf variant_effect_predictor.tar.gz
cd variant_effect_predictor
perl INSTALL.pl 
cd /home/vagrant  # go back home

# vep cache dir
cp /vagrant/xbrowse-laptop-downloads/vep_cache_dir.tar.gz .
tar -xzf vep_cache_dir.tar.gz
rm vep_cache_dir.tar.gz

# system libraries required for packages
apt-get install libmysqlclient-dev gfortran libopenblas-dev liblapack-dev libfreetype6-dev libpng-dev -y
# have to install numpy before requirements.txt because of setup.py errors in some random package 
pip install pandas
pip install -r /vagrant/xbrowse/server_requirements.txt

echo "export PYTHONPATH=$PYTHONPATH:/vagrant/xbrowse:/home/vagrant" >> /etc/bash.bashrc

#
# set up xbrowse instance
#

cp /vagrant/xbrowse_settings/* /home/vagrant/
ln -s /vagrant/xbrowse/manage.py .
ln -s /vagrant/xbrowse/wsgi.py .

# guinicorn
pip install gunicorn
cp /vagrant/gunicorn_config.py .

# all the dependencies are installed; set up supervisord to manage them
apt-get install -y supervisor
cp /vagrant/gunicorn.conf /etc/supervisor/conf.d/
supervisorctl reread
supervisorctl reload

# nginx
apt-get install nginx -y
cp /vagrant/xbrowse_nginx /etc/nginx/sites-available/xbrowse_nginx
ln -s /etc/nginx/sites-available/xbrowse_nginx /etc/nginx/sites-enabled
rm /etc/nginx/sites-enabled/default 
rm /etc/nginx/sites-available/default 
service nginx restart


