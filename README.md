# image2sound

**image2sound** is a utility that accepts an image file, converts the RGB values
of each pixel to a frequency, and saves the result to three separate WAV files.

## Requirements

*See `requirements.txt` for specifics*

## Setup

Create and enter a virtual environment then install the requirements: 

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## To run

Simply running `python3 main.py` from inside the src folder will generate audio
using the test image and default settings. Running it with `--help` now provides
dynamic and more verbose assistance by pulling from the parameter definition files. 

### Arguments

The following optional arguments may be set:

- `-p` for a path to an image
- `-o` for path to save the output file to
- `-key` for musical key (defaults to C )
- `-t` for tempo (defaults to 60 bpm)
- `-ts` to set the time signature (defaults to 4/4)
- `-w` to use specific waveform types (sine, square, triangle, sawtooth, or
  piano) 

> The "clicky" audio found in older versions has now been solved by introducing
> ADSR envelope filters. This also negates the need to use Blackman smoothing,
> which is now an option rather than the default behavior. If you prefer to use
> smoothing, pass `--smooth`.

- Use `-adsr` followed by a [template type](/src/envelope_settings.py) to choose
  a preset for attack, decay, sustain, and release values. This defaults to
  *piano*.

### "Stereo" mode

Note that the default behavior of the utility is to split the resulting audio into
separate files to make better use of DAWs. However, you may want a stereo file
instead. Do this by adding '--stereo' to your run command. Please note that this
mode bypasses the composition engine, uses a different conversion method for
generating the audio, and is incompatible with CMYK images. In addition, you can
use the following parameters in conjunction with stereo mode:

- `-min` for the desired number of minutes (defaults to 1 so must be set to zero
  if shorter tracks are wanted)
- `-sec` for the desired number of seconds (defaults to zero)

> "Stereo" mode is planned to be deprecated at some point in the future. 

### "Reveal" mode

Adding `--reveal` will override the key, tempo, and minutes/seconds with data
derived from the image itself, "revealing" the music within the image

> **"Reveal" mode plus overrides**
>
> You can specify arguments as overrides in conjunction with "Reveal" mode. For
> example, if you want to make sure that the key is D-Major, but you want the
> other parameters to be derived from the image,
> run `python3 main.py -key D-Major --reveal`

### Experimental new conversion method

Adding `--method2` will utilize an experimental new conversion method that
limits the left and right channels to specific frequency ranges, simulating "
left-hand" and "right-hand" keyboard parts. Please note that this method does
not currently support "Split" mode.

### "Quartet Mode"

Using CMYK images will automatically trigger "quartet mode." This will create
four separate, mono WAV files with each being limited to the sonic range
associated with the four instruments used in a traditional string quartet

### MIDI export with Composition Engine

Adding `--midi` will export the converted audio as a MIDI file.

#### Differences from the standard conversion method

- MIDI now uses a composition engine which arranges phrases and sections into songs. You can specify a movement type with `-mt` (sonata is the default).
- It also incorporates *variable note lengths*. The note lengths are determined by the difference between the color value of the current note in the list and that of the following note.
- Composition styles are defined in `movement_definitions.py` and new variations can be added there.
- Use of the composition engine means that *time parameters passed by the user no longer have any effect* since the track length is determined by the movement style and the tempo.
  - Red, cyan, and magenta = violin
  - Blue and yellow = viola
  - Green and black = cello

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
python3 main.py -p image.png -key G-Major -t 96 -min 4 -sec 20 -ts 3/4 -adsr cello -w sawtooth --stereo
```

Example 5:

```
python3 main.py -p image.png -key A-Major -t 80 --midi -mt rondo
```
