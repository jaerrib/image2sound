# image2sound

**image2sound** is a utility that accepts an image file, converts the RGB values of each pixel to a frequency, and saves the result to three separate WAV files.

*WARNING: Large image files result in large audio files. Even 48x48 images may be close to 30 minutes.*

## Requirements
- PIL
- numpy
- wavio
- argparse
- math

## To run
```
python3 main.py -p file_name -key musical_key -t tempo
```
Example:
```angular2html
python3 main.py -p image.png -key Dminor -t 80
```