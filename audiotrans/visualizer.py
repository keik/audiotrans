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

        self.init = False
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.axes.set_aspect('auto')

        if chart_type == 'freq':
            self.xhop = 30
            self.draw_data = draw_freq
            self.axes.set_ylim(-1, 1)
            self.axes.set_xlim(0, 1000)

        elif chart_type == 'spec':
            self.xhop = 1
            self.draw_data = draw_spec
            self.axes.set_ylim(0, 100)
            self.axes.set_xticks(np.linspace(0, 100, 6))
            self.axes.set_xticklabels(np.linspace(0, int(framerate / 2), 6))

        elif chart_type == 'specflux':
            self.xhop = 1
            self.draw_data = draw_specflux
            self.axes.set_ylim(0, 100)
            self.axes.set_xlim(0, 200)

        self.background = None

    def draw(self, data):
        if self.init is False:

            # update draw method to omit condition evaluation for performance
            if type(data) is tuple:
                series_num = len(data)
                self.draw = self._draw_multiseries
            else:
                series_num = 1
                self.draw = self._draw_series

            # self.lines = self.axes.plot((np.zeros((self.axes.get_xlim()[1], series_num))))
            self.lines = self.axes.plot((np.zeros((0, series_num))))
            self.axes.legend(np.arange(series_num))
            self.fig.show()
            self.background = self.fig.canvas.copy_from_bbox(self.axes.bbox)
            xlen = int(self.axes.get_xlim()[1])
            for l in self.lines:
                l.set_data(np.arange(xlen), np.zeros(xlen))

        self.draw(data)
        self.init = True

    def _draw_series(self, data):
        self.fig.canvas.restore_region(self.background)
        self.draw_data(data[::self.xhop], self.axes, self.lines[0])
        self.fig.canvas.blit(self.axes.bbox)

    def _draw_multiseries(self, data):
        self.fig.canvas.restore_region(self.background)
        series_num = len(data)
        for i in range(series_num):
            self.draw_data(data[i][::self.xhop], self.axes, self.lines[i])
        self.fig.canvas.blit(self.axes.bbox)


def draw_freq(data, axes, line):
    if len(np.shape(data)) != 1:
        raise TypeError('To draw frequency, input data must formed 1-D array')

    prev_x, prev_y = line.get_data()
    new_y = np.append(prev_y[len(data):], data)
    line.set_data(prev_x, new_y)
    axes.draw_artist(line)


def draw_spec(data, axes, line):
    dim = len(np.shape(data))
    if dim == 1:
        d = np.abs(data)
    elif dim == 2:
        d = np.abs(data.T[0])

    axes.set_xlim(0, len(d))
    line.set_data(np.arange(len(d)), d)
    axes.draw_artist(line)


def draw_specflux(data, axes, line):
    prev_x, prev_y = line.get_data()
    line.set_data(prev_x, np.append(prev_y[len(data):], data))
    axes.draw_artist(line)
