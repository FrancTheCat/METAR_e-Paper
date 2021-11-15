#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import requests
import textwrap

stationname = "EDDV"
line_spacing = 20
line_length = 43

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("METAR e-Paper")
    
    epd = epd4in2.EPD()
    logging.info("init and Clear")
    epd.init()
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    
    # METAR
    logging.info("Get station METAR")
    response = requests.get('https://tgftp.nws.noaa.gov/data/observations/metar/stations/'+stationname+'.TXT')
    logging.info(response.text)

    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)

    metar = textwrap.wrap(response.text, line_length)
    for index, zeile in enumerate(metar):
        logging.info(zeile)
        y = index * line_spacing
        logging.info(y)
        draw.text((0, y), zeile, font = font18, fill = 0)

    global lines 
    lines = len(metar)

    # TAF
    logging.info("Get station TAF")
    response = requests.get('https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/'+stationname+'.TXT')
    logging.info(response.text)

    draw = ImageDraw.Draw(Himage)

    taf = textwrap.wrap(response.text, 40)
    for index, zeile in enumerate(taf):
        logging.info(zeile)
        y= (lines + 1) * line_spacing + index * line_spacing
        logging.info(y)
        draw.text((0, y), zeile, font = font18, fill = 0)
        
    epd.Clear()
    epd.display(epd.getbuffer(Himage))

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()
