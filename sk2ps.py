#! /usr/bin/env python

# Sketch - A Python-based interactive drawing program
# Copyright (C) 1998, 1999, 2000, 2003 by Bernhard Herzog
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA



# Convert a SKFile into a PostScript file.
#
# This is a very simple implementation of such a script: Just load the
# entire drawing into a document object (via the load module) and draw
# it into a PostScriptDevice.
#
# This means that a lot of more or less unnecessary modules are
# loaded...

import sys, os

from Sketch import load, PostScriptDevice
from Sketch.Lib import util

def sk2ps(filename, psfilename, **psargs):
    # convert the SK file FILENAME into a PostScript file PSFILENAME.
    # Any keyword arguments are passed to the PostScript device class.
    doc = load.load_drawing(filename)
    bbox = doc.BoundingRect(visible = psargs.get('visible', 0),
                            printable = psargs.get('printable', 1))
    psargs['bounding_box'] = tuple(bbox)
    psargs['document'] = doc
    ps = apply(PostScriptDevice, (psfilename,), psargs)
    doc.Draw(ps)
    ps.Close()


usage = '''\
usage: sk2ps [Options] infile [outfile]

Convert the Skencil/Sketch SK-file infile to PostScript (EPS). Output is
written to outfile or to stdout.

Generic options:

  -h --help             Print this help message and exit

Layer Selection:

Normally all layers marked as printable are printed, regardless of
whether they are visible or not. These options control which layers to
print:

  -v --visible          Print all layers marked as visible
  -p --noprintable      Choose layers only according to their visible flag
                        and the -v option.

Eps Header Comments:

  -t --title=TITLE      Use TITLE as the value of the `Title:\' comment.
                        Default is the basename of infile.
  -d --date=DATE        Use the DATE as the vale of the `CreationDate:\'
                        comment. Default is the current date.
  -f --for=NAME         Use NAME as the value of the `For:\' comment.
                        default is the real user name.

Other Options:

  -e --embed-fonts      Embed fonts in the eps file.
  -r --rotate           Rotate the drawing 90 degree counter clockwise
'''

def print_usage():
    print usage

def main():
    import Sketch
    Sketch.init_lib()

    draw_printable = 1
    draw_visible = 0
    embed_fonts = 0
    eps_for = util.get_real_username()
    eps_date = util.current_date()
    eps_title = None
    rotate = 0

    import getopt
    opts, args = getopt.getopt(sys.argv[1:], 'hprved:f:t:',
                               ['help', 'noprintable', 'rotate', 'visible',
                                'embed-fonts', 'for=', 'date=', 'title='])

    for optchar, value in opts:
        if optchar == '-h' or optchar == '--help':
            print_usage()
            return -1
        elif optchar == '-p' or optchar == '--noprintable':
            draw_printable = 0
        elif optchar == '-v' or optchar == '--visible':
            draw_visible = 1
        elif optchar == '-d' or optchar == '--date':
            eps_date = value
        elif optchar == '-f' or optchar == '--for':
            eps_for = value
        elif optchar == '-r' or optchar == '--rotate':
            rotate = 1
        elif optchar == '-t' or optchar == '--title':
            eps_title = value
        elif optchar == '-e' or optchar == '--embed-fonts':
            embed_fonts = 1

    if len(args) not in (1, 2):
        print_usage()
        return -1

    filename = args[0]
    if len(args) > 1:
        psfile = args[1]
    else:
        psfile = sys.stdout

    if eps_title is None:
        eps_title = os.path.basename(filename)

    sk2ps(filename, psfile, printable= draw_printable, visible = draw_visible,
          For = eps_for, CreationDate = eps_date, Title = eps_title,
          rotate = rotate, embed_fonts = embed_fonts)

if __name__ == '__main__':
    result = main()

    if result:
        sys.exit(result)
