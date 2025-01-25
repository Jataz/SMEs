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

```