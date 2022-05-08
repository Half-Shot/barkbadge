#!/bin/sh
set +e

SITE_PACKAGES=`python -c 'import site; print(site.getsitepackages()[0])'`
PACKAGES="adafruit_bitmap_font
adafruit_display_text
adafruit_io
adafruit_led_animation
adafruit_portalbase
adafruit_logging"

rm -R dist/*
mkdir -p dist/

if [ "$FULLCOPY" == "y" ]; then
	echo "Copying bitmaps..."
	cp -ur bitmaps/ dist/
	echo "Copying fursonas..."
	cp -ur fursonas/ dist/
	echo "Copying fonts..."
	cp -ur fonts/ dist/

	# Copy packages from site-packages
	echo "Installing libraries..."
	rm -R dist/lib
	mkdir -p dist/lib
	for pkg in $PACKAGES
	do
		cp -ur "$SITE_PACKAGES/$pkg" dist/lib
		for file in `find dist/lib -name '*.py' ! -name '*__init__.py'`
		do
			bin/mpy-cross $file -o ${file:0:-2}mpy
			rm $file
		done
		find dist/lib -path '*/__pycache__*' -delete
	done

	# neopixel is special
	bin/mpy-cross $SITE_PACKAGES/neopixel.py -o dist/lib/neopixel.mpy
fi


echo "Installing halfy-badge..."
for pyfile in *.py
do
	if [ $pyfile == "code.py" ]
	then
		cp -ur $pyfile dist/
	else
		bin/mpy-cross $pyfile -o dist/${pyfile:0:-2}mpy
	fi
done

# Setup blank state.

echo "{}" > dist/state.json

echo "Copying dist to device"
cp -vru dist/* /run/media/will/CIRCUITPY
