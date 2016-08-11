# -*- coding: utf-8 -*-


from sys import exit
from os import path
import time
from argparse import ArgumentParser
from logging import getLogger, StreamHandler, Formatter, DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('[%(asctime)s %(levelname)s %(module)s] %(message)s'))
logger.addHandler(handler)


def main():

    parser = ArgumentParser()

    parser.add_argument('filepath', nargs='?',
                        help="""Audio file path to read on stream and transform.""")

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Run as verbose mode')

    args = parser.parse_args()

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

    # TODO: proto
    import wave
    import pyaudio

    p = pyaudio.PyAudio()

    wf = wave.open(args.filepath)

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
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
