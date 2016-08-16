import mock
import pytest

import sys
import time

import audiotrans.core


class MockStream():
    def __init__(self, format, channels, rate, output, stream_callback):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.output = output
        self.stream_callback = stream_callback

        self.counter = 0

    def start_stream(self):
        for i in range(3):
            time.sleep(0.1)
            self.stream_callback(None, 100, None, None)

    def is_active(self):
        self.counter += 1
        if self.counter < 10:
            return True
        else:
            return False

    def stop_stream(self):
        pass

    def close(self):
        pass


@mock.patch('pyaudio.PyAudio.open',
            new=lambda self, **kwargs: MockStream(**kwargs))
def test_with_verbose_mode():
    sys.argv[1:] = ['data/drums.wav', '-v']
    audiotrans.core.main()


@mock.patch('pyaudio.PyAudio.open',
            new=lambda self, **kwargs: MockStream(**kwargs))
def test_with_visualizer():
    sys.argv[1:] = ['data/drums.wav', '-c', 'freq']
    audiotrans.core.main()


@mock.patch('pyaudio.PyAudio.open',
            new=lambda self, **kwargs: MockStream(**kwargs))
def test_with_filepath():
    sys.argv[1:] = ['data/drums.wav']
    audiotrans.core.main()


@mock.patch('pyaudio.PyAudio.open',
            new=lambda self, **kwargs: MockStream(**kwargs))
def test_with_invalid_filepath():
    sys.argv[1:] = ['data/invalid.wav']
    with pytest.raises(SystemExit):
        audiotrans.core.main()


@mock.patch('pyaudio.PyAudio.open',
            new=lambda self, **kwargs: MockStream(**kwargs))
def test_without_filepath():
    sys.argv[1:] = []

    # TODO: implement
    with pytest.raises(Exception):
        audiotrans.core.main()
