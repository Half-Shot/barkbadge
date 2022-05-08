#!/bin/sh
set +e
KERNEL=`uname --kernel-name | tr '[:upper:]' '[:lower:]'`
mkdir -p bin

if [ -f "bin/mpy-cross" ]; then
	echo "ERROR: bin/mpy-cross exists"
	exit 1
fi

if [ $(uname -m) != 'x86_64' ]; then
	echo "ERROR: Only x86_64 architectures supported."
	exit 2
fi

wget -O bin/mpy-cross https://adafruit-circuit-python.s3.amazonaws.com/bin/mpy-cross/mpy-cross.static-amd64-$KERNEL-7.2.5
chmod +x bin/mpy-cross