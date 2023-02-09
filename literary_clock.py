import os
import textwrap
import sys
import weather_env

from datetime import datetime
from glob import glob
from random import randrange
from PIL import Image, ImageDraw, ImageFont, ImageOps


libdir = "./lib/e-Paper/RaspberryPi_JetsonNano/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5b_V2 as epd7in5
from weather_providers import openweathermap

def format_weather_description(weather_description):
    if len(weather_description) < 20:
        return {1: weather_description, 2: ''}

    splits = textwrap.fill(weather_description, 20, break_long_words=False,
                           max_lines=2, placeholder='...').split('\n')
    weather_dict = {1: splits[0]}
    weather_dict[2] = splits[1] if len(splits) > 1 else ''
    return weather_dict

def main():

	openweathermap_apikey = weather_env.OPENWEATHERMAP_APIKEY
	location_lat = weather_env.WEATHER_LATITUDE
	location_long = weather_env.WEATHER_LONGITUDE
	unit = weather_env.WEATHER_FORMAT

	weather_provider = openweathermap.OpenWeatherMap(
		openweathermap_apikey,
		location_lat,
		location_long,
		"metric"
	)

	weather = weather_provider.get_weather()

	degrees = "°C"

	weather_desc = format_weather_description(weather["description"])

	output_dict = {
		'LOW_ONE': "{}{}".format(str(round(weather['temperatureMin'])), degrees),
		'HIGH_ONE': "{}{}".format(str(round(weather['temperatureMax'])), degrees),
		'ICON_ONE': weather["icon"],
		'WEATHER_DESC_1': weather_desc[1],
		'WEATHER_DESC_2': weather_desc[2]
	}


	image = Image.new(mode='1', size=(800, 480), color=255)
	drawImage = ImageDraw.Draw(image)

	#Weather icon
	iconPath = 'icons/%s.xbm' % output_dict['ICON_ONE']
	iconImage = ImageOps.invert(Image.open(iconPath).resize((100, 100)).convert('L'))
	image.paste(iconImage, (140, 370))
	
	#Weather numbers
	tempFont = ImageFont.truetype('Literata72pt-Regular.ttf', 72)
	temp = '%s / %s' % (output_dict['HIGH_ONE'], output_dict['LOW_ONE'])
	drawImage.text((285, 365), temp, font=tempFont, fill=0)

	#Current Time
	now = datetime.now()
	hour_minute = now.strftime('%H%M')
	now_time = now.strftime('%H:%M')
	draw_time = ImageDraw.Draw(image)
	time_font = ImageFont.truetype('Literata72pt-Regular.ttf', 144)
	draw_time.text((220, 100), now_time, font=time_font, fill=0)

	image = ImageOps.invert(image)
	return image

def redDraw():
	imageRed = Image.new(mode='1', size=(800, 480), color=255)

#Current date
	now = datetime.now()
	today = now.strftime('%a, %B, %d')
	dayFont = ImageFont.truetype('Literata72pt-Regular.ttf', 72)
	drawDate = ImageDraw.Draw(image)
	drawDate.text((100, 20), today, font=dayFont, fill=0)

	ImageDraw.Draw(imageRed).line([(0, 78), (800, 78)], fill=0, width=4)
	
	return imageRed

if __name__ == '__main__':
	image = main()
	imageRed = redDraw()
	try:
		epd = epd7in5.EPD()
		epd.init()
		if datetime.now().minute == 0 and datetime.now().hour == 2:
			epd.Clear()
		epd.display(epd.getbuffer(image), epd.getbuffer(imageRed))
		epd.sleep()
	
	except IOError as e:
		print(e)
	
	except KeyboardInterrupt:
		epd.sleep()