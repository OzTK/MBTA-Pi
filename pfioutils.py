from time import sleep
import pifacedigitalio as pfio

class PFIOUtils:
	def __init__(self, *args):
		if len(args) == 1:
			self.p = args[0]
		else:
			self.p = pfio.PiFaceDigital()
		self.listeners = [None, None, None, None]

	def turn_off_leds(self):
		self.p.output_port.all_off()

	def turn_on_leds(self, leds_count, total_leds):
		for i in range(total_leds):
			if i < leds_count and self.p.leds[i].value == 0:
				self.p.leds[i].turn_on()
			elif i >= leds_count and self.p.leds[i].value == 1:
				self.p.leds[i].turn_off()

	def blink_leds(self, blinksRemaining):
		for i in range(blinksRemaining):
			self.p.output_port.toggle()
			sleep(0.2)
			self.p.output_port.toggle()
			sleep(0.2)

	def swipe_leds(self, leds_count, light_sleep_time):
		self.turn_off_leds()
		for i in range(0, leds_count):
			self.p.leds[i].turn_on()
			sleep(light_sleep_time)
		for i in range(0, leds_count):
			self.p.leds[i].turn_off()
			sleep(light_sleep_time)
		for i in range(leds_count - 1, -1, -1):
			self.p.leds[i].turn_on()
			sleep(light_sleep_time)       
		for i in range(leds_count - 1, -1, -1):
			self.p.leds[i].turn_off()
			sleep(light_sleep_time)

	def registerButtonAction(self, buttonId, action):
		if len(self.listeners) > buttonId and self.listeners[buttonId] != None:
			self.unregisterButtonAction(buttonId)
		self.listeners[buttonId] = pfio.InputEventListener(chip=self.p)
		self.listeners[buttonId].register(buttonId, pfio.IODIR_RISING_EDGE, action)
		self.listeners[buttonId].activate()

	def unregisterButtonAction(self, buttonId):
		self.listeners[buttonId].deactivate()
		self.listeners[buttonId].deregister(buttonId)
		self.listeners[buttonId] = None