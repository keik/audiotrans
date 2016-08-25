import numpy as np
import matplotlib.pyplot as plt


class Visualizer():
    """
    Visualize transformed data.

    Parameters
    ----------
    chart_type : str
        chart type to data visualization.

        freq : Display frequency of wave.
            To plot, transformed data must be formed 1-D array of wave.
        spec : Display spectrum of wave.
            To plot, Transformed data must be formed 1-D array of spectrum
            or 2-D array of spectrogram.
        specflux : Display spectral flux
            To plot, transformed data must be formed 1-D array of wave.

    framerate : int
        framerate of loading data
    """

    def __init__(self, chart_type, framerate):

        # TODO: modular
        if chart_type not in ['freq', 'spec', 'specflux']:
            raise TypeError('chart_type can accept `freq` or `spec` or `specflux`')

        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.axes.set_aspect('auto')

        if chart_type == 'freq':
            self.xhop = 30
            self.draw = self._draw_freq
            self.axes.set_ylim(-1, 1)
            self.axes.set_xlim(0, 1000)

        elif chart_type == 'spec':
            self.draw = self._draw_spec
            self.axes.set_ylim(0, 100)
            self.axes.set_xticks(np.linspace(0, 100, 6))
            self.axes.set_xticklabels(np.linspace(0, int(framerate / 2), 6))

        elif chart_type == 'specflux':
            self.xhop = 1
            self.draw = self._draw_specflux
            self.axes.set_ylim(0, 100)
            self.axes.set_xlim(0, 1000)

        self.fig.show()

        self.background = self.fig.canvas.copy_from_bbox(self.axes.bbox)

        # TODO: modular
        self.lines = self.axes.plot((np.zeros((1000, 2))))

    def _draw_freq(self, data):
        self.fig.canvas.restore_region(self.background)

        if len(np.shape(data)) != 1:
            raise TypeError('To draw frequency, input data must formed 1-D array')

        d = data[::self.xhop]
        prev_x, prev_y = self.lines[0].get_data()

        self.lines[0].set_data(prev_x, np.append(prev_y[len(d):], d))
        self.axes.draw_artist(self.lines[0])
        self.fig.canvas.blit(self.axes.bbox)

    def _draw_spec(self, data):
        self.fig.canvas.restore_region(self.background)

        dim = len(np.shape(data))
        if dim == 1:
            d = np.abs(data)
        elif dim == 2:
            d = np.abs(data.T[0])
        self.axes.set_xlim(0, len(d))

        self.lines[0].set_data(np.arange(len(d)), d)
        self.axes.draw_artist(self.lines[0])
        self.fig.canvas.blit(self.axes.bbox)

    def _draw_specflux(self, data):
        specflux, threshold = data
        self.fig.canvas.restore_region(self.background)

        s, t = specflux[::self.xhop], (threshold[::self.xhop] + 10)
        prev_s_x, prev_s_y = self.lines[0].get_data()
        prev_t_x, prev_t_y = self.lines[1].get_data()

        self.lines[0].set_data(prev_s_x, np.append(prev_s_y[len(s):], s))
        self.lines[1].set_data(prev_t_x, np.append(prev_t_y[len(t):], t))
        self.axes.draw_artist(self.lines[0])
        self.axes.draw_artist(self.lines[1])
        self.fig.canvas.blit(self.axes.bbox)
