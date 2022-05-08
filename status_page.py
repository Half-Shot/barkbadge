import adafruit_logging as logging
import analogio
import board
import displayio
import microcontroller
from adafruit_display_text import label

from media import BW_PALETTE

VERSION = "1.0"

divider_ratio = 2
logger = logging.getLogger('StatusPage')

class StatusPage:
	battery = analogio.AnalogIn(board.VOLTAGE_MONITOR)
	battery_voltage = 0
	temp = 0
	last_check = 0

	def __init__(self, state):
		self.state = state

	def update(self, s_delta):
		self.last_check += s_delta
		if self.last_check <= 5:
			 return False
		self.last_check = 0
		
		battery_voltage = self.battery.value
		battery_voltage *= divider_ratio
		battery_voltage *= self.battery.reference_voltage
		battery_voltage /= 2**16
		battery_voltage = round(battery_voltage, 2)
		any_change = False
		changed = abs(self.battery_voltage - battery_voltage) >= 0.3
		if changed:
			self.battery_voltage = battery_voltage
			any_change = True

		changed = abs(self.temp - microcontroller.cpu.temperature) >= 2
		if changed:
			self.temp = microcontroller.cpu.temperature
			any_change = True
		
		return any_change

	def render(self, display):
		root = displayio.Group(scale=1)

		# Gives us a white backgroud
		color_bitmap = displayio.Bitmap(display.width, display.height, 1)
		bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=BW_PALETTE)
		root.append(bg_sprite)

		text_area = label.Label(
			self.state.FONT_FANCY_LARGE,
			text="Status",
			color=0x000000,
			anchor_point=(0, 0),
			anchored_position=(5, 5)
		)
		root.append(text_area)

		battery = "unknown"
		wifi = "not connected"

		text_area = label.Label(
			self.state.FONT_TEXT,
			text=f"Battery: v{self.battery_voltage}\nWiFi: {wifi}\nVersion: {VERSION}\nCPU Temp: {self.temp}",
			color=0x000000,
			anchor_point=(0, 0),
			anchored_position=(5, 35)
		)
		root.append(text_area)
		display.show(root)
