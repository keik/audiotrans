# -*- coding: utf-8 -*-

import sys
from argparse import ArgumentParser, RawTextHelpFormatter
import subarg


def get_args():

    sys.argv = subarg.parse(sys.argv)

    parser = ArgumentParser(
        description="""Transform audio in real-time""",
        epilog="""Passing arguments to transforms:
  For -t, you may use subarg syntax to pass options to the transforms
  as the second parameter. For example:

    -t [ stft -w 2048 -H 256 ]

  For details of available options, see documents of transforms which to use.
""",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('filepath', nargs='?',
                        help="""Audio file path to read on stream and transform.""")

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Run as verbose mode')

    parser.add_argument('-b', '--buffer-size', dest='buffer_size', default='1024',
                        help="""Buffer size to read data on stream""")

    parser.add_argument('-t', '--transform', dest='transforms', default=[], action='append',
                        help="""Transform module name to apply.
Specified module name is auto-prefixed `audiotrans_transform_`,
so to use `audiotrans_transform_stft`, you may just specify `stft`.""")

    parser.add_argument('-c', '--chart-type', dest='chart_type',
                        help="""Chart type to data visualization.
Below values are available:

  freq : Display frequency of wave.
         To plot, transformed data must be formed 1-D array of wave.
  spec : Display spectrum of wave.
         To plot, Transformed data must be formed 1-D array of spectrum
         or 2-D array of spectrogram.

Or if not specified, no chart appears.""")

    return parser.parse_args()
