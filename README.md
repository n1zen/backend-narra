# Narra Soil Sensor App (BACKEND APP)

This is the backend app for the [**Narra Soil Sensor App**](https://github.com/n1zen/NarraApp)

## MCU-Based Soil Scanner with Machine Learning Application for Finding Locations Suitable for Planting Narra Trees

The MCU-Based Soil Scanner with Machine Learning Application is a system designed to aid conservation groups and community reforestation programs in identifying optimal locations for planting Narra trees (Pterocarpus indicus). Given the ecological significance of Narra trees and the challenges in their growth due to soil unsuitability and deforestation, this project integrates soil scanning technology and artificial intelligence to analyze soil properties and determine areas most suitable for planting.

The system consists of multiple soil sensors (including pH, moisture, and temperature sensors) connected to a microcontroller unit (MCU), which processes the collected data. Using a machine learning model, the system classifies soil quality based on key parameters necessary for Narra tree growth. A user interface (mobile/web app) presents the analyzed data in a user-friendly format, allowing stakeholders to make informed decisions.

The project aims to provide an affordable and accessible solution for sustainable reforestation, reducing the trial-and-error method in tree planting. The PRODelopers conducted research through literature reviews, database and prototype trial, and soil sampling to refine the system's efficiency. Before deployment, the system undergoes multiple tests and validation procedures to ensure accuracy in soil assessment. The results will contribute to future reforestation efforts and environmental conservation strategies.

### Researchers

- Jaylord T. Alipio
- Ace Del Rosario
- Jhon Genesis G. Madera
- [**Thed Justin D. Palting**](https://github.com/TheddySmolBoy)
- [**Louie Izen B. Torres**](https://github.com/n1zen)

## App Details

An app that shows live feedback from soil sensor and access to a database, storing and viewing previous readings.

### Front-End App Developers

- Lead Developer: [**Louie Izen B. Torres**](https://github.com/n1zen)
- Developer: [**Thed Justin D. Palting**](https://github.com/TheddySmolBoy)

### Back-End App Developers

- Lead Developer: [**Louie Izen B. Torres**](https://github.com/n1zen)
- Database Developer: [**Thed Justin D. Palting**](https://github.com/TheddySmolBoy)



# Setup Raspberry Pi

### Follow the following tutorials and repositories

- [**IF WIFI ADAPTER IS NOT "PLUG AND PLAY" WITH RASPBERRY PI**](https://github.com/lwfinger/rtw88)
- [**SETUP RTC**](https://www.youtube.com/watch?v=in6lQ7zES9o)
- [**SETUP RASPAP**](https://www.youtube.com/watch?v=TWvL2C95FEg)

### Install required dependencies

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y mosquitto mosquitto-clients
sudo apt install mariadb-server
sudo mysql_secure_installation
```

## Cloning the Repository

- Clone the repo

```bash
git clone https://github.com/n1zen/backend-narra.git
```
- Go to directory and install dependencies for FastAPI app
```bash
cd backend-narra
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn aiomysql python-dotenv 
```
- Install dependencies for MQTT service
```bash
pip install pyserial paho-mqtt
```
## Setting Up MariaDB

- Login as root user
```bash
sudo mysql -u root -p
```

- Create user
```bash
CREATE USER 'username'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'username'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES
EXIT
```

- login as your username
```bash
mysql -u username -p
```
- create database then exit
```bash
CREATE DATABASE 'database_name';
EXIT;
```
- import cloudtreeDB.sql to your new database
```bash
mysql -u username -p database_name < cloudtreeDB.sql
```

## Setting Up FastAPI App as a Service

- Set FastAPI app for development
```python
async def get_db():
    async with aiomysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("DEV_USER"),
        password=os.getenv("DEV_PASSWORD"),
        db=os.getenv("DEV_DB"),
    ) as conn:
        yield conn

# you'll find the code above on main.py line 13
```

- Set FastAPI app for production
```python
async def get_db():
    async with aiomysql.connect(
        host=os.getenv("HOST"),
        user=os.getenv("PROD_USER"),
        password=os.getenv("PROD_PASSWORD"),
        db=os.getenv("PROD_DB"),
    ) as conn:
        yield conn

# you'll find the code above on main.py line 13
```
- Create .env file
```bash
cd backend-narra
sudo nano .env
```
- Add your env variables
```bash
HOST="host"
PROD_USER="dbusername"
PROD_PASSWORD="dbuser_pass"
PROD_DB="database_name"
DEV_USER="testusername"
DEV_PASSWORD="testuser_pass"
DEV_DB="test_db"
```

- Create service file
```bash
sudo nano /etc/systemd/system/cloudtree_api.service
```
- Add the following to the file
```bash
    [Unit]
    Description=FastAPI application service
    After=network.target

    [Service]
    User=pi
    WorkingDirectory=/home/pi/my_fastapi_app
    ExecStart=/home/pi/my_fastapi_app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
    Restart=always
    RestartSec=5
    StandardOutput=syslog
    StandardError=syslog
    SyslogIdentifier=fastapi_app

    [Install]
    WantedBy=multi-user.target
```
- Reload. Enable. Start
```bash
sudo systemctl daemon-reload
```
```bash
sudo systemctl enable cloudtree_api.service
```
```bash
sudo systemctl start cloudtree_api.service
```

- Check status with this code
```bash
sudo systemctl status cloudtree_api.service
```


## Setting Up MQTT Service

- Create file
```bash
sudo nano /etc/systemd/system/mqtt_sensor.service
```
```bash
[Unit]
Description=MQTT Sensor Publisher Service
After=network.target

[Service]
Type=simple
User=cloudtree
WorkingDirectory=/home/cloudtree/backend-narra
ExecStart=/home/cloudtree/backend-narra/venv/bin/python3 /home/cloudtree/backend-narra/mqtt_sensor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

- Reload systemd and start the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable mqtt_sensor.service
sudo systemctl start mqtt_sensor.service
```

- Check status
```bash
sudo systemctl status mqtt_sensor.service
```


## Setting Up UDP Service

- Do the following:
```bash
sudo nano /etc/systemd/sysyem/broadcaster.service
```
```bash
[Unit]
Description=UDP Broadcaster Service
After=network.target

[Service]
Type=simple
User=cloudtree
WorkingDirectory=/home/cloudtree/backend-narra
ExecStart=/usr/bin/python3 /home/cloudtree/backend-narra/broadcaster.py
Restart=always

[Install]
WantedBy=multi-user.target
```

- Reload systemd and start the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable broadcaster.service
sudo systemctl start broadcaster.service
```
- Check status
```bash
sudo systemctl status broadcaster.service
```
