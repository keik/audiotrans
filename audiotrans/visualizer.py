import numpy as np
import matplotlib.pyplot as plt


class Visualizer():

    def __init__(self, chart_type, framerate):

        if chart_type not in ['freq', 'spec']:
            raise

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

        self.fig.show()

        self.background = self.fig.canvas.copy_from_bbox(self.axes.bbox)
        self.line = self.axes.plot(np.arange(0, 1000), np.zeros(1000))[0]

    def _draw_freq(self, data):
        self.fig.canvas.restore_region(self.background)

        d = data[::self.xhop]
        prev_x, prev_y = self.line.get_data()

        self.line.set_data(prev_x, np.append(prev_y[len(d):], d))
        self.axes.draw_artist(self.line)
        self.fig.canvas.blit(self.axes.bbox)

    def _draw_spec(self, data):
        self.fig.canvas.restore_region(self.background)

        d = np.abs(data)
        self.axes.set_xlim(0, len(d) / 2)

        self.line.set_data(np.arange(len(d)), d)
        self.axes.draw_artist(self.line)
        self.fig.canvas.blit(self.axes.bbox)
