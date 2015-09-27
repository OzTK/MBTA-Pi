from time import sleep
import sys
import urllib.request
import json
import pfioutils

# Constants
SWIPE_SLEEP_TIME = 0.1
LAST_LED = 7
LEDS_NUMBER = 8
API_KEY = "VWDs8NCjg0OPWxYFZar-tg"
MBTA_URL_TEMPLATE = "http://realtime.mbta.com/developer/api/v2/predictionsbystop?api_key={0}&stop={1}&format=json"
# to avoid flooding the api
API_CALL_SLEEP_TIME = 15

flag_exit = False
pfio = pfioutils.PFIOUtils()

# prediction calculation
def get_prediction(trip):
	seconds = int(trip["pre_away"])
	minutes = seconds / 60
	return int(minutes)

# flag script for exit on 1st (lowest) button press
def on_first_button_pressed(event):
	global flag_exit
	flag_exit = True
	print("EXIT REQUESTED")

# returns true and unregister button handler if exit flag is on
def check_exit():
	if flag_exit:
		pfio.unregisterButtonAction(0)
		print("Unregistered action button")
	return flag_exit

stop_id = None
bus_line = None
if len(sys.argv) > 1:
	if sys.argv[1] == "reset":
		print("deinit board")
		pfio.p.deinit_board()
		sys.exit()
	elif len(sys.argv) == 3:
		stop_id = sys.argv[1]
		bus_line = sys.argv[2]
		print("Configured with stop {0} and bus {1}".format(stop_id, bus_line))

if stop_id == None or bus_line == None:
	print("Wrong arguments: stop id and bus line must be specified")
	pfio.p.deinit_board()
	sys.exit()

pfio.registerButtonAction(0, on_first_button_pressed)

mbta_url = MBTA_URL_TEMPLATE.format(API_KEY, stop_id)

while True:
	if check_exit():
		break
	print("Loading mbta data...")
	try:
		res = urllib.request.urlopen(mbta_url)
	except urllib.error.HTTPError:
		print("No bus data! Is it too late?")
		pfio.blink_leds(3)
		sleep(API_CALL_SLEEP_TIME)
		continue
	except urllib.error.URLError:
		print("No internet access")
		pfio.blink_leds(1)
		continue
		
	data = json.loads(res.read().decode("utf-8"))
	routes = data["mode"][0]["route"]
	
	print("Extracting bus prediction")
	prediction = 0
	for route in routes:
		if route["route_id"] == bus_line:
			prediction = get_prediction(route["direction"][0]["trip"][0])
			break

	print("Showing prediction: " + str(prediction) + "min")
	if prediction > 0:
		pfio.turn_on_leds(prediction if prediction < LEDS_NUMBER else LEDS_NUMBER, LEDS_NUMBER)
	else:
		pfio.swipe_leds(LEDS_NUMBER, SWIPE_SLEEP_TIME)

	if check_exit():
		break

	sleep(API_CALL_SLEEP_TIME)

pfio.p.disable_interrupts()
pfio.p.deinit_board()
# Workaround to get the board deinitialized (pfio bug)
pfio = pfioutils.PFIOUtils()
pfio.p.deinit_board()