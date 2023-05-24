sudo python3.7 /home/tc/startup.py
echo 'Installing Django'
#Offline Install
sudo -H pip3 install /home/tc/djangoinstall/Django-2.1.5.tar.gz
#Online Django Install
#sudo pip3.7 install --upgrade --no-deps --force-reinstall django
echo 'Starting sshreader and Django Web server'
cd /home/tc/
/usr/local/bin/python3.7 sshreader.py &
cd RESTtoweraccess
/usr/local/bin/python3.7 manage.py runserver 0.0.0.0:8000
