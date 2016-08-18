import pytest
import numpy as np
from audiotrans.visualizer import Visualizer


@pytest.mark.parametrize('chart_type', [None,
                                        'invalid'])
def test_instantiate_with_invalid_chart_type(chart_type):
    with pytest.raises(TypeError):
        Visualizer(chart_type=chart_type, framerate=44100)


def test_draw_freq():
    visualizer = Visualizer(chart_type='freq', framerate=44100)

    assert visualizer.draw == visualizer._draw_freq, \
        """`draw` method is now for freq"""

    visualizer.draw(np.array([1, 2, 3, 4, 5]))
    with pytest.raises(TypeError):
        visualizer.draw(np.array([[1, 2, 3, 4, 5]]))


def test_draw_spec():
    visualizer = Visualizer(chart_type='spec', framerate=44100)

    assert visualizer.draw == visualizer._draw_spec, \
        """`draw` method is now for spec"""

    visualizer.draw(np.array([1, 2, 3, 4, 5]))
    visualizer.draw(np.array([[1, 2, 3, 4, 5]]))
