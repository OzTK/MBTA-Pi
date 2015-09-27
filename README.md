# MBTA-Pi
This python script allows your Raspberry Pi to show the time remaining until the next MBTA bus arrives at a specified stop.

# Pre-requisites
You will need a Raspberry Pi and the Piface Digital 2 extension to make this script work. See http://www.piface.org.uk/products/piface_digital to learn more about Piface Digital.

# Setup
These steps are valid for Noobs and may vary depending on the system installed on your Rasperry Pi.

## Install python 3
`sudo apt-get install python3`

## Install pifacedigitalio
This is the python library allowing to interact with your Piface Digital
`sudo apt-get install python{,3}-pifacedigitalio`
See http://pifacedigitalio.readthedocs.org for the full api documentation

# Run the script
`python3 mbta-pi.py [stop id] [bus line]`

This will display the number of minutes (up to 8, limited by the number of leds) before the next bus at the specified stop.
The process can be exited by pressing the S0 button (the one closest to the leds).

If it happens that the process is exited by killing it, the leds will be locked in the states they were before exiting. They board can then be reset using `python3 mbta-pi.py reset`

You can find more info about the MBTA api at http://realtime.mbta.com/portal

# Launching at startup
A common use-case for this script is to have an accurate estimate of your bus arrival in the morning, so that you don't miss it, arrive late at work and have to make up a questionable excuse like "I was about to leave for work but there was a sheep standing at my front door and it wouldn't move, so I had to wait until it was gone".

So to launch your script as soon as you plug-in your Raspberry Pi, you could add this line to your Crontab:
`@reboot python3 /path/to/mbta_pi.py [stop id] [bus line] > /path/to/mbtalog.txt 2>&1 &`
