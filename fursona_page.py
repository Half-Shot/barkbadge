import gc

import adafruit_logging as logging
import analogio
import board
import displayio
from adafruit_display_text import label

from media import BW_PALETTE

logger = logging.getLogger('FursonaPickPage')

class FursonaPickPage:
	avatar_bitmap = None

	last_rendered_fursona = None

	def __init__(self, state):
		self.state = state

	def on_button_press(self, button):
		# Cycle fursona
		logger.info("Cycling fursona")
		self.state.next_fursona()

	def update(self, ms_delta):
		if self.last_rendered_fursona != self.state.current_fursona:
			# Need to get new bitmaps
			self.avatar_bitmap = displayio.OnDiskBitmap(self.state.current_fursona.avatars[0])
			self.last_rendered_fursona = self.state.current_fursona
			gc.collect()
			return True

	def render(self, display):
		root = displayio.Group(scale=1)

		if not self.last_rendered_fursona:
			return # Skip this render loop

		# Gives us a white backgroud
		color_bitmap = displayio.Bitmap(display.width, display.height, 1)
		bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=BW_PALETTE)
		root.append(bg_sprite)

		avatar = displayio.TileGrid(self.avatar_bitmap, pixel_shader=self.avatar_bitmap.pixel_shader, x=(display.width // 2), y=0)
		root.append(avatar)

		text_area = label.Label(
			self.state.FONT_FANCY_MEDIUM,
			text="Fursona",
			color=0x000000,
			anchor_point=(0, 0),
			anchored_position=(5, 5)
		)
		root.append(text_area)

		text_area = label.Label(
			self.state.FONT_FANCY_LARGE,
			text=self.state.current_fursona.name,
			color=0x000000,
			anchor_point=(0.5, 0.5),
			anchored_position=(display.width // 4, display.height // 2)
		)
		root.append(text_area)
		display.show(root)
