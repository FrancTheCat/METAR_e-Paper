# METAR_e-Paper

Enable SPI:

sudo raspi-config
  Interfacing Options -> SPI -> yes

sudo  reboot


Install required packages:

sudo apt-get update

sudo apt-get install python3-pip

sudo apt-get install python3-pil

sudo apt-get install python3-numpy

sudo pip3 install RPi.GPIO

sudo pip3 install spidev


Edit Chrontab (default pi user)

sudo crontab -e

add the following lines after the comment

25 * * * * /home/pi/METAR_e-Paper/code/METAR_e-Paper.py

25 * * * * /home/pi/METAR_e-Paper/code/METAR_e-Paper.py
