# -*- coding: utf-8 -*-

import pytest
import audiotrans.load_transforms


def test_load_valid_transforms_with_str():
    audiotrans.load_transforms(['fixture.dummy_transform',
                                'fixture.dummy_transform'])


def test_load_valid_transforms_with_tuple():
    audiotrans.load_transforms([['fixture.dummy_transform', 'a', 'b'],
                                ['fixture.dummy_transform', 'c', 'd']])


def test_load_invalid_transforms():
    with pytest.raises(TypeError):
        audiotrans.load_transforms([['fixture.invalid_transform', 'a', 'b']])
