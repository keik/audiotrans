# -*- coding: utf-8 -*-


from sys import exit
from os import path
from logging import getLogger, StreamHandler, Formatter, DEBUG
from . import cli
from . import load_transforms
from .visualizer import Visualizer


logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('[%(asctime)s %(levelname)s %(module)s] %(message)s'))
logger.addHandler(handler)


def main():

    args = cli.get_args()

    if args.verbose:
        logger.setLevel(DEBUG)
        logger.info('Start as verbose mode')

    if args.filepath is None:
        logger.info('File path is not specified. Read audio inputted from mic.')

        # TODO: implement
        raise 'Not implemented'

    else:
        if not path.isfile(args.filepath):
            logger.error('file not found in "{}"'.format(args.filepath))
            exit(1)

    # ------------------------
    # import modules
    # ------------------------
    import time
    import wave
    from functools import reduce
    import numpy as np
    import pyaudio

    trs = load_transforms(args.transforms)

    # ------------------------
    # read and transform
    # ------------------------

    transformed_data = None
    p = pyaudio.PyAudio()
    wf = wave.open(args.filepath)

    def callback(in_data, frame_count, time_info, status):
        nonlocal transformed_data

        data = wf.readframes(frame_count)
        transformed_data = np.fromstring(data, np.int16) / 2 ** 15
        transformed_data = reduce(lambda acc, m: m.transform(acc), trs, transformed_data)
        logger.info('transformed {}: {}'.format(transformed_data.shape, transformed_data))
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    # ------------------------
    # read and transform
    # ------------------------

    if args.chart_type is None:
        visualizer = None

    else:
        visualizer = Visualizer(chart_type=args.chart_type, framerate=wf.getframerate())

    while stream.is_active():
        time.sleep(1 / 30)
        if visualizer is not None:
            visualizer.draw(transformed_data)

    stream.stop_stream()
    stream.close()
    wf.close()

    p.terminate()
