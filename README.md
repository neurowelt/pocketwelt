# pocketwelt

Python powertool in your pocket :hammer:

## Introduction

`pocketwelt` purpose is to provide basic tools for Python projects.

Idea for this package came from my personal experience of repeating certain methods over and over again - quite simple, but yet too complex to keep them in my memory at all times.

Hopefully `pocketwelt` will help you as it helps me - as a pocekt tool that comes in handy when I want to kickstart development as fast as possible or simply forgot about simple base64 encoding ;)

Worth noting - package uses only built-in Python libraries. My purpose is to keep this as vanilla as possible, so it does not collide with other dependencies you might have in your project.

## Installation

`pocketwelt` is available on [PyPi](...) and you can install it via pip:

```bash
pip install pocketwelt
```

You can also install it straight from git:

```bash
pip install git+https://github.com/neurowelt/pocketwelt.git
```

## Usage

Since this package is built using only vanilla Python libraries you can start using it right away after installing! Check out a few examples to get you going:
* [Custom colored logger](#custom-colored-logger)
* [Pickle your custom class](#pickle-your-custom-class)
* [Decode `base64` images](#decode-base64-images)

### Custom colored logger

`pocketwelt` comes with a neat `CustomLogger` class that provides colored logs and simple file based logging. You can create as many loggers as you want by simply calling the following method:

```python
from pocketwelt import getCustomLogger

error_logger = getCustomLogger("Error Logger", "ERROR")
info_logger = getCustomLogger("Info Logger", "INFO")

# Use as usual
error_logger.error("Error")
error_logger.info("Info that won't log")
info_logger.info("Info")
```

### Pickle your custom class

Often times when working with large dictionaries that contain more complex types you may want to save your current class for later to quickly reload it. You can more than easily use the following methods to do this:

```python
from pocketwelt import save_pickle, load_pickle
from your_script.complex_class import CustomClass

# Perform some operations with your class
llm = CustomClass()
llm.func()
llm.calc()

# Save object for later
save_pickle(llm, "llm.pkl")

# Reload it back
llm = load_pickle("llm.pkl")
```

### Decode `base64` images

You never know when you're going have to decode some base64 objects - that's where the `encodings` module comes in! For example, decoding `base64` image to `PIL.Image` never have been easier:

```python
from pocketwelt import b64_decode
from PIL import Image

decoded_obj = b64_decode(b64_image)
image = Image.open(decoded_obj)
```

> [!TIP]
> Check out the [official documentation](https://neurowelt.github.io/pocketwelt/) to read in detail about every single method and their limitations!

## Contribute

If you have a tool in your mind that you would like to see added to this package - feel encouraged to setup an [issue](https://github.com/neurowelt/pocketwelt/issues), create a [pull request](https://github.com/neurowelt/pocketwelt/pulls) with your own code or just [write to me](mailto:neurowelt.dev@gmail.com) with anything that comes to your mind!

Whenever you see a bug, vulnerability or place for enhancement, also do not hesitate to open an [issue](https://github.com/neurowelt/pocketwelt/issues) describing your findings. Any contribution will be greatly appreciated <3

## Notes

When going through the `tests` directory you will find [a painting of Gandalf](./tests/test_image.png) (see [original](https://www.jefmurray.com/gallery/)) that I use for testing. It was created by Jef Murray, a reknown fantasy illustrator. I recommend visiting his [site](https://www.jefmurray.com/gallery/) to see more of his work.