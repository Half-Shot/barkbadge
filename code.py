import time

import adafruit_logging as logging
import board
import neopixel
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.sequence import AnimationSequence
from digitalio import DigitalInOut, Direction, Pull

from fursona_page import FursonaPickPage
from home_page import Homepage
from state import BadgeState
from status_page import StatusPage

neopixels = neopixel.NeoPixel(board.NEOPIXEL, 4, auto_write=False, brightness=0)

logger = logging.getLogger('BadgeApp')
logger.setLevel(logging.DEBUG)
class BadgeApp:
	buttons = []
	display = board.DISPLAY

	button_down = [False, False, False, False]
	needs_redraw = True

	enable_rainbow = False

	last_rendered_fursona = None

	def __init__(self):
		self.state = BadgeState()
		self.colorcycle = ColorCycle(neopixels, speed=0.4, colors=[(255,255,255)])
		self.animations = AnimationSequence(
			self.colorcycle,
			RainbowSparkle(neopixels, speed=0.1, num_sparkles=15),
		)
		self.pages = [
			Homepage(self.state),
			StatusPage(self.state),
			FursonaPickPage(self.state),
		]

		for pin in (board.BUTTON_A, board.BUTTON_B, board.BUTTON_C, board.BUTTON_D):
			switch = DigitalInOut(pin)
			switch.direction = Direction.INPUT
			switch.pull = Pull.UP
			self.buttons.append(switch)

	def change_page(self, page):
		if page == len(self.pages):
			page = 0
		elif page < 0:
			page = len(self.pages) - 1
		self.state.current_page = page
		self.needs_redraw = True
		self.state.save_state()

	def on_button_press(self, button_index, duration):
		logger.debug(f"Button {button_index} pressed for {duration}s")
		page = self.pages[self.state.current_page]
		if button_index == 0 and hasattr(page, "on_button_press"):
			page.on_button_press(0)
		elif button_index == 1:
			# Back Button
			self.change_page(self.state.current_page-1)
		elif button_index == 2:
			# Next Button
			self.change_page(self.state.current_page+1)
		elif button_index == 3:
			if duration >= 2:
				# Change rainbow mode
				self.animations.next()
			if neopixels.brightness < 1:
				neopixels.brightness += 0.25
			else:
				neopixels.brightness = 0
			neopixels.show()


	def update(self, delta):
		page = self.pages[self.state.current_page]
		if page.update(delta) == True:
			self.needs_redraw = True

		if self.last_rendered_fursona != self.state.current_fursona:
			self.colorcycle.colors = [tuple(x) for x in self.state.current_fursona.colors]

		for i, b in enumerate(self.buttons):
			if self.button_down[i] and b.value:
				# Button up
				self.on_button_press(i, self.button_down[i])
				self.button_down[i] = 0

			if not b.value:
				self.button_down[i] += delta

	def render(self):
		page = self.pages[self.state.current_page]
		page.render(self.display)

	def loop(self):
		if neopixels.brightness != 0:
			self.animations.animate()
		try:
			self.update(0.1)
			if self.needs_redraw:
				logger.debug("Rendering")
				self.render()
				time.sleep(self.display.time_to_refresh)
				self.display.refresh()
				self.needs_redraw = False
		except Exception as e:
			# TODO: Check the exception kind here.
			logger.warning("Loop error %s", e)
		time.sleep(0.1)

app = BadgeApp()

while True:
	app.loop()
