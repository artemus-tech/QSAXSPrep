# -*- coding: utf-8 -*-
import matplotlib           # http://matplotlib.org

"""
It is best practice not to import pyplot if you are embedding. Instead use, from matplotlib.figure import Figure
Clear the figure before plotting with self.fig.clear() and create new axes.
Finally, refresh the canvas with self.canvas.draw()
"""


matplotlib.rcParams["text.usetex"] = False
matplotlib.rcParams["legend.numpoints"] = 3
matplotlib.rcParams['font.size'] = 12.0
matplotlib.rcParams['legend.fontsize']=12.0
matplotlib.rcParams['figure.figsize']  = 8,6    # figure size in inches
matplotlib.rcParams['figure.dpi'] = 120         # figure dots per inch
matplotlib.rcParams['backend'] = 'Qt5Agg'
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams['lines.linewidth'] = 2
# Presets subplots_adjust
# left  = 0.125  # the left side of the subplots of the figure
# right = 0.657  # the right side of the subplots of the figure
# bottom = 0.1   # the bottom of the subplots of the figure
# top = 0.9      # the top of the subplots of the figure
# wspace = 0.2   # the amount of width reserved for blank space between subplots
# hspace = 0.2   # the amount of height reserved for white space between subplots

