#!/usr/bin/env bash

cp -r /vagrant/xbrowse-laptop-downloads/* .

# fix to remove awkward grub confirm window, taken from https://github.com/mitchellh/vagrant/issues/289
apt-get -y remove grub-pc
apt-get -y install grub-pc
grub-install /dev/sda # precaution
update-grub 

apt-get update 
apt-get upgrade -y

# basic system libs
apt-get install -y git vim build-essential

# python
apt-get install -y python-dev python-setuptools
easy_install pip
pip install setuptools --no-use-wheel --upgrade
pip install virtualenv
pip install virtualenvwrapper
source virtualenvwrapper.sh

# set up a virtualenv for xbrowse-server
virtualenv /opt/env

source /opt/env/bin/activate

# postgres 
apt-get install -y libpq-dev postgresql postgresql-contrib 
sudo -u postgres createdb xbrowsedb
sudo -u postgres createuser xbrowseuser --superuser
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE xbrowsedb TO xbrowseuser;"
sudo -u postgres psql -c "ALTER USER xbrowseuser WITH PASSWORD 'password';"
pip install psycopg2

# mongodb
wget http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.4.8.tgz
tar -xzf mongodb-linux-x86_64-2.4.8.tgz
cp mongodb-linux-x86_64-2.4.8/bin/* /usr/local/bin/
mkdir /data
mkdir /data/db

# VEP
apt-get install -y libdbi-perl
tar -xzf variant_effect_predictor.tar.gz
cd variant_effect_predictor
perl INSTALL.pl -a a
cd /home/vagrant

# vep cache dir
tar -xzf vep_cache_dir.tar.gz
rm vep_cache_dir.tar.gz

# all the dependencies are installed; set up supervisord to manage them
apt-get install -y supervisor
cp /vagrant/mongodb.conf /etc/supervisor/conf.d/
supervisorctl reread
sleep 2
# not sure why this is necessary, but mongo doesn't start with supervisorctl restart all
supervisorctl shutdown  
sleep 2
supervisord
sleep 2

# xbrowse code
# only download it if code folder not already there - so you can rebuild VM without error 
if [ ! -d "/vagrant/code" ]; then
	mkdir /vagrant/code
	git clone https://github.com/xbrowse/xbrowse.git /vagrant/code/xbrowse
	git clone https://github.com/xbrowse/xbrowse-web.git /vagrant/code/xbrowse-web
fi
add2virtualenv /vagrant/code/xbrowse

# system libraries required for packages
apt-get install libmysqlclient-dev gfortran libopenblas-dev liblapack-dev libfreetype6-dev libpng-dev -y
# have to install numpy before requirements.txt because of setup.py errors in some random package 
pip install pandas
pip install -r /vagrant/code/xbrowse-web/requirements.txt

#
# set up xbrowse instance
#
mkdir /opt/xbrowse

# reference
cp /vagrant/xbrowse_settings/* /opt/xbrowse/
mongorestore xbrowse_reference

# init xbrowse server
cp /vagrant/local_settings.py /vagrant/code/xbrowse-web/xbrowse_server/
cp -r /vagrant/server_files /home/vagrant/
cp -r /vagrant/xbrowse.sh /home/vagrant/
cd /vagrant/code/xbrowse-web
./manage.py syncdb --noinput
chmod 777 /home/vagrant/database.sqlite
./manage.py migrate --all

#
# At this point the xbrowse instance is set up - now let's actually deploy it
#

# guinicorn
pip install gunicorn
cp /vagrant/gunicorn_config.py .
cp /vagrant/gunicorn.conf /etc/supervisor/conf.d/
supervisorctl reread
supervisorctl shutdown
sleep 5
supervisord

# nginx
apt-get install nginx -y
cp /vagrant/xbrowse_nginx /etc/nginx/sites-available/xbrowse_nginx
ln -s /etc/nginx/sites-available/xbrowse_nginx ln -s /etc/nginx/sites-enabled
rm /etc/nginx/sites-enabled/default 
rm /etc/nginx/sites-available/default 
service nginx restart

# init xbrowse resources
cd /vagrant/code/xbrowse-web
./manage.py rebuild --popfreq

# create user 
source /home/vagrant/xbrowse.sh
python -c """from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"""

# # create xbrowse project 
# ./manage.py add_project 1kg
# ./manage.py add_individuals_to_project 1kg --fam-file /home/vagrant/1kg.ped
# ./manage.py set_vcf 1kg /home/vagrant/1kg.vcf 
# ./manage.py reload 1kg