# -*- coding: utf-8 -*-


from sys import exit
from os import path
from array import array
from logging import getLogger, StreamHandler, Formatter, DEBUG
from . import cli
from . import load_transforms
from .visualizer import Visualizer
from threading import Lock


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

    wf = wave.open(args.filepath)

    # ------------------------
    # initialize visualizer
    # ------------------------

    lock = Lock()
    if args.chart_type is None:
        visualizer = None

    else:
        visualizer = Visualizer(chart_type=args.chart_type, framerate=wf.getframerate())

    # ------------------------
    # read and transform
    # ------------------------

    transformed_data_buffer = None
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        nonlocal transformed_data_buffer

        data = wf.readframes(frame_count)
        transformed_data = reduce(lambda acc, m: m.transform(acc), trs,
                                  np.fromstring(data, np.int16) / 2 ** 15)
        logger.info('transformed data is formed {}'
                    .format([t.shape for t in transformed_data]
                            if type(transformed_data) is tuple else transformed_data.shape))

        lock.acquire()
        if transformed_data_buffer is None:
            transformed_data_buffer = transformed_data
        else:
            if type(transformed_data) is tuple:
                transformed_data_buffer = [np.append(transformed_data_buffer[i],
                                                     transformed_data[i])
                                           for i in range(len(transformed_data_buffer))]
            else:
                transformed_data_buffer = np.append(transformed_data_buffer, transformed_data)
        lock.release()

        # # TODO: output remixed wave properly method
        if type(transformed_data) is not tuple and len(transformed_data.shape) == 1:
            ndata = array('h', (transformed_data * 2 ** 15).astype(int)).tostring()
            if len(data) == len(ndata):
                data = ndata

        if visualizer is not None and visualizer.init is False:
            while visualizer.init is False:
                time.sleep(0.01)

        return (data, pyaudio.paContinue)

    # ------------------------
    # read and transform
    # ------------------------

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    frames_per_buffer=int(args.buffer_size),
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(1 / 30)
        if visualizer is not None and transformed_data_buffer is not None:
            # draw and clear transformed data to prevent render same data many times
            lock.acquire()
            visualizer.draw(transformed_data_buffer)
            transformed_data_buffer = None
            lock.release()

    stream.stop_stream()
    stream.close()
    wf.close()

    p.terminate()
