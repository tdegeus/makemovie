# makemovie

Wrapper around `ffmpeg` to speed-up interaction with it. In particular, `makemovie`, can create a movie automatically from a bunch of image-files.

This program can perform several conversions (automatically if they are essential):

* Renumber such that the index is between `1..N`. (*automatic*)
* Convert SVG -> PNG. (*automatic*)
* Trim all images to the same size.
* Apply a (non-transparent) background.

>   This program can be also used to automatically convert a bunch of image files, without making a movie.

## Usage

```bash
# getting help
makemovie --help

# general usage: make movie from PNG-files
makemovie -o movie *.png

# verbose (print) operations
makemovie --verbose -o movie *.png

# tip: keep all intermediate files
makemovie --temp-dir tmp *.png

# tip: image conversion in the current folder
makemovie --trim --temp-dir . *.png
```



imagemagick
rsvg-convert
