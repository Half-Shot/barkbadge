import json

from adafruit_bitmap_font import bitmap_font
from displayio import OnDiskBitmap

from fursona import load_fursonas


class BadgeState:
	BM_TELEGRAM_LOGO = OnDiskBitmap('/bitmaps/telegram.bmp')
	FONT_FANCY_LARGE = bitmap_font.load_font("/fonts/bree-32.bdf")
	FONT_FANCY_MEDIUM = bitmap_font.load_font("/fonts/bree-24.bdf")
	FONT_TEXT = bitmap_font.load_font("/fonts/ubuntu-18.bdf")

	def __init__(self):
		self.load_state()
		self.fursonas = load_fursonas()
		self.current_fursona = self.fursonas[self.current_fursona_index]

	def load_state(self):
		with open('state.json', 'r') as f:
			prev_state = json.loads(f.read())
			self.current_fursona_index = prev_state.get("current_fursona_index", 0)
			self.current_page = prev_state.get("current_page", 0)

	def save_state(self):
		pass
		#with open('state.json', 'w') as f:
			# f.write(json.dumps({
			# 	"current_fursona_index": self.current_fursona_index,
			# 	"current_page": self.current_page
			# }))

	def next_fursona(self):
		if self.current_fursona_index == len(self.fursonas) - 1:
			self.current_fursona_index = 0
		else:
			self.current_fursona_index += 1
		self.current_fursona = self.fursonas[self.current_fursona_index]
		self.save_state()