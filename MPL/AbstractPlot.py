from MPL.plot_config import *
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class AbstractPlot(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height))

        self.axes = fig.add_subplot(111)
        self.fig = fig

        super(AbstractPlot, self).__init__(fig)

    def set_scale(self, scale: tuple = ("log", "log")):
        if all(scale):
            x_scale, y_scale = scale
            self.axes.set_yscale(y_scale)
            self.axes.set_xscale(x_scale)

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
        else:
            raise Exception("Incorrect scale data was sent")
