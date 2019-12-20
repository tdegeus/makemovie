'''trim_image
    Trim a batch of images.

Usage:
    trim_image [options] <image>...

Arguments:
    The images to trim.

Options:
    -a, --append=<str>
        Append filenames, if empty the input files are overwritten. [default: ]

    --background=<str>
        Apply a background color (e.g. "none" or "white").

    --flatten
        Flatten input images: required for transparent PNG-files.

    --temp-dir=<str>
        Output directory for temporary images (deleted if not specified).

    -v, --verbose
            Print all executed commands.

    -h, --help
        Show help.

    --version
        Show version.

(c-MIT) T.W.J. de Geus | tom@geus.me | www.geus.me | github.com/tdegeus
'''

import docopt

from .. import __version__
from .. import trim


def main():

    args = docopt.docopt(__doc__, version = __version__)

    trim(
        filenames = args['<image>'],
        background = args['--background'] if args['--background'] is not None else 'white',
        flatten = args['--flatten'],
        append = args['--append'],
        temp_dir = args['--temp-dir'],
        verbose = args['--verbose'])
