import os
import sys

libdir = "./lib/e-Paper/RaspberryPi_JetsonNano/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5b_V2 as epd7in5

def main():

	try:
		epd = epd7in5.EPD()
		epd.init()
		epd.Clear()
		epd.sleep()
	except IOError as e:
		print(e)

if __name__ == '__main__':
	main()