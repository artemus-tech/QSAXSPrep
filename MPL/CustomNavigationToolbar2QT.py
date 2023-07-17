from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT


class CustomNavigationToolbar2QT(NavigationToolbar2QT):

    def __init__(self, figure_canvas, parent=None):
        # only display the buttons we need
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure')
        )
        NavigationToolbar2QT.__init__(self, figure_canvas, parent=None)

