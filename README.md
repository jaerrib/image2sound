# image2sound

**image2sound** is a utility that accepts an image file, converts the RGB values of each pixel to a frequency, and saves the result to three separate WAV files.

*NOTE: Large image files no longer automatically result in large audio files as the user can specify a target track length and sane defaults are applied when this is not specified.*

## Requirements
- PIL
- numpy
- wavio
- argparse
- math

## To run
Simply running ```python3 main.py``` will generate audio using the test image and default settings.

### Arguments

The following optional arguments may be set, however:

- ```-p``` for a path to an image
- ```-key``` for musical key (defaults to C )
- ```-t``` for tempo (defaults to 60 bpm)
- ```-min``` for the desired number of minutes (defaults to 1 so must be set to zero if shorter tracks are wanted)
- ```-sec``` for the desired number of seconds (defaults to zero)

### "Split" mode

Note that the default behavior of the utility is to create a single stereo audio file. 
Adding ```--split``` will split the resulting audio into three separate files (red, green, blue).

### "Reveal" mode

Adding ```--reveal``` will override the key, tempo, and minutes/seconds with data derived from the image itself, "revealing" the music within the image as it were,

Example 1:
```
python3 main.py -p image.png -key Dminor -t 80 -min 11 -sec 38
```

Example 2:
```
python3 main.py -p image.png -key Dminor -t 80 -min 11 -sec 38 --split
```

Example 3:
```
python3 main.py -p image.png --reveal
```