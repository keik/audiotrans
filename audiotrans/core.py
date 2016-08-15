# -*- coding: utf-8 -*-


from sys import exit
from os import path
from logging import getLogger, StreamHandler, Formatter, DEBUG
from . import cli
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

    trs = _load_transforms(args.transforms)

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
        while transformed_data is None:
            pass
        visualizer = Visualizer(chart_type=args.chart_type, framerate=wf.getframerate())

    while stream.is_active():
        time.sleep(1 / 30)
        if visualizer is not None:
            visualizer.draw(transformed_data)

    stream.stop_stream()
    stream.close()
    wf.close()

    p.terminate()


def _load_transforms(transforms):

    from . import Transform
    import inspect

    # normalize arguments to form as [(name, [option, ...]), ...]
    transforms_with_argv = map(lambda t: (t[0], t[1:]) if isinstance(t, list) else (t, []),
                               transforms)

    def instantiate_transform(module_name, argv):
        tr_module = __import__(module_name)
        tr_classes = inspect.getmembers(
            tr_module,
            lambda c: issubclass(c if inspect.isclass(c) else None.__class__,
                                 Transform))
        if len(tr_classes) > 1:
            raise 'Transform module must have only one subclass of Transform'

        tr_class = tr_classes[0]
        return tr_class[1](argv)

    return [instantiate_transform(tr[0], tr[1])
            for tr in transforms_with_argv]
