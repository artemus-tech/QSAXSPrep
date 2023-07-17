from MPL.AbstractPlot import *
import numpy as np


class MplCanvas(AbstractPlot):

    def get_plot(self, data: np.ndarray, scale: tuple = ("log", "log"),
                 label_list=["$q, nm^{-1}$", "I, arb. units"], legend=["I(q)"]):

        if data.ndim == 2:
            number_rows, number_cols = data.shape

            if number_cols and number_rows > 0:
                x_scale = self.axes.get_xscale()
                y_scale = self.axes.get_yscale()

                self.axes.clear()


                if number_cols == 2:
                    self.axes.plot(data[:, 0], data[:, 1])
                if number_cols == 4:
                    self.axes.plot(data[:, 0], data[:, 1])
                    self.axes.plot(data[:, 2], data[:, 3])
                if number_cols == 6:
                    self.axes.plot(data[:, 0], data[:, 1])
                    self.axes.plot(data[:, 2], data[:, 3])
                    self.axes.plot(data[:, 4], data[:, 5])
                if number_cols == 8:
                    self.axes.plot(data[:, 0], data[:, 1])
                    self.axes.plot(data[:, 2], data[:, 3])
                    self.axes.plot(data[:, 4], data[:, 5])
                    self.axes.plot(data[:, 6], data[:, 7])

                self.axes.set_xlabel(label_list[0])
                self.axes.set_ylabel(label_list[1])
                self.set_scale(scale=(x_scale,y_scale))
                self.axes.legend(legend)
                self.fig.canvas.draw()
