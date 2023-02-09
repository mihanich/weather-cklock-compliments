# Literary Clock
This project uses a Raspberry Pi Zero WH, a microSDHC card, and a Waveshare 7.5 inch e-Paper display HAT 800x480 to make a clock that displays the time using quotes from books, today's date, a weather icon, and the high and low temperatures.

This project heavily adapted and borrowed from multiple sources and is indebted to the following projects specifically:
- [Jake Krajewski's Raspberry Pi + e-Paper Tutorial](https://medium.com/swlh/create-an-e-paper-display-for-your-raspberry-pi-with-python-2b0de7c8820c)
- [Mendhak's Waveshare e-Paper Display](https://github.com/mendhak/waveshare-epaper-display)
- [Jaap Meijers's Instructables Kindle Literary Clock](https://www.instructables.com/Literary-Clock-Made-From-E-reader/)
- [Dhole's Monochrome Weather Icons](https://github.com/Dhole/weather-pixel-icons)
- [Google Fonts](https://fonts.google.com)

I borrowed the weather source code from Mendhak's repo. Jake Krajewski's Medium post showed me that writing to the screen with Python Pillow was easy to do. Jaap Meijers's project provided the quotes and code I modified to generate the quotes. I used Dhole's weather icons to display weather. I used Google Fonts to find good fonts (Literata is apparently designed for displays).

![example](example.png)


- [Shopping list](#shopping-list)
- [Setup the PI](#setup-the-pi)
- [Setup dependencies](#setup-dependencies)
- [Using this application](#using-this-application)
- [Pick a Weather provider](#pick-a-weather-provider)
  - [OpenWeatherMap](#openweathermap)
- [Run it](#run-it)
- [Troubleshooting](#troubleshooting)
- [Waveshare documentation and sample code](#waveshare-documentation-and-sample-code)


## Shopping list

- Waveshare 7.5 inch e-Paper display HAT 800x480 (I think this is the V2 display) 
- Raspberry Pi Zero WH (presoldered header. You don't have to get a presoldered header, but I don't have a soldering iron)
- microSDHC card (I used a Samsung EVO 32GB card but probably any microSDHC card will do)

## Setup the PI

### Prepare the Pi

I tried to follow Mendhak's [post with instructions to prepare the Raspberry Pi with WiFi and SSH](https://code.mendhak.com/prepare-raspberry-pi/), but the instructions didn't work for me entirely for `ssh` and WiFi setup. I followed [the steps for the `ssh` and WiFi in this guide from the Instructables website](https://www.instructables.com/Install-and-Setup-Raspbian-Lite-on-Raspberry-Pi-3/). I also had to switch to a Linux machine instead of my Windows machine to finish the `ssh` and WiFi setup after I could not get it working on Windows 10.


### Connect the display

The Waveshare display I received came with standoffs that were too small to attach the display HAT to the Raspberry Pi Zero WH. I had to wire the Waveshare display to the Raspberry Pi using the GPIO pins and the included cabling for use with other boards.


## Setup dependencies

    sudo apt install git ttf-wqy-zenhei ttf-wqy-microhei python3 python3-pip python-imaging libopenjp2-7-dev libjpeg8-dev inkscape figlet wiringpi
    sudo pip3 install astral spidev RPi.GPIO Pillow
    sudo sed -i s/#dtparam=spi=on/dtparam=spi=on/ /boot/config.txt  #This enables SPI
    sudo reboot

### Get the BCM2835 driver

    wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.58.tar.gz
    sudo tar zxvf bcm2835-1.58.tar.gz
    cd bcm2835-1.58/
    sudo ./configure
    sudo make
    sudo make check
    sudo make install

## Using this application

### Clone it

git clone this repository in the `/home/pi` directory.

    cd /home/pi
    git clone --recursive https://github.com/jadonn/literary-clock.git
    
This should create a `/home/pi/literary-clock` directory. 

### OpenWeatherMap

Register on the [OpenWeathermap](https://openweathermap.org) website, and go to the [API Keys page](https://home.openweathermap.org/api_keys), that's the key you'll need. 
Add it to the env.sh file.  

    export OPENWEATHERMAP_APIKEY=xxxxxx

### Location information for Weather

Whichever weather provider you've picked, you'll need to provide the location and units to display in.  

Modify the `env.sh` file and update with the latitude and longitude of your location.  
As needed, change the temperature format (CELSIUS or FAHRENHEIT).  

    export WEATHER_LATITUDE=51.3656
    export WEATHER_LONGITUDE=0.1963
    export WEATHER_FORMAT=CELSIUS

## Run it

From within the `/home/pi/literary_clock.py` folder run `python literary_clock.py`. The display should update with an icon for the weather, today's date, and a quote if there is a quote for the minute of the day when the script is run.

### Automate it

Once you've proven that the run works, and an image is sent to your epaper display, you can automate it by setting up a cronjob.  

    crontab -e

Add this entry so it runs every minute:

    * * * * * cd /home/pi/weather-cklock-compliments && python3 literary_clock.py > run.log 2>&1

This will cause the script to run every minute, and write the output as well as errors to the run.log file. 


## Troubleshooting

If the scripts don't work at all, try going through the Waveshare sample code linked below - if you can get those working, this script should work for you too. 

Cron job errors should go to syslog or be viewable through running `sudo journalctl -xe`.

The scripts cache the calendar and weather information, to avoid hitting weather API rate limits.   
If you want to force a weather update, you can delete the `weather-cache.json`.


## Waveshare documentation and sample code

Check the Waveshare wiki for [more information for your display](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT)


The [Waveshare demo repo is here](https://github.com/waveshare/e-Paper).  Assuming all dependencies are installed, these demos should work.  

    git clone https://github.com/waveshare/e-Paper
    cd e-Paper


This is the best place to start for troubleshooting - try to make sure the examples given in their repo works for you. 

[Readme for the C demo](https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/c/readme_EN.txt)

[Readme for the Python demo](https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/readme_jetson_EN.txt)


