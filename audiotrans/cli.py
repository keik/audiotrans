# -*- coding: utf-8 -*-

from argparse import ArgumentParser


def get_args():

    parser = ArgumentParser()

    parser.add_argument('filepath', nargs='?',
                        help="""Audio file path to read on stream and transform.""")

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Run as verbose mode')

    parser.add_argument('-t', '--transform', dest='transforms', default=[], action='append',
                        help="""Transform module name to apply.""")

    return parser.parse_args()
