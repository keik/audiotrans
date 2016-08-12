# -*- coding: utf-8 -*-


from sys import exit
from os import path
from logging import getLogger, StreamHandler, Formatter, DEBUG
from . import cli

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
        logger.error('Not implemented')
        exit(1)

    else:
        if not path.isfile(args.filepath):
            logger.error('file not found in "{}"'.format(args.filepath))
            exit(1)

    # ------------------------
    # import modules
    # ------------------------
    import wave
    import pyaudio
    import time
    from functools import reduce
    trs = _load_transforms(args.transforms)

    p = pyaudio.PyAudio()

    wf = wave.open(args.filepath)

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        transformed_data = reduce(lambda acc, m: m.transform(acc), trs, data)

        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    wf.close()

    p.terminate()


def _load_transforms(transforms):

    from . import Transform
    import inspect

    transforms_with_args = map(lambda t: (t, [], {}), transforms)

    def instantiate_transform(module_name, *args, **kwargs):
        tr_module = __import__(module_name)
        tr_class_members = inspect.getmembers(
            tr_module,
            lambda c: issubclass(c if inspect.isclass(c) else None.__class__,
                                 Transform))
        if len(tr_class_members) > 1:
            raise
        return tr_class_members[0][1](*args, **kwargs)

    return [instantiate_transform(tr[0], *tr[1], **tr[2])
            for tr in transforms_with_args]
