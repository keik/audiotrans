# -*- coding: utf-8 -*-

from argparse import ArgumentParser


def main():

    parser = ArgumentParser()

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Run as verbose mode')

    args = parser.parse_args()
    print(args)
