
import tempfile
import os
import re

from subprocess import check_output, STDOUT
from shutil import which



__version__ = '0.1.0'



def _exec(cmd, verbose = False):

    if verbose:
        print(cmd)

    output = check_output(cmd, shell = True, stderr = STDOUT).decode("utf-8")

    if verbose and len(output) > 0:
        print(output)

    return output



def _mkdir(dirname, verbose = False):

    if os.path.isdir(dirname):
        return

    os.makedirs(dirname)

    if verbose:
        print('mkdir {0:s}'.format(dirname))



def _mv(orig, dest, verbose = False):

    os.rename(orig, dest)

    if verbose:
        print('mv {0:s} {1:s}'.format(orig, dest))



def _check_get_abspath(filenames):

    if type(filenames) == str:
        filenames = [filenames]

    filenames = [os.path.abspath(f) for f in filenames]

    for filename in filenames:
        if not os.path.isfile(filename):
            raise IOError('"{0:s}" does not exist'.format(filename))

    return filenames



def _make_convert_tempdir(temp_dir = None, verbose = False):

    if temp_dir is None:
        temp_dir = tempfile.mkdtemp()
    else:
        temp_dir = os.path.abspath(temp_dir)

    _mkdir(temp_dir, verbose)

    return temp_dir



def _convert(filenames, options, append = None, temp_dir = None, verbose = False):
    r'''
Run convert on a batch of files.
    '''

    if not which('convert'):
        raise IOError('"convert" not found, please install ImageMagick')

    filenames = _check_get_abspath(filenames)
    temp_dir = _make_convert_tempdir(temp_dir, verbose)

    for filename in filenames:

        temp_file = os.path.join(temp_dir, os.path.relpath(filename))

        _exec('convert {options:s} "{old:s}" "{new:s}"'.format(
            options = options,
            old = filename,
            new = temp_file),
            verbose = verbose)

        if append:
            base, ext = os.path.splitext(filename)
            dest = os.path.join(base, append, ext)
        else:
            dest = filename

        _mv(temp_file, dest, verbose)



def set_background(
    filenames,
    background,
    flatten = False,
    append = False,
    temp_dir = None,
    verbose = False):
    r'''
Trim a batch of files.

:arguments:

    **filenames** (``<list<str>>``)
        A list of filenames.

    **background** (``<str>``)
        Apply a background colour (e.g. "none" or "white").

:options:

    **flatten** ([``False``] | ``True``)
        Flatten images: required for transparent PNG-files.

    **append** (``<str>``)
        If specified the original images are not overwritten. Rather the filename is
        appended with the string specified here. Note that this implies that there could be others
        files that are overwritten.

    **temp_dir** (``<str>``)
        If specified that directory is used as temporary directory. Otherwise, a directory is
        automatically selected.

    **verbose** ([``False``] | ``True``)
        If True, all commands are printed to the standard output.
    '''

    if not which('convert'):
        raise IOError('"convert" not found, please install ImageMagick')

    filenames = _check_get_abspath(filenames)
    temp_dir = _make_convert_tempdir(temp_dir, verbose)

    # add options

    opt += ['-background {0:s}'.format(background)]

    if background != 'none':
        opt += ['-alpha remove']

    if flatten:
        opt += ['-flatten']

    # apply to images

    _convert(filenames, ' '.join(opt), append, verbose)



def trim(
    filenames,
    background = 'none',
    flatten = False,
    append = False,
    temp_dir = None,
    verbose = False):
    r'''
Trim a batch of files.

:arguments:

    **filenames** (``<list<str>>``)
        A list of filenames.

:options:

    **background** ([``'none'``] | ``<str>``)
        Apply a background colour (e.g. "none" or "white").

    **flatten** ([``False``] | ``True``)
        Flatten images: required for transparent PNG-files.

    **append** (``<str>``)
        If specified the original images are not overwritten. Rather the filename is
        appended with the string specified here. Note that this implies that there could be others
        files that are overwritten.

    **temp_dir** (``<str>``)
        If specified that directory is used as temporary directory. Otherwise, a directory is
        automatically selected.

    **verbose** ([``False``] | ``True``)
        If True, all commands are printed to the standard output.
    '''

    if not which('convert'):
        raise IOError('"convert" not found, please install ImageMagick')

    filenames = _check_get_abspath(filenames)
    temp_dir = _make_convert_tempdir(temp_dir, verbose)

    # dry run to get trim size of each image

    split = lambda txt: \
        re.split(r'([0-9]*)(x)([0-9]*)(\ )([0-9]*)(x)([0-9]*)([\+][0-9]*)([\+][0-9]*)(.*)', txt)

    out = []

    for filename in filenames:
        out += [_exec('convert -trim -verbose  "{old:s}" "{new:s}"'.format(
            old = filename,
            new = os.path.join(temp_dir, 'tmp.png')),
            verbose = verbose)]

    out = [o.split('\n')[1] for o in out]

    # width of the original image
    w = [int(split(o)[1]) for o in out]

    # height of the original image
    h = [int(split(o)[3]) for o in out]

    # width of the trimmed image
    w0 = [int(split(o)[5]) for o in out]

    # height of the trimmed image
    h0 = [int(split(o)[7]) for o in out]

    # horizontal position at which the trimmed image starts
    x = [int(split(o)[8]) for o in out]

    # vertical position at which the trimmed image starts
    y = [int(split(o)[9]) for o in out]

    assert min(w0) == max(w0)
    assert min(h0) == max(h0)

    # select crop dimensions

    dim = {
        'w': max(w) + (max(x) - min(x)),
        'h': max(h) + (max(y) - min(y)),
        'x': min(x),
        'y': min(y)}

    opt = ['-crop {w:d}x{h:d}{x:+d}{y:+d}'.format(**dim)]

    # add options

    opt += ['-background {0:s}'.format(background)]

    if background != 'none':
        opt += ['-alpha remove']

    if flatten:
        opt += ['-flatten']

    # trim images

    _convert(filenames, ' '.join(opt), append, temp_dir, verbose)



def rsvg_convert(
    filenames,
    background = 'none',
    ext = '.png',
    verbose = False):
    r'''
Convert SVG images.

:arguments:

    **filenames** (``<list<str>>``)
        A list of filenames.

:options:

    **background** ([``'none'``] | ``<str>``)
        Apply a background colour (e.g. "none" or "white").

    **ext** ([``'.png'``] | ``<str>``)
        Extension to which to convert to.

    **verbose** ([``False``] | ``True``)
        If True, all commands are printed to the standard output.

:returns:

    List of new filenames.
    '''

    if not which('rsvg-convert'):
        raise IOError('"rsvg-convert" not found')

    filenames = _check_get_abspath(filenames)
    out = []

    for filename in filenames:

        dest = os.path.splitext(file)[0] + '.png'
        out += [dest]

        _exec('rsvg-convert -b {background:s} "{old:s}" -o "{new:s}"'.format(
            background = background,
            old = filename,
            new = dest),
            verbose = verbose)

    return out


