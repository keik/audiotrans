# -*- coding: utf-8 -*-

import pytest
import audiotrans.load_transforms


def test_load_valid_transforms_with_str():
    audiotrans.load_transforms(['fixture.audiotrans_transform_dummy',
                                'fixture.audiotrans_transform_dummy'])


def test_load_valid_transforms_with_tuple():
    audiotrans.load_transforms([['fixture.audiotrans_transform_dummy', 'a', 'b'],
                                ['fixture.audiotrans_transform_dummy', 'c', 'd']])


def test_load_invalid_transforms():
    with pytest.raises(TypeError):
        audiotrans.load_transforms([['fixture.audiotrans_transform_invalid', 'a', 'b']])
