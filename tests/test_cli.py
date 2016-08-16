# -*- coding: utf-8 -*-

import pytest
import sys
import audiotrans.__main__


@pytest.mark.skipif("os.environ['TRAVIS'] == 'true'")
def test_run_with_filepath():
    sys.argv[1:] = ['data/drums.wav']
    audiotrans.__main__.main()


@pytest.mark.skip(reason="TODO: Implement")
def test_run_without_filepath():
    sys.argv[1:] = []
    audiotrans.__main__.main()


@pytest.mark.skipif("os.environ['TRAVIS'] == 'true'")
def test_run_with_verbose_argument():
    sys.argv[1:] = ['data/drums.wav', '-v']
    audiotrans.__main__.main()
