# Configure the following settings in your Django project's settings.py file

## Configure the env file

```bash
# core/settings.py
mkdir ~/environments
cd ~/environments
python3 -m venv myenv
```

## Step 2: Activate the Virtual Environment

```bash
source ~/environments/myenv/bin/activate
which python
```

## Step 3: Make the Virtual Environment Persistent

```bash
nano ~/.bashrc
# Add the following line to the end of the file:
source ~/environments/myenv/bin/activate
# Save and close the file
source ~/.bashrc
# Close and exit the terminal and open a new terminal to verify the changes
```

## Preparing the system for hosting

### Using Nginx and Gunicorn for production

### Step 1: Install Nginx and Gunicorn

```bash
sudo apt-get install nginx
sudo apt-get install gunicorn

#Create an Nginx configuration file for your project
sudo nano /etc/nginx/sites-available/smes

#Add the following lines 
    server {
        listen 80;
        server_name 173.249.5.188;
	
        location / {
            proxy_pass http://unix:/run/gunicorn.sock;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;


          # Prevent 504 Gateway Timeout
          keepalive_timeout 10;
          keepalive_requests 1000;

          proxy_connect_timeout 30;
          proxy_send_timeout 30;
          proxy_read_timeout 30;
          send_timeout 30;

          proxy_buffer_size 512k;
          proxy_buffers 64 512k;
          proxy_busy_buffers_size 1024k;

         gzip on;
         gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
         gzip_comp_level 5;

        }

        location /static/ {
            alias /var/www/SMEs/static/;
        }

        location /media/ {
            alias /var/www/SMEs/media/;
        }
    }

#Enable The configuation
sudo ln -s /etc/nginx/sites-available/smes /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx


```
##Configure Gunicorn as a Systemd Service

```Bash
#Create a systemd service to manage Gunicorn:
Create the Service File: 
sudo nano /etc/systemd/system/smes.service

[Unit]
Description=Gunicorn instance to serve SMEs
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/SMEs
Environment="PATH=/root/environments/myenv/bin"
ExecStart=/root/environments/myenv/bin/gunicorn --workers 9 --threads 4 --bind unix:/run/gunicorn.sock core.wsgi:application --timeout 120 --worker-class gthread --keep-alive 5 --max-requests 2000 --max-requests-jitter 100

[Install]
WantedBy=multi-user.target


#Reload and Restart the Service
sudo systemctl daemon-reload
sudo systemctl restart smes
#Check for status
sudo systemctl status smes


```

## Troubleshoot Errors
```Bash
#Check logs for details:
    sudo journalctl -u smes
    sudo tail -f /var/log/nginx/error.log
    sudo tail -f /var/log/nginx/access.log
    cat /var/log/nginx/error.log


```

## Disable the Default Nginx Configuration
```Bash
#The default Nginx configuration file is likely taking precedence. Disable it by removing the symbolic link to the default site:
    sudo rm /etc/nginx/sites-enabled/default

#Ensure Your Project Configuration is Enabled
    sudo ln -s /etc/nginx/sites-available/smes /etc/nginx/sites-enabled
    ls /etc/nginx/sites-enabled/

    sudo nginx -t
    sudo systemctl reload nginx


```

## After Making changes to the system

```Bash
#Restart Gunicorn
After making changes to settings.py, restart the Gunicorn service for the changes to take effect:
    sudo systemctl restart smes

    sudo systemctl restart smes

```


## Configuring Mysql

