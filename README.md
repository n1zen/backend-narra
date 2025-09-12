# Narra Soil Sensor App (BACKEND APP)

This is the backend app for the [**Narra Soil Sensor App**](https://github.com/n1zen/NarraApp)

## MCU-Based Soil Scanner with Machine Learning Application for Finding Locations Suitable for Planting Narra Trees

The MCU-Based Soil Scanner with Machine Learning Application is a system designed to aid conservation groups and community reforestation programs in identifying optimal locations for planting Narra trees (Pterocarpus indicus). Given the ecological significance of Narra trees and the challenges in their growth due to soil unsuitability and deforestation, this project integrates soil scanning technology and artificial intelligence to analyze soil properties and determine areas most suitable for planting.

The system consists of multiple soil sensors (including pH, moisture, and temperature sensors) connected to a microcontroller unit (MCU), which processes the collected data. Using a machine learning model, the system classifies soil quality based on key parameters necessary for Narra tree growth. A user interface (mobile/web app) presents the analyzed data in a user-friendly format, allowing stakeholders to make informed decisions.

The project aims to provide an affordable and accessible solution for sustainable reforestation, reducing the trial-and-error method in tree planting. The developers conducted research through literature reviews, database and prototype trial, and soil sampling to refine the system's efficiency. Before deployment, the system undergoes multiple tests and validation procedures to ensure accuracy in soil assessment. The results will contribute to future reforestation efforts and environmental conservation strategies.

### Researchers

- Jaylord T. Alipio
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

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y mosquitto mosquitto-clients
sudo apt install mariadb-server
sudo mysql_secure_installation
```


# Setting Up MariaDB

> Work in progress...


# Cloning the Repository

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


# Setting Up FastAPI App as a Service

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


# Setting Up MQTT Service

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


# Setting Up UDP Service

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