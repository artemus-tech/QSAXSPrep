from typing import Callable, List, Tuple

from MPL.MplCanvas import MplCanvas
from MPL.MplEditCanvas import MplEditCanvas
from MPL.CustomNavigationToolbar2QT import CustomNavigationToolbar2QT


class MplRepository:
    def __init__(self,
                 edit_plot_factory: Callable[..., MplEditCanvas],
                 plot_factory: Callable[..., MplCanvas],
                 toolbar: Callable[..., CustomNavigationToolbar2QT]) -> None:
        self.edit_plot_factory = edit_plot_factory
        self.plot_factory = plot_factory
        self.toolbar = toolbar

    def generate_edit_plots_collection(self, edit_plot_number) -> List[
        Tuple[CustomNavigationToolbar2QT, MplEditCanvas]
    ]:
        edit_plot_array = [self.edit_plot_factory() for i in range(edit_plot_number)]
        return [
            (plt, self.toolbar(plt)) for plt in edit_plot_array
        ]

    def generate_plots_collection(self, plot_number: int) -> List[
        Tuple[CustomNavigationToolbar2QT, MplCanvas]
    ]:
        plot_array = [self.plot_factory() for i in range(plot_number)]

        return [(plt, self.toolbar(plt)) for plt in plot_array]