```Bash
#
sudo apt install mysql-server

sudo mysql -u root -p
CREATE DATABASE smes_db;

CREATE USER 'jataz'@'localhost' IDENTIFIED BY '9965@jay17Freedom';
GRANT ALL PRIVILEGES ON smes_db.* TO 'jataz'@'localhost';
FLUSH PRIVILEGES;

sudo apt update
sudo apt install default-libmysqlclient-dev build-essential


use pymysql pip install pymysql

import in DJango settings
    import pymysql
    pymysql.install_as_MySQLdb()
use pip install cryptography for password The cryptography package is required for secure authentication methods like caching_sha2_password

Cheking errors
sudo tail -f /var/log/mysql/error.log

```
## Configure for multiple users support
```Bash
sudo nano /etc/mysql/my.cnf
[mysqld]
# General settings
max_connections = 1000  # Increased to handle more concurrent users
thread_cache_size = 128
table_open_cache = 5000
table_definition_cache = 4000

# Temporary Table Optimization
tmp_table_size = 512M
max_heap_table_size = 512M

# InnoDB Optimizations
innodb_buffer_pool_size = 4G  # Increased buffer pool for better performance
innodb_buffer_pool_instances = 4  # Improves parallel query execution
innodb_log_file_size = 512M  # Larger log file for heavy transactions
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT
innodb_io_capacity = 2000
innodb_io_capacity_max = 4000
innodb_read_io_threads = 16
innodb_write_io_threads = 16

# Query Performance Optimization
join_buffer_size = 8M
sort_buffer_size = 8M
read_rnd_buffer_size = 8M  # Query cache is deprecated in MySQL 8.0

# Log Slow Queries (Debugging)
slow_query_log = 1
slow_query_log_file = /var/log/mysql-slow.log
long_query_time = 1  # Log queries longer than 1 second

# Connection Timeout (Prevents Long-Held Connections)
wait_timeout = 28800
```

## ALLOW DATABASE CONNECTION OUTSIDE THE LINUX SERVER

```Bash
Configure MySQL to Allow Remote Access
Edit the MySQL Configuration File: Open the MySQL configuration file:
    sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
        Change the bind-address: Look for the line:
            bind-address = 127.0.0.1
            bind-address = 0.0.0.0
    Restart MySQL: Apply the changes by restarting the MySQL service:
        sudo systemctl restart mysql

```


## Check User database if they can connect to the ip address
```Bash

Your MySQL server is blocking remote connections from 173.249.5.188 (your Django server's IP). This is why Django cannot connect, causing the Internal Server Error.

✅ Fix: Allow Remote Access for jataz User
You need to grant the necessary MySQL privileges to allow remote access. Follow these steps:

1️⃣ Log in to MySQL Locally
Since your database server is blocking remote connections, connect to MySQL from the server itself:

bash
    mysql -u root -p

Enter your MySQL root password when prompted.

2️⃣ Check Existing User Permissions
Run:sql

    SELECT user, host FROM mysql.user;

✅ Correct Command for Granting Remote Access
Run the following SQL command without IDENTIFIED BY:

    ALTER USER 'jataz'@'localhost' IDENTIFIED WITH mysql_native_password BY '9965@jay17Freedom';
    CREATE USER 'jataz'@'%' IDENTIFIED WITH mysql_native_password BY '9965@jay17Freedom';
    GRANT ALL PRIVILEGES ON smes_db.* TO 'jataz'@'%' WITH GRANT OPTION;
    FLUSH PRIVILEGES;


✅ This allows your Django server (173.249.5.188) to connect to MySQL.

✅ If jataz Doesn't Exist for Remote Access
If you still get an error, the jataz user may not be set up for remote access. Run:
    CREATE USER 'jataz'@'173.249.5.188' IDENTIFIED WITH mysql_native_password BY '9965@jay17Freedom';
    GRANT ALL PRIVILEGES ON smes_db.* TO 'jataz'@'173.249.5.188';
    FLUSH PRIVILEGES;
✅ This creates the user and allows access from Django’s server.
```

```Bash
✅ Step 4: Enable Caching with Redis
Since your system will serve 10,000+ users, caching reduces database load and speeds up API responses.

1️⃣ Install Redis

sudo apt update
sudo apt install redis-server -y
2️⃣ Configure Redis in Django
1️⃣ Install Redis Python Client:

bash
Copy
Edit
pip install django-redis
2️⃣ Modify settings.py:

python
Copy
Edit
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_TIMEOUT": 5,
            "SOCKET_CONNECT_TIMEOUT": 5,
        }
    }
}
3️⃣ Restart Redis:

bash
Copy
Edit
sudo systemctl restart redis

```