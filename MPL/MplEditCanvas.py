# -*- coding: utf-8 -*-
from MPL.AbstractPlot import AbstractPlot
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import Common.cast as ct
import numpy as np


class MplEditCanvas(AbstractPlot):
    """
    Allow user to add points in interactive mode
    """

    def __del__(self):
        """Destructor"""
        self._disconnect()
        print('destroyed')

    def __init__(self, restrict=2, width=5, height=4, dpi=100):
        """Constructor method, initialize presets"""
        # event definition

        self._output = None
        self.event = None
        # set marker size
        self.msz = 8
        # set marker zoome size
        self.marker_zoom_size = 12
        # set picker
        self.pick_numb = 5
        # set numbers of points
        self.restrict = restrict
        # generate  vector abscissa
        self.src_axis_scale_x = ct.init_zero_length_array()
        self.src_axis_scale_y = ct.init_zero_length_array()
        # main point collection storage
        self.curve_points = []
        self._bounds = []
        self.clickId = None
        self.closeId = None
        self.moveId = None

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.fig = fig

        super(MplEditCanvas, self).__init__(fig)

    def get_plot(self, data, label_list) -> None:
        """
        :param data: matrix[X,Y]
        :return: void
        """
        # save src-generated Grid
        self.src_axis_scale_x = data[:, 0]
        self.src_axis_scale_y = data[:, 1]
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        with plt.ion():

            if len(self.src_axis_scale_x) > 1:
                for i in range(len(self.src_axis_scale_x)):
                    point, = self.axes.plot(self.src_axis_scale_x[i], self.src_axis_scale_y[i], 'bo',
                                            markersize=self.msz)
                    self.curve_points.append(point)
                self.axes.set_xlabel(label_list[0])
                self.axes.set_ylabel(label_list[1])

    def bind_datastorage(self, data, output="data.txt", label_list=["$q, nm^{-1}$", "I, arb. units"]):
        self.get_plot(data, label_list)
        self._connect()
        self._output = output

    def _connect(self):
        # connect to click motion_notify_event
        self.clickId = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        # connect to motion_notify_event
        self.moveId = self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        # connect to close plot window event
        self.closeId = self.fig.canvas.mpl_connect('close_event', self.on_close)

    def _disconnect(self):
        if self.clickId:
            self.fig.canvas.mpl_disconnect(self.clickId)
        if self.moveId:
            self.fig.canvas.mpl_disconnect(self.moveId)
        if self.closeId:
            self.fig.canvas.mpl_disconnect(self.closeId)

    def __in_array_q1q2(self, event):
        for point in self._bounds:
            if point.contains(event)[0]:
                point.remove()
                # trace, to show deleted points formed location
                target, = self.axes.plot(point.get_xdata()[0], point.get_ydata()[0], 'wo', markersize=self.msz,
                                         picker=self.pick_numb)
                self._bounds.remove(point)

                target.remove()

        return self._bounds

    def on_click(self, event):
        if event.inaxes is not None and event.inaxes == self.axes:
            axes = event.inaxes
            # for axes in event.canvas.figure.axes[0]:
            # axes = event.canvas.figure.axes
            # to prevent merge modes with adding points procedure
            if axes.get_navigate_mode() is None:

                if event.xdata is not None and event.ydata is not None:
                    # get current axis
                    # overlay plots.
                    # ax.hold(True)
                    # left click branch
                    if event.button == 1 and len(self._bounds) < self.restrict:
                        point, = self.axes.plot(event.xdata, event.ydata, 'ro', markersize=self.msz,
                                                picker=self.pick_numb)
                        self._bounds.append(point)
                    # right click branch
                    if event.button == 3:
                        # self.curve_points = self.__in_array(event)
                        self._bounds = self.__in_array_q1q2(event)
                    # refresh plot
                    self.fig.canvas.draw()
                    # save result into file and buffer
                    appended = np.unique(sorted([point.get_xdata()[0] for point in self._bounds]))
                    np.savetxt(self._output, appended)

    def on_move(self, event):
        if event.inaxes is not None and event.inaxes == self.axes:
            for point in self._bounds:
                should_be_zoomed = (point.contains(event)[0] == True)
                """onmousemove  return 30, onmouseout return 10"""
                marker_size = 2 * self.msz if should_be_zoomed else self.msz
                # zoom point
                point.set_markersize(marker_size)
            # refresh plot
            self.fig.canvas.draw()

    def on_close(self, event):
        pass
