# image2sound

**image2sound** is a utility that accepts an image file, converts the RGB values
of each pixel to a frequency, and saves the result to three separate WAV files.

*NOTE: Large image files no longer automatically result in large audio files as
the user can specify a target track length and sane defaults are applied when
this is not specified.*

## Requirements

*See `requirements.txt` for specifics*

## To run

Simply running `python3 main.py` will generate audio using the test image and
default settings.

### Arguments

The following optional arguments may be set, however:

- `-p` for a path to an image
- `-o` for path to save the output file to
- `-key` for musical key (defaults to C )
- `-t` for tempo (defaults to 60 bpm)
- `-min` for the desired number of minutes (defaults to 1 so must be set to zero
  if shorter tracks are wanted)
- `-sec` for the desired number of seconds (defaults to zero)
- `-ts` to set the time signature (defaults to 1/1, essentially "no feel")

> The algorithm now uses Blackman smoothing by default. The original conversion
> method had a characteristic "clicky" sound due to incomplete wave forms. To
> achieve the original sound, pass `--nosmooth`.

### "Split" mode

Note that the default behavior of the utility is to create a single stereo audio
file.
Adding `--split` will split the resulting audio into three separate files (red,
green, blue).

### "Reveal" mode

Adding `--reveal` will override the key, tempo, and minutes/seconds with data
derived from the image itself, "revealing" the music within the image

> **"Reveal" mode plus overrides**
>
> You can specify arguments as overrides in conjunction with "Reveal" mode. For
> example, if you want to make sure that the key is D-Major, but you want the
> other parameters to be derived from the image,
> run `python3 main.py -key D-Major --reveal`

### Experiemental new conversion method

Adding `--method2` will utilize an experimental new conversion method that
limits the left and right channels to specific frequency ranges, simulating "
left-hand" and "right-hand" keyboard parts. Please note that this method does
not currently support "Split" mode.

### Examples

Example 1:

```
python3 main.py -p image.png -key D-minor -t 80 -min 11 -sec 38
```

Example 2:

```
python3 main.py -p image.png -key D-minor -t 80 -min 11 -sec 38 --split
```

Example 3:

```
python3 main.py -p image.png --reveal
```

Example 4:

```
python3 main.py -p image.png -key G-Major -t 96 -min 4 -sec 20 -ts 3/4 --split
```