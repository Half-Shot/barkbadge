import json
import os


class Fursona:
	def __init__(self, data):
		self.name = data['name']
		self.avatars = data['avatars']
		self.telegram = data['telegram']
		self.quotes = data.get('quotes', [])
		self.colors = [tuple(x) for x in data['colors']] 

def load_fursonas():
	fursonas = []
	for fursona in os.listdir('fursonas'):
		if fursona.endswith('json'):
			with open(f'fursonas/{fursona}') as f:
				fursonas.append(
					Fursona(
						json.loads(
							f.read()
						)
					)
				)
	return fursonas


load_fursonas()