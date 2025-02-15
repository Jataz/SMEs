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
        server_name 173.230.133.175;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
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
#Create the Service File: sudo nano /etc/systemd/system/smes.service
[Unit]
Description=Gunicorn instance to serve SMEs
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/SMEs
Environment="PATH=/root/environments/myenv/bin"
ExecStart=/root/environments/myenv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 core.wsgi:application

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
#sudo apt install mysql-server

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

## ALLOW DATABASE CONNECTION OUTSIDE THE LINUX SERVER

```Bash
## Step 3 Mysql optimization
    sudo nano /etc/mysql/my.cnf

    Add the following configuration to your my.cnf file:
        [mysqld]
        # General settings
        max_connections = 1000 # increased to handle more concurrent users
        thread_cache_size = 128 # increased to handle more concurrent users
        table_open_cache = 5000 
        table_definitions_cache = 4000

        #Temporary Table Optimization
        tmp_table_size = 512M
        max_heap_table_size = 512M

        #InnoDB Optimization
        innodb_buffer_pool_size = 4G # increased buffer pool for better performance
        innodb_buffer_pool_instances = 4 # improves parallel query execution
        innodb_log_file_size = 512M # Larger log file for heavy transactions
        innodb_flush_log_at_trx_commit = 2 # increased commit speed
        innodb_flush_method = O_DIRECT # improves write performance
        innodb_io_capacity = 2000 # increased I/O capacity
        innodb_io_capacity_max = 4000 # increased I/O capacity
        innodb_read_io_threads = 16 # improves read performance
        innodb_write_io_threads = 16 # improves write performance


        # Query Performance Optimization
        join_buffer_size = 8M # increased join buffer size
        sort_buffer_size = 8M # increased sort buffer size
        read_rnd_buffer_size = 8M # increased read random buffer size

        # Log Slow Queries (Debuggin)
        slow_query_log = 1
        slow_query_log_file = /var/log/mysql/slow.log
        long_query_time = 1 # increased threshold for slow queries

        # Connection Timeout (Prevents Long Held Connections)
        wait_timeout = 28800 # increased timeout to 30 minutes
        interative_timeout = 28800 # increased interactive timeout to 30 minutes

## step 4 Configure MySQL to Allow Remote Access
    Edit the MySQL Configuration File: Open the MySQL configuration file:
        sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
            Change the bind-address: Look for the line:
    
                bind-address = 0.0.0.0
        Restart MySQL: Apply the changes by restarting the MySQL service:
            sudo systemctl restart mysql
```
