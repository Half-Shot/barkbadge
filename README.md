Bark Badge
==========

TODO: Write this.

## Setting up

This project requires a reasonably new version of Python 3, and [`poetry`](https://python-poetry.org).

To install dependencies, run:

```sh
poetry install
```

You will also need a version of `mpy-cross` which improves performance on the device by compiling the
Python first. You can use the script `tools/get-mpy.sh` to do this.

If you get stuck, see [these instructions](https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/creating-a-library#mpy-3106477-16) for help.

## Development

### Dependencies

The project depends on the following dependencies (and currently to statically depend on this, includes the libraries)