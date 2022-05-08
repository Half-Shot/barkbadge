import gc

import adafruit_logging as logging
import displayio
from adafruit_display_text import label

from media import BW_PALETTE

QUOTE_ROTATE_EVERY_S = 300

logger = logging.getLogger('Homepage')

class Homepage:
	avatar_bitmaps = []

	last_rendered_fursona = None

	quote_section = ""
	quote_period = 0
	quote_index = 0
	avatar_index = 0

	def __init__(self, state):
		self.state = state

	def update(self, s_delta):
		if self.last_rendered_fursona != self.state.current_fursona:
			self.quote_index = 0
			self.avatar_index = 0
			logger.debug("Loading avatar")
			self.avatar_bitmaps = []
			for avatars in self.state.current_fursona.avatars:
				self.avatar_bitmaps.append(
					displayio.OnDiskBitmap(avatars)
				)
			# Need to get new bitmaps
			self.last_rendered_fursona = self.state.current_fursona
			gc.collect()
			return True

		self.quote_period += s_delta
		if self.quote_period >= QUOTE_ROTATE_EVERY_S:
			logger.debug("Loading quote")
			self.quote_index += 1
			self.quote_period = 0
			if self.quote_index == len(self.state.current_fursona.quotes):
				self.quote_index = 0

			self.avatar_index += 1
			if self.avatar_index == len(self.state.current_fursona.avatars):
				self.avatar_index = 0
			return True



	def render(self, display):
		logger.debug("Rerendering home page")
		root = displayio.Group(scale=1)
		
		if not self.last_rendered_fursona:
			return # Skip this render loop

		# Gives us a white backgroud
		color_bitmap = displayio.Bitmap(display.width, display.height, 1)
		bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=BW_PALETTE)
		root.append(bg_sprite)

		avatar_bitmap = self.avatar_bitmaps[self.avatar_index]
		if avatar_bitmap:
			avatar = displayio.TileGrid(avatar_bitmap, pixel_shader=avatar_bitmap.pixel_shader, x=0, y=0)
			root.append(avatar)

		name = label.Label(
			self.state.FONT_FANCY_LARGE,
			text=self.state.current_fursona.name,
			color=0x000000,
			anchor_point=(0.5, 0.5),
			anchored_position=(195,30)
		)
		root.append(name)

		telegram_text = label.Label(
			self.state.FONT_FANCY_MEDIUM,
			text=self.state.current_fursona.telegram,
			color=0x000000,
			anchor_point=(0, 0.5),
			anchored_position=(150, 100)
		)
		root.append(telegram_text)

		tg_logo = displayio.TileGrid(
			self.state.BM_TELEGRAM_LOGO,
			pixel_shader=self.state.BM_TELEGRAM_LOGO.pixel_shader,
			x=120,
			y=85
		)
		root.append(tg_logo)
		self.quote_text = label.Label(
			self.state.FONT_TEXT,
			text=self.state.current_fursona.quotes[self.quote_index],
			color=0x000000,
			anchor_point=(0.5, 0.5),
			anchored_position=(190, 60)
		)
		root.append(self.quote_text)
	
		display.show(root)
