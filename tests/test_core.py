import mock
import pytest

import sys
import time
from threading import Thread
from queue import Queue, Empty

import audiotrans.core


class MockStream():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.counter = 0

        # mocking with thread, which would raise exceptions
        self.t = Thread(target=self.run)
        self.t.e = Queue()  # store exceptions

    def run(self):
        for i in range(10):
            time.sleep(0.1)
            try:
                self.stream_callback(None, 100, None, None)
            except:
                self.t.e.put(sys.exc_info()[1])

    def start_stream(self):
        self.t.start()

    def is_active(self):
        try:
            raise self.t.e.get(block=False)  # retrieve stored exception
        except Empty:
            pass

        return self.t.isAlive()

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
def test_with_transform_which_returns_tuple():
    sys.argv[1:] = ['data/drums.wav', '-t', 'fixture.audiotrans_transform_tuple']
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
