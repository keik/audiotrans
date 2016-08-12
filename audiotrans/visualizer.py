import numpy as np
import matplotlib.pyplot as plt


class Visualizer():

    def __init__(self, chart_type):

        if chart_type not in ['freq', 'spec']:
            raise

        if chart_type == 'freq':
            self.xhop = 30
        elif chart_type == 'spec':
            # TODO: implement
            raise 'Not implemented'

        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.axes.set_aspect('auto')
        self.axes.set_xlim(0, 1000)
        self.axes.set_ylim(-1, 1)

        self.fig.show()

        self.background = self.fig.canvas.copy_from_bbox(self.axes.bbox)
        self.line = self.axes.plot(np.arange(0, 1000), np.zeros(1000))[0]

    def draw(self, data):
        self.fig.canvas.restore_region(self.background)
        d = data[::self.xhop]
        prev_x, prev_y = self.line.get_data()
        self.line.set_data(prev_x, np.append(prev_y[len(d):], d))
        self.axes.draw_artist(self.line)
        self.fig.canvas.blit(self.axes.bbox)
